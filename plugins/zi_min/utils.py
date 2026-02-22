from io import BytesIO
from pathlib import Path
from typing import Tuple, Optional
from nonebot.adapters import MessageSegment
from nonebot.log import logger


def validate_text(text: str, max_length: int = 15) -> bool:
    """
    检查输入的字符串是否符合要求。
    
    Args:
        text: 要验证的文字
        max_length: 最大长度限制
        
    Returns:
        bool: 验证是否通过
        
    Raises:
        ValueError: 验证失败时抛出
    """
    if not text:
        raise ValueError("输入的文字不能为空。")
    if len(text) > max_length:
        raise ValueError(f"文字 '{text}' 过长，请控制在{max_length}个字符以内。")
    return True


def get_resource_paths(data_dir: Path, base_image_filename: str, font_filename: str) -> Tuple[Path, Path]:
    """
    获取资源文件路径
    
    Args:
        data_dir: 数据目录
        base_image_filename: 基础图片文件名
        font_filename: 字体文件名
        
    Returns:
        (base_image_path, font_path) 元组
    """
    base_image_path = data_dir / base_image_filename
    font_path = data_dir / font_filename
    return base_image_path, font_path


def ensure_dirs_exist(*dirs: Path) -> None:
    """
    确保目录存在
    
    Args:
        *dirs: 要创建的目录
    """
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"确保目录存在: {directory}")


def read_image_bytes(image_path: Path) -> Optional[bytes]:
    """
    读取图片文件为字节数据
    
    Args:
        image_path: 图片文件路径
        
    Returns:
        bytes: 图片字节数据，失败时返回None
    """
    try:
        with open(image_path, "rb") as f:
            return f.read()
    except Exception as e:
        logger.error(f"读取图片文件失败: {image_path}, 错误: {e}")
        return None


def image_to_message(image_bytes: bytes, mime_type: str = "image/jpeg") -> "MessageSegment":
    """
    将图片字节数据转换为MessageSegment对象
    
    Args:
        image_bytes: 图片字节数据
        mime_type: 图片MIME类型
        
    Returns:
        MessageSegment: 图片消息段
    """
    from nonebot.adapters.satori import MessageSegment
    return MessageSegment.image(raw=image_bytes, mime=mime_type)
