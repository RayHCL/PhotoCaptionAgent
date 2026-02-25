"""
图片理解 Agent
分析图片内容，提取场景、情绪、关键词等信息
"""
from typing import Dict
from utils.dashscope_client import DashScopeClient
from utils.image_processor import image_to_base64, get_image_mime_type


class ImageAnalyzer:
    """图片理解 Agent"""

    # 图片分析提示词模板
    ANALYSIS_PROMPT = """请仔细分析这张图片，提取以下信息：
1. 场景：图片拍摄的场景是什么？（如：海边日落、咖啡馆、城市街道等）
2. 人物：图片中有什么人物？他们的状态如何？（如：独自一人、情侣、朋友聚会等）
3. 情绪/氛围：图片整体传递出什么情绪？（如：浪漫、安静、热闹、治愈等）
4. 关键词：3-5个描述这张图片的关键词

请用简洁的语言描述以上信息，总字数控制在100字以内。"""

    def __init__(self):
        self.client = DashScopeClient()

    def analyze(self, image_content: bytes) -> Dict[str, str]:
        """
        分析图片内容

        Args:
            image_content: 图片二进制内容

        Returns:
            包含场景、人物、情绪、关键词的字典
        """
        image_base64 = image_to_base64(image_content)
        image_mime = get_image_mime_type(image_content)

        result = self.client.chat_with_image(
            image_base64=image_base64,
            image_mime_type=image_mime,
            prompt=self.ANALYSIS_PROMPT
        )

        return {
            "image_summary": result
        }
