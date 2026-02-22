from pathlib import Path
from nonebot.log import logger
import shutil
import os


async def initialize_resources(data_dir: Path, cache_dir: Path) -> None:
    """
    初始化籽岷插件资源
    
    Args:
        data_dir: 数据目录
        cache_dir: 缓存目录
    """
    logger.info("籽岷插件: 正在检查资源")
    
    # 确保目录存在
    data_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # 检查基础图片是否存在
    base_image_path = data_dir / "zimin.jpg"
    if not base_image_path.exists():
        logger.warning(f"基础图片不存在: {base_image_path}")
        logger.info("请将基础图片 'zimin.jpg' 放置在以下目录:")
        logger.info(f"  {data_dir}")
        logger.info("或者使用默认的测试图片")
        
        # 可以在这里添加下载默认资源的逻辑
        # 例如：从网络下载或复制内置资源
    
    # 检查字体文件是否存在
    font_path = data_dir / "simhei.ttf"
    if not font_path.exists():
        logger.warning(f"字体文件不存在: {font_path}")
        logger.info("请将中文字体文件 'simhei.ttf' 放置在以下目录:")
        logger.info(f"  {data_dir}")
        logger.info("如果没有中文字体，将使用系统默认字体（可能不支持中文）")
    
    logger.info("籽岷插件: 资源检查完成")


def copy_default_resources(data_dir: Path) -> None:
    """
    复制默认资源文件（如果有的话）
    
    Args:
        data_dir: 目标数据目录
    """
    # 这里可以添加复制内置资源的逻辑
    # 例如：从插件内部资源目录复制到用户数据目录
    
    # 示例：检查是否存在测试图片
    test_image = Path("test_zimin.jpg")
    if test_image.exists():
        target_path = data_dir / "zimin.jpg"
        try:
            shutil.copy(test_image, target_path)
            logger.info(f"已复制测试图片到: {target_path}")
        except Exception as e:
            logger.error(f"复制测试图片失败: {e}")
    else:
        logger.info("未找到测试图片，需要手动准备基础图片")


async def download_default_resources(data_dir: Path) -> bool:
    """
    下载默认资源文件（如果需要从网络获取）
    
    Args:
        data_dir: 目标数据目录
        
    Returns:
        bool: 下载是否成功
    """
    # 这里可以添加从网络下载资源的逻辑
    # 例如：从GitHub或其他资源库下载基础图片和字体
    
    logger.info("下载默认资源功能暂未实现")
    logger.info("请手动准备以下文件:")
    logger.info(f"  1. 基础图片: {data_dir / 'zimin.jpg'}")
    logger.info(f"  2. 字体文件: {data_dir / 'simhei.ttf'}")
    
    
    return False