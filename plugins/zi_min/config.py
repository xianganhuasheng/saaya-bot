from pydantic import BaseModel


class Config(BaseModel):
    """籽岷插件配置"""
    # 是否启用籽岷功能
    enable_zi_min: bool = True
    # 基础图片文件名（放在插件资源目录中）
    base_image_filename: str = "zimin.jpg"
    # 字体文件名（放在插件资源目录中）
    font_filename: str = "simhei.ttf"
    # 字体大小
    font_size: int = 50
    # 文字颜色 (R, G, B)
    text_color_r: int = 0
    text_color_g: int = 0
    text_color_b: int = 0
    # 最大文本长度
    max_text_length: int = 15