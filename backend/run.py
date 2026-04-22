import os

import toml
import uvicorn
from fastapi import HTTPException
from fastapi.responses import FileResponse

from app import create_app

app = create_app()


@app.get('/WW_verify_ICp5GPc8bQthGR1c.txt')
async def verify_file():
    try:
        # 使用绝对路径来确保文件路径正确
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_path = os.path.join(path, "./backend")
        file_path = os.path.join(base_path, "doc", "WW_verify_ICp5GPc8bQthGR1c.txt")
        return FileResponse(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="文件未找到")


@app.get('/WW_verify_P9AOhD1zYFk0x0zK.txt')
async def verify_file():
    try:
        # 使用绝对路径来确保文件路径正确
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_path = os.path.join(path, "./backend")
        file_path = os.path.join(base_path, "doc", "WW_verify_P9AOhD1zYFk0x0zK.txt")
        return FileResponse(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="文件未找到")


if __name__ == '__main__':
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_path = os.path.join(path, "./backend")
    app_config = toml.load(fr"{base_path}/app_config.toml")
    active = app_config.get('settings', {}).get('active', 'development')
    config_name = f'app_{active}_config.toml'
    config = toml.load(fr"{base_path}/config/{config_name}")
    port = config.get('fastapi', {}).get('port', 8302)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_config=None
    )
