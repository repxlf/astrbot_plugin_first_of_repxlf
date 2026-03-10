from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

@register("Repxlf's Kogasa", "Repxlf", "一个简单的 Hello Forgotten World 插件", "1.0.2")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。aaaa"""

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

        url = "http://59.110.46.232/images/-2.jpg"

        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGB")

        draw = ImageDraw.Draw(img)

        # 白板区域
        board_x1 = 550
        board_y1 = 180
        board_x2 = 850
        board_y2 = 420

        board_width = board_x2 - board_x1
        board_height = board_y2 - board_y1

        # 如果为空则直接返回空白
        if not text:
            output_path = "whiteboard_result.png"
            img.save(output_path)
            yield event.image_result(output_path)
            return

        font_size = 100
        best_lines = []
        best_font = None

        while font_size > 10:

            font = ImageFont.truetype("DejaVuSans.ttf", font_size)

            lines = []
            current_line = ""

            for char in text:

                test_line = current_line + char
                bbox = draw.textbbox((0, 0), test_line, font=font)
                test_width = bbox[2] - bbox[0]

                if test_width <= board_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = char

            if current_line:
                lines.append(current_line)

            # 计算总高度
            bbox = draw.textbbox((0, 0), "测试", font=font)
            line_height = (bbox[3] - bbox[1]) + 5

            total_height = line_height * len(lines)

            if total_height <= board_height:
                best_lines = lines
                best_font = font
                break

            font_size -= 2

        if not best_lines:
            best_lines = [text]
            best_font = ImageFont.truetype("DejaVuSans.ttf", 10)

        # 重新计算高度用于垂直居中
        bbox = draw.textbbox((0, 0), "测试", font=best_font)
        line_height = (bbox[3] - bbox[1]) + 5

        total_height = line_height * len(best_lines)

        y = board_y1 + (board_height - total_height) // 2

        for line in best_lines:

            bbox = draw.textbbox((0, 0), line, font=best_font)
            line_width = bbox[2] - bbox[0]

            x = board_x1 + (board_width - line_width) // 2

            draw.text((x, y), line, font=best_font, fill=(68,144,206))

            y += line_height

        output_path = "whiteboard_result.png"
        img.save(output_path)

        yield event.image_result(output_path)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
