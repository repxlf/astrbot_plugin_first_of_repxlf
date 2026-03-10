from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    """@filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息
        """
    
    @filter.command("举白板")
    async def whiteboard(self, event: AstrMessageEvent, text: str):
        '''
        举白板插件
        使用方法：
        /举白板 内容
        '''

        logger.info("触发举白板指令")

        # 模板图片URL
        url = "http://59.110.46.232/images/-2.jpg"

        # 下载图片
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGB")

        draw = ImageDraw.Draw(img)
    
        # 白板区域（需要根据你的图片调整）
        board_x1 = 0
        board_y1 = 0
        board_x2 = 200
        board_y2 = 200

        board_width = board_x2 - board_x1
        board_height = board_y2 - board_y1

        # 自动调整字体大小
        font_size = 100
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)

        while font_size > 10:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
            bbox = draw.textbbox((0, 0), text, font=font)

            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            if text_width <= board_width and text_height <= board_height:
                break

            font_size -= 2

        # 计算文字居中位置
        x = board_x1 + (board_width - text_width) // 2
        y = board_y1 + (board_height - text_height) // 2

        # 写入文字（蓝色）
        draw.text((x, y), text, font=font, fill=(0, 0, 255))

        # 保存图片
        output_path = "whiteboard_result.png"
        img.save(output_path)

        # 发送图片
        yield event.image_result(output_path)
        

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
