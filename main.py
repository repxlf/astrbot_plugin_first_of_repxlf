from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from PIL import Image, ImageDraw, ImageFont
import requests
import math
import os
from io import BytesIO

@register("Repxlf's Kogasa", "Repxlf", "一个简单的 Hello ForgottenWorld 插件", "1.1.0")
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
    async def whiteboard(self, event: AstrMessageEvent, text: str = ""):
        '''
        举白板插件
        使用方法：
        /举白板 内容
        '''

        logger.info("触发举白板指令")

        url = "http://59.110.46.232/images/-2.jpg"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGB")

        if not text or text.strip() == "":
            output_path = "whiteboard_result.png"
            img.save(output_path)
            yield event.image_result(output_path)
            return

        draw = ImageDraw.Draw(img)

        board_x1 = 550
        board_y1 = 180
        board_x2 = 850
        board_y2 = 420

        board_width = board_x2 - board_x1
        board_height = board_y2 - board_y1

        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(plugin_dir, "NotoSansSChineseMedium-7.ttf")

        # --- 初始文本 ---
        original_text = text

        # 定义一个函数封装自适应渲染逻辑，方便重复调用
        def adapt_text(text_to_render):
            nonlocal draw, board_width, board_height, font_path

            # 单行特判
            max_font_size = board_height - 20
            font_size = max_font_size
            single_line_font = None
            bbox_width, bbox_height = 0, 0

            while font_size > 10:
                font = ImageFont.truetype(font_path, font_size)
                bbox = draw.textbbox((0, 0), text_to_render, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                if text_width <= board_width and text_height <= board_height:
                    single_line_font = font
                    bbox_width = text_width
                    bbox_height = text_height
                    break
                font_size -= 1

            if single_line_font and (bbox_width / bbox_height < 3.5):
                best_lines = [text_to_render]
                best_font = single_line_font
                line_height = bbox_height + 5
                return best_lines, best_font, line_height

            # 多行自适应逻辑
            font_size = board_height - 20
            best_lines = []
            best_font = None

            while font_size > 10:
                font = ImageFont.truetype(font_path, font_size)
                bbox = draw.textbbox((0, 0), "测试", font=font)
                line_height = (bbox[3] - bbox[1]) + 5
                max_lines = board_height // line_height
                max_lines = max(1, max_lines)

                lines = []
                start = 0
                text_len = len(text_to_render)
                for i in range(max_lines):
                    remaining_lines = max_lines - i
                    remaining_chars = text_len - start
                    chars_this_line = (remaining_chars + remaining_lines - 1) // remaining_lines
                    lines.append(text_to_render[start:start+chars_this_line])
                    start += chars_this_line
                    if start >= text_len:
                        break

                fits_width = True
                for line in lines:
                    line_bbox = draw.textbbox((0,0), line, font=font)
                    line_width = line_bbox[2] - line_bbox[0]
                    if line_width > board_width:
                        fits_width = False
                        break

                if fits_width:
                    best_lines = lines
                    best_font = font
                    break

                font_size -= 2

            if not best_lines:
                return None, None, None  # 无法渲染

            return best_lines, best_font, line_height

        # --- 尝试渲染原文本 ---
        best_lines, best_font, line_height = adapt_text(original_text)

        # --- 安全保险 ---
        if best_lines is None:
            # 原文本太长，替换为提示文本重新渲染
            fallback_text = "你的话太多了。"
            best_lines, best_font, line_height = adapt_text(fallback_text)

        # --- 渲染 ---
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

    @filter.command("早苗说")
    async def sanae_say(self, event: AstrMessageEvent, text: str = ""):
        """
        早苗说插件
        使用方法：
        /早苗说 内容
        """

        logger.info("触发早苗说指令")

        SCALE = 4  # 整体放大倍数

        # 1 空输入处理
        if not text or text.strip() == "":
            text = "什么都不说是等着老娘向你表白吗？"

        # 下载ABC图片
        url_A = "http://59.110.46.232/images/-3.jpg"
        url_B = "http://59.110.46.232/images/-4.jpg"
        url_C = "http://59.110.46.232/images/-5.jpg"

        img_A = Image.open(BytesIO(requests.get(url_A).content)).convert("RGB")
        img_B = Image.open(BytesIO(requests.get(url_B).content)).convert("RGB")
        img_C = Image.open(BytesIO(requests.get(url_C).content)).convert("RGB")

        # 放大图片
        img_A = img_A.resize((img_A.width * SCALE, img_A.height * SCALE), Image.NEAREST)
        img_B = img_B.resize((img_B.width * SCALE, img_B.height * SCALE), Image.NEAREST)
        img_C = img_C.resize((img_C.width * SCALE, img_C.height * SCALE), Image.NEAREST)

        # 尺寸（同步放大）
        height = 56 * SCALE
        A_width = 46 * SCALE
        B_width = 13 * SCALE
        C_width = 5 * SCALE

        # 字体
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(plugin_dir, "unifont-15.0.06.ttf")

        font_size = 12 * SCALE
        font = ImageFont.truetype(font_path, font_size)

        # 用于测量文字
        temp_img = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(temp_img)

        bbox = draw.textbbox((0, 0), text, font=font)
        raw_text_width = bbox[2] - bbox[0]

        # 2 字符间距改为 8px
        spacing = 8
        char_count = len(text)

        text_width = raw_text_width + spacing * (char_count - 1 if char_count > 1 else 0)

        # 4 输入过长限制（250px → 1000px）
        if text_width > 250 * SCALE:
            text = "啰啰嗦嗦不就是喜欢我嘛，我也喜欢你"
            bbox = draw.textbbox((0, 0), text, font=font)
            raw_text_width = bbox[2] - bbox[0]
            char_count = len(text)
            text_width = raw_text_width + spacing * (char_count - 1 if char_count > 1 else 0)

        # 根据文本宽度决定B数量
        padding = 10 * SCALE
        needed_width = text_width + padding

        repeat = math.ceil(needed_width / B_width)
        repeat = max(1, repeat)

        # 创建新图
        new_width = A_width + repeat * B_width + C_width
        img = Image.new("RGB", (new_width, height))

        # 拼接ABC
        x = 0
        img.paste(img_A, (x, 0))
        x += A_width

        for _ in range(repeat):
            img.paste(img_B, (x, 0))
            x += B_width

        img.paste(img_C, (x, 0))

        draw = ImageDraw.Draw(img)

        # B区域
        text_area_left = A_width
        text_area_right = A_width + repeat * B_width
        text_area_width = text_area_right - text_area_left

        # 居中
        text_x = text_area_left + (text_area_width - text_width) // 2

        # y轴 13~23 → 放大
        text_height = bbox[3] - bbox[1]
        text_y = (13 * SCALE) + ((10 * SCALE - text_height) // 2)

        # 逐字绘制（实现8px间距）
        x_cursor = text_x
        for ch in text:
            draw.text((x_cursor, text_y), ch, font=font, fill=(0, 0, 0))
            ch_bbox = draw.textbbox((0, 0), ch, font=font)
            ch_width = ch_bbox[2] - ch_bbox[0]
            x_cursor += ch_width + spacing

        output_path = "sanae_say.png"
        img.save(output_path)

        yield event.image_result(output_path)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
