import random
import math
import os
from PIL import Image, ImageDraw, ImageFont
from pypinyin import pinyin, Style


class VerificationCodeService:
    def __init__(
            self,
    ):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.__base_path = os.path.join(path, "../")
        self.__FONT_PATH = fr"{self.__base_path}/doc/font/simfang.ttf"
        self.__PINYIN_FONT_PATH = fr"{self.__base_path}/doc/font/simfang.ttf"
        self.__PIC_DIR = fr"{self.__base_path}/temp"

    def generate_behavior_verification_code(self):
        """生成行为验证码"""
        try:
            # 随机选择图片并打开
            image_path = self.choose_random_image()
            image = Image.open(image_path)

            # 在图片上添加文字，生成验证码
            correct_text, text_positions = self.create_captcha_with_image(image)
            print(f"正确的文字: {correct_text}")
            print(f"文字位置: {text_positions}")

        except Exception as e:
            print(f"生成验证码时出错: {e}")

    # 随机生成中文字符
    @staticmethod
    def get_random_chinese_characters(count):
        """生成随机中文字符"""
        return ''.join(random.choices([chr(i) for i in range(0x4e00, 0x9fff)], k=count))

    @staticmethod
    def get_random_color():
        """返回随机的RGB颜色"""
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @staticmethod
    def draw_text_with_outline(draw, x, y, text, font, text_color, outline_color, outline_width=2):
        """在指定位置绘制带有描边的文字"""
        # 先绘制描边，使用比原文字略大的位置
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                if offset_x == 0 and offset_y == 0:  # 跳过原始位置
                    continue
                draw.text((x + offset_x, y + offset_y), text, font=font, fill=outline_color)

        # 在描边内绘制原文字
        draw.text((x, y), text, font=font, fill=text_color)

    @staticmethod
    def rotate_point(x, y, angle, center_x, center_y):
        """根据旋转角度和中心点旋转给定点"""
        angle_rad = math.radians(angle)
        x_new = math.cos(angle_rad) * (x - center_x) - math.sin(angle_rad) * (y - center_y) + center_x
        y_new = math.sin(angle_rad) * (x - center_x) + math.cos(angle_rad) * (y - center_y) + center_y
        return x_new, y_new

    @staticmethod
    def get_pinyin(text):
        """获取中文字的拼音，带有声调"""
        pinyin_result = pinyin(text, style=Style.TONE)  # 使用TONE获取带声调的拼音
        return ''.join([item[0] for item in pinyin_result])

    def choose_random_image(self):
        """从 ./pic 目录中随机选择一张图片"""
        images = [f for f in os.listdir(self.__PIC_DIR) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        if not images:
            raise FileNotFoundError(f"No images found in {self.__PIC_DIR}")
        image_path = os.path.join(self.__PIC_DIR, random.choice(images))
        return image_path

    def create_captcha_with_image(self, image, max_width=400, max_height=150, text_count=5):
        """在下载的第三方图片上添加随机旋转、扭曲、颜色和描边的文字，生成验证码"""
        # 获取原始图片的宽高
        original_width, original_height = image.size
        original_ratio = original_width / original_height

        # 计算目标宽高，保持原始比例
        if original_ratio > 1:
            target_width = min(max_width, original_width)
            target_height = int(target_width / original_ratio)
        else:
            target_height = min(max_height, original_height)
            target_width = int(target_height * original_ratio)

        # 调整图片大小
        image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

        font = ImageFont.truetype(self.__FONT_PATH, 24)  # 缩小文字字号为24
        pinyin_font = ImageFont.truetype(self.__PINYIN_FONT_PATH, 20)  # 设置拼音字体，字号缩小为20

        # 随机生成指定数量的中文字符
        all_texts = [self.get_random_chinese_characters(1) for _ in range(text_count)]

        # 随机选择正确的文字
        correct_text = random.choice(all_texts)

        text_positions = {}

        for text in all_texts:
            x = random.randint(50, target_width - 100)
            y = random.randint(30, target_height - 50)

            angle = random.randint(-30, 30)
            text_image = Image.new('RGBA', (target_width, target_height), (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_image)

            text_color = self.get_random_color()
            outline_color = self.get_random_color()

            # 获取拼音的边界框并计算宽高
            pinyin_text = self.get_pinyin(text)  # 获取带声调的拼音

            # 绘制拼音
            self.draw_text_with_outline(text_draw, x, y - 20, pinyin_text, pinyin_font, text_color, outline_color,
                                        outline_width=1)

            # 绘制汉字
            self.draw_text_with_outline(text_draw, x, y, text, font, text_color, outline_color, outline_width=2)

            # 旋转文字时使用抗锯齿，减少模糊
            rotated_text_image = text_image.rotate(angle, resample=Image.BICUBIC, expand=1)

            # 计算旋转后的文字的实际位置
            rotated_bbox = rotated_text_image.getbbox()
            text_positions[text] = {
                "top_left": (rotated_bbox[0], rotated_bbox[1]),
                "bottom_right": (rotated_bbox[2], rotated_bbox[3]),
            }

            # 将旋转后的文字贴到原图上
            image.paste(rotated_text_image, (0, 0), rotated_text_image)

        image.save(f"./captcha_pexels.jpg")

        return correct_text, text_positions
