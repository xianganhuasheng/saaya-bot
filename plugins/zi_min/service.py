from pathlib import Path
from typing import Optional, Tuple
import tempfile

from nonebot.log import logger

from .utils import validate_text, get_resource_paths, read_image_bytes


# 导入PIL库
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    logger.warning("PIL (Pillow) 库未安装，籽岷插件将无法正常工作")


class ZMinService:
    """籽岷图片生成服务"""
    
    def __init__(
        self,
        data_dir: Path,
        base_image_filename: str,
        font_filename: str,
        font_size: int,
        text_color: Tuple[int, int, int],
        max_text_length: int
    ):
        """
        初始化服务
        
        Args:
            data_dir: 数据目录
            base_image_filename: 基础图片文件名
            font_filename: 字体文件名
            font_size: 字体大小
            text_color: 文字颜色
            max_text_length: 最大文本长度
        """
        self.data_dir = data_dir
        self.base_image_filename = base_image_filename
        self.font_filename = font_filename
        self.font_size = font_size
        self.text_color = text_color
        self.max_text_length = max_text_length
        
        # 获取资源路径
        self.base_image_path, self.font_path = get_resource_paths(
            data_dir, base_image_filename, font_filename
        )
    
    async def generate_zmin_image(
        self, 
        text_left: str, 
        text_middle: str, 
        text_right: str,
        cache_dir: Path
    ) -> Optional[Path]:
        """
        生成籽岷图片
        
        Args:
            text_left: 左侧文字
            text_middle: 中间文字
            text_right: 右侧文字
            cache_dir: 缓存目录
            
        Returns:
            生成的图片路径，失败时返回None
        """
        if not HAS_PIL:
            logger.error("PIL (Pillow) 库未安装，无法生成图片")
            return None
        
        # 验证文字
        for text in [text_left, text_middle, text_right]:
            validate_text(text, self.max_text_length)
        
        # 检查基础图片是否存在
        if not self.base_image_path.exists():
            logger.error(f"基础图片不存在: {self.base_image_path}")
            return None
        
        try:
            # 加载图片
            img = Image.open(self.base_image_path)
            img = img.convert("RGB")
            
            draw = ImageDraw.Draw(img)
            
            # 加载字体
            try:
                font = ImageFont.truetype(str(self.font_path), self.font_size)
            except IOError:
                logger.warning(f"字体文件不存在: {self.font_path}，使用默认字体")
                font = ImageFont.load_default()
            
            # 定义要擦除的区域 (左上角x, 左上角y, 右下角x, 右下角y)
            # 这些坐标是基于原图估算的
            erase_areas = [
                (100, 150, 230, 220),  # 左侧区域
                (430, 150, 560, 220),  # 中间区域
                (660, 150, 940, 220)   # 右侧区域
            ]
            
            texts = [text_left, text_middle, text_right]
            
            # 循环处理每个位置：擦除旧文字，绘制新文字
            for i, text in enumerate(texts):
                area = erase_areas[i]
                
                # 擦除原有区域 (填充白色矩形)
                draw.rectangle(area, fill=(255, 255, 255))
                
                # 计算文字的宽高
                try:
                    left, top, right, bottom = font.getbbox(text)
                    text_width = right - left
                    text_height = bottom - top
                except AttributeError:
                    # 对于旧版本的 Pillow，使用 getsize
                    text_width, text_height = font.getsize(text)
                
                area_width = area[2] - area[0]
                area_height = area[3] - area[1]
                
                # 计算居中坐标
                x = area[0] + (area_width - text_width) / 2
                y = area[1] + (area_height - text_height) / 2
                
                # 微调 Y 坐标，让文字视觉上更居中
                y -= text_height * 0.1
                
                # 绘制新文字
                draw.text((x, y), text, font=font, fill=self.text_color)
            
            # 保存到临时文件，使用PNG格式确保兼容性
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir=cache_dir) as tmp:
                output_path = Path(tmp.name)
                img.save(output_path, format='PNG')
                return output_path
                
        except Exception as e:
            logger.error(f"生成图片失败: {e}")
            return None
    
    def check_resources(self) -> bool:
        """
        检查资源文件是否存在
        
        Returns:
            bool: 资源是否完整
        """
        resources_exist = self.base_image_path.exists()
        if not resources_exist:
            logger.warning(f"基础图片不存在: {self.base_image_path}")
        
        # 字体文件不是必需的（可以使用默认字体）
        if not self.font_path.exists():
            logger.warning(f"字体文件不存在: {self.font_path}")
        
        return resources_exist