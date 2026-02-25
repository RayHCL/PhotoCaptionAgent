"""
文案生成 Agent
根据图片信息和风格生成朋友圈文案
"""
from typing import List, Dict
from utils.dashscope_client import DashScopeClient
from utils.image_processor import image_to_base64, get_image_mime_type
from agents.style_manager import StyleManager


class CaptionGenerator:
    """文案生成 Agent"""

    # 文案生成提示词模板
    def __init__(self):
        self.client = DashScopeClient()

    def generate(
        self,
        image_content: bytes,
        image_summary: str,
        style: str,
        emoji_enabled: bool = True
    ) -> List[str]:
        """
        根据图片信息和风格生成文案

        Args:
            image_content: 图片二进制内容
            image_summary: 图片分析结果
            style: 文案风格
            emoji_enabled: 是否使用 emoji

        Returns:
            生成的文案列表
        """
        style_info = StyleManager.get_style_info(style)
        base_prompt = style_info.get("prompt", "")

        # 构建完整提示词
        emoji_instruction = "可以正常使用 emoji" if emoji_enabled else "不要使用任何 emoji"

        prompt = f"""图片内容分析：{image_summary}

请根据以上图片内容，生成3条适合微信朋友圈的文案。

要求：
1. 风格：{style_info.get('description', style)}
2. 语言风格：{base_prompt}
3. emoji：{emoji_instruction}
4. 每条文案20-50字
5. 每条文案单独一行，用序号1.2.3.开头

生成的文案："""

        image_base64 = image_to_base64(image_content)
        image_mime = get_image_mime_type(image_content)

        result = self.client.chat_with_image(
            image_base64=image_base64,
            image_mime_type=image_mime,
            prompt=prompt
        )

        # 解析结果
        captions = []
        for line in result.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('.')):
                # 去掉序号
                clean_line = line.lstrip('0123456789.').strip()
                if clean_line:
                    captions.append(clean_line)

        # 如果解析失败，直接返回原始结果
        if not captions:
            captions = [result]

        return captions[:3]  # 最多返回3条
