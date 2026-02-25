"""
图片处理工具
"""
import base64
import io
from typing import Tuple
from PIL import Image


def validate_image(file_content: bytes) -> bool:
    """验证图片格式"""
    try:
        img = Image.open(io.BytesIO(file_content))
        return img.format in ['JPEG', 'JPG', 'PNG']
    except Exception:
        return False


def get_image_info(file_content: bytes) -> Tuple[int, int]:
    """获取图片尺寸"""
    img = Image.open(io.BytesIO(file_content))
    return img.size


def resize_image_if_needed(file_content: bytes, max_size: int = 1024) -> bytes:
    """如果图片过大则 resize"""
    img = Image.open(io.BytesIO(file_content))
    width, height = img.size

    if width <= max_size and height <= max_size:
        return file_content

    # 等比缩放
    if width > height:
        new_width = max_size
        new_height = int(height * max_size / width)
    else:
        new_height = max_size
        new_width = int(width * max_size / height)

    img = img.resize((new_width, new_height), Image.LANCZOS)

    output = io.BytesIO()
    img.save(output, format=img.format or 'JPEG')
    return output.getvalue()


def image_to_base64(file_content: bytes) -> str:
    """将图片转为 base64 字符串"""
    return base64.b64encode(file_content).decode('utf-8')


def get_image_mime_type(file_content: bytes) -> str:
    """获取图片 MIME 类型"""
    img = Image.open(io.BytesIO(file_content))
    if img.format == 'PNG':
        return "image/png"
    return "image/jpeg"
