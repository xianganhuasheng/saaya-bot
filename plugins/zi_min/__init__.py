from pathlib import Path
from nonebot import get_plugin_config, get_driver, on_command
from nonebot.exception import MatcherException
from nonebot.params import CommandArg
from nonebot.adapters.satori import MessageEvent, Message
from nonebot.log import logger
import nonebot_plugin_localstore as localstore  # noqa: E402

from utils import PassiveGenerator

# 导入模块化组件
from .config import Config
from .utils import ensure_dirs_exist, read_image_bytes, image_to_message
from .service import ZMinService
from .initialize import initialize_resources


# 获取配置
plugin_config = get_plugin_config(Config)

# 获取插件目录作为资源路径
# todo: 暂时将图片和ttf字体文件放在插件目录，后续传服务器上实时获取
# plugin_dir = localstore.get_data_dir("zi_min") ###不要删除这段注释###
plugin_dir = Path(__file__).parent
data_dir = plugin_dir  # 直接使用插件目录作为数据目录
cache_dir = localstore.get_cache_dir("zi_min")

# 确保资源目录存在
ensure_dirs_exist(data_dir, cache_dir)

# 颜色元组
text_color = (plugin_config.text_color_r, 
              plugin_config.text_color_g, 
              plugin_config.text_color_b)

# 初始化服务
service = ZMinService(
    data_dir=data_dir,
    base_image_filename=plugin_config.base_image_filename,
    font_filename=plugin_config.font_filename,
    font_size=plugin_config.font_size,
    text_color=text_color,
    max_text_length=plugin_config.max_text_length
)


# 注册命令
if plugin_config.enable_zi_min:
    logger.info("籽岷插件启动")
    zmin = on_command(
        "zi_min", 
        aliases={"籽岷", "zimin", "zm"}, 
        priority=10, 
        block=True
    )
    
    @zmin.handle()
    async def handle_zmin(event: MessageEvent, args: Message = CommandArg()):
        """处理籽岷命令"""
        arg_text = args.extract_plain_text().strip()
        passive_generator = PassiveGenerator(event)
        
        if not arg_text:
            await zmin.finish(
                "用法：/zimin <左侧文字> <中间文字> <右侧文字>\n"
                "示例：/zimin 当破即破！ 当断即断！ ?!当当!?\n"
                "注意：每个文字不要超过15个字符"
                + passive_generator.element
            )
        
        # 简单的参数分割（按空格分割，不考虑引号）
        parts = arg_text.split()
        if len(parts) != 3:
            await zmin.finish(
                "请提供三个文字参数，用空格分隔\n"
                "示例：/zimin 左侧 中间 右侧"
                + passive_generator.element
            )
        
        text_left, text_middle, text_right = parts
        
        try:
            # 生成图片
            output_path = await service.generate_zmin_image(
                text_left, text_middle, text_right, cache_dir
            )
            
            if not output_path or not output_path.exists():
                await zmin.finish(
                    "生成图片失败，请检查资源文件是否完整"
                    + passive_generator.element
                )
            
            # 读取图片字节数据并发送
            image_bytes = read_image_bytes(output_path)
            if not image_bytes:
                await zmin.finish(
                    "读取生成的图片失败" + passive_generator.element
                )
            
            # 发送图片，使用PNG格式
            image_message = image_to_message(image_bytes, "image/png")
            
            # 直接使用+操作符组合消息，与其他插件保持一致
            # 参考blackjack插件中的用法：HELP_MESSAGE + gens[latest_message_id].element
            await zmin.finish(image_message + passive_generator.element)
        
        except MatcherException:
            raise

        except ValueError as e:
            await zmin.finish(
                f"输入错误: {str(e)}" + passive_generator.element
            )
        except Exception as e:
            logger.error(f"生成籽岷图片时出错: {e}", exc_info=True)
            await zmin.finish(
                "生成图片时出现未知错误" + passive_generator.element
            )


# 可选：初始化资源
@get_driver().on_startup
async def init_resources():
    """初始化资源文件"""
    await initialize_resources(data_dir, cache_dir)
    logger.info("籽岷插件资源初始化完成")