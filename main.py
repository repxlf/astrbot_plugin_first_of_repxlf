from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from PIL import Image, ImageDraw, ImageFont
import requests
import os
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
    async def whiteboard(self, event: AstrMessageEvent, text: str = ""):
        import requests
        from PIL import Image, ImageDraw, ImageFont
        from io import BytesIO
        import math

        # 图片URL（替换成你的模板地址）
        url = "http://59.110.46.232/images/-2.jpg"

        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGB")

        # 如果内容为空，直接发送空白板
        if text is None or text.strip() == "":
            output = "whiteboard_result.png"
            img.save(output)
            yield event.image_result(output)
            return

        draw = ImageDraw.Draw(img)

        # 白板区域
        x1, y1 = 550, 180
        x2, y2 = 850, 420

        width = x2 - x1
        height = y2 - y1

        # 字体颜色
        color = (68,144,206)

        # 字体
        font_path = os.path.join(os.path.dirname(__file__), "msyh.ttc")

        text = text.strip()

        # ======================
        # 自动分行
        # ======================

        total_chars = len(text)

        chars_per_line = math.ceil(math.sqrt(total_chars))

        lines = []

        for i in range(0, total_chars, chars_per_line):
            lines.append(text[i:i+chars_per_line])

        line_count = len(lines)

        # ======================
        # 自动字体大小
        # ======================

        font_size = 120

        while font_size > 10:

            font = ImageFont.truetype(font_path, font_size)

            max_width = 0
            total_height = 0

            for line in lines:

                bbox = draw.textbbox((0,0), line, font=font)

                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]

                if w > max_width:
                    max_width = w

                total_height += h

            line_spacing = int(font_size * 0.3)
            total_height += (line_count - 1) * line_spacing

            if max_width <= width and total_height <= height:
                break

            font_size -= 2

        # ======================
        # 计算居中
        # ======================

        start_y = y1 + (height - total_height) // 2
        y = start_y

        # ======================
        # 绘制每一行
        # ======================

        for line in lines:

            bbox = draw.textbbox((0,0), line, font=font)

            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]

            x = x1 + (width - w) // 2

            draw.text(
                (x, y),
                line,
                font=font,
                fill=color
            )

            y += h + int(font_size * 0.3)

        output = "whiteboard_result.png"
        img.save(output)

        yield event.image_result(output)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
