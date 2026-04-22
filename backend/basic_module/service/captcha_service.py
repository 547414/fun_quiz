import json
import logging
import random
import os
import io
import base64
import secrets
import string
import uuid

from PIL import Image, ImageDraw, ImageFont
from pypinyin import pinyin, Style
import toml

from basic.error.base_error import BusinessError
from basic.redis_client.redis_client import RedisClient
from basic_module.model.captcha_model import CaptchaTextPositionModel, CaptchaTextPositionDetailModel, CaptchaModel, \
    CaptchaValidateParamsModel, CaptchaViewModel

logger = logging.getLogger('captcha_service')


class CaptchaService:

    def __init__(
            self,
            redis_client: RedisClient,

    ):
        self.__redis_client = redis_client
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.__base_path = os.path.join(path, "../")
        self.font_path = f"{self.__base_path}/doc/font/simfang.ttf"
        self.pinyin_font_path = f"{self.__base_path}/doc/font/simfang.ttf"
        self.pic_dir = f"{self.__base_path}/doc/pic"
        self.__app_config = toml.load(fr"{self.__base_path}/app_config.toml")
        self.__active = self.__app_config.get('settings', {}).get('active', 'development')
        self.__config_name = f'app_{self.__active}_config.toml'
        self.__config = toml.load(fr"{self.__base_path}/config/{self.__config_name}")

    @staticmethod
    def get_random_chinese_characters(count):
        return ''.join(random.choices([chr(i) for i in range(0x4e00, 0x9fff)], k=count))

    @staticmethod
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @staticmethod
    def draw_text_with_outline(draw, x, y, text, font, text_color, outline_color, outline_width=2):
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                if offset_x == 0 and offset_y == 0:
                    continue
                draw.text((x + offset_x, y + offset_y), text, font=font, fill=outline_color)
        draw.text((x, y), text, font=font, fill=text_color)

    @staticmethod
    def get_pinyin(text):
        pinyin_result = pinyin(text, style=Style.TONE)
        return ''.join([item[0] for item in pinyin_result])

    def choose_random_image(self):
        images = [f for f in os.listdir(self.pic_dir) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        if not images:
            raise FileNotFoundError(f"No images found in {self.pic_dir}")
        image_path = os.path.join(self.pic_dir, random.choice(images))
        return Image.open(image_path)

    def create_captcha_with_image(self, image, max_width=400, max_height=150, text_count=5):
        original_width, original_height = image.size
        original_ratio = original_width / original_height

        if original_ratio > 1:
            target_width = min(max_width, original_width)
            target_height = int(target_width / original_ratio)
        else:
            target_height = min(max_height, original_height)
            target_width = int(target_height * original_ratio)

        image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

        font = ImageFont.truetype(self.font_path, 36)
        pinyin_font = ImageFont.truetype(self.pinyin_font_path, 28)

        all_texts = [self.get_random_chinese_characters(1) for _ in range(text_count)]
        correct_texts = random.sample(all_texts, 3)
        text_positions = {}

        for text in all_texts:
            x = random.randint(50, target_width - 150)
            y = random.randint(30, target_height - 120)
            angle = random.randint(-20, 20)

            text_image = Image.new('RGBA', (target_width, target_height), (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_image)

            text_color = self.get_random_color()
            outline_color = self.get_random_color()
            pinyin_text = self.get_pinyin(text)

            self.draw_text_with_outline(text_draw, x, y - 20, pinyin_text, pinyin_font, text_color, outline_color, 1)
            self.draw_text_with_outline(text_draw, x, y, text, font, text_color, outline_color, 2)

            rotated_text_image = text_image.rotate(angle, resample=Image.BICUBIC, expand=1)
            rotated_bbox = rotated_text_image.getbbox()
            text_positions[text] = CaptchaTextPositionModel(
                text=text,
                pinyin=pinyin_text,
                top_left=CaptchaTextPositionDetailModel(
                    x=rotated_bbox[0],
                    y=rotated_bbox[1],
                ),
                bottom_right=CaptchaTextPositionDetailModel(
                    x=rotated_bbox[2],
                    y=rotated_bbox[3],
                )
            )
            image.paste(rotated_text_image, (0, 0), rotated_text_image)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return base64_image, correct_texts, text_positions

    def generate_verification_code_base64(self):
        image = self.choose_random_image()
        base64_image, correct_texts, text_positions = self.create_captcha_with_image(image)
        uuid_str = str(uuid.uuid4())
        captcha = CaptchaModel(
            captcha_id=uuid_str,
            correct_texts=correct_texts,
            text_positions=text_positions,
        )
        self.__redis_client.set_value(
            key=f"captcha_{uuid_str}",
            value=json.dumps(captcha.model_dump()),
            expiration=500
        )
        base64_image_str = f"data:image/jpeg;base64,{base64_image}"
        correct_pinyin_texts = []
        for text in correct_texts:
            pinyin_text = captcha.text_positions[text].pinyin
            correct_pinyin_texts.append(pinyin_text)
        return CaptchaViewModel(
            captcha_id=uuid_str,
            correct_texts=correct_texts,
            correct_pinyin_texts=correct_pinyin_texts,
            captcha_base64=base64_image_str,
        )

    def validate_captcha(self, params: CaptchaValidateParamsModel):
        redis_captcha = self.__redis_client.get_value(
            key=f"captcha_{params.captcha_id}",
        )
        if not redis_captcha:
            raise BusinessError("验证码不存在或已过期")
        captcha_info = CaptchaModel(**json.loads(redis_captcha))
        if not params.text_positions:
            raise BusinessError("验证码不能为空")
        if len(params.text_positions) != len(captcha_info.correct_texts):
            raise BusinessError("验证码数量不匹配")
        # 校验验证码顺序
        for i, text_position in enumerate(params.text_positions):
            if text_position.text != captcha_info.correct_texts[i]:
                raise BusinessError(f"验证码文本错误")
            # 校验验证码位置
            top_left = captcha_info.text_positions[text_position.text].top_left
            bottom_right = captcha_info.text_positions[text_position.text].bottom_right
            in_x = top_left.x <= text_position.x <= bottom_right.x
            in_y = top_left.y <= text_position.y <= bottom_right.y
            if not (in_x and in_y):
                raise BusinessError(f"验证失败")
        validate_auth_code = self.generate_secure_key()
        self.__redis_client.set_value(
            key=f"captcha_validate_auth_code_{params.captcha_id}",
            value=validate_auth_code,
            expiration=500
        )
        return validate_auth_code

    @staticmethod
    def generate_secure_key(length=32):
        charset = string.ascii_letters + string.digits
        while True:
            key = ''.join(secrets.choice(charset) for _ in range(length))
            if (any(c.islower() for c in key) and
                    any(c.isupper() for c in key) and
                    any(c.isdigit() for c in key)):
                return key
