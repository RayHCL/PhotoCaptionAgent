"""
阿里云百炼 API 客户端
"""
import os
import json
from typing import Dict, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()


class DashScopeClient:
    """百炼 API 客户端"""

    # API URL - 使用正确的端点
    BASE_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY", "")

    def chat_with_image(
        self,
        image_base64: str,
        image_mime_type: str,
        prompt: str,
        model: str = "qwen-vl-plus"
    ) -> str:
        """
        调用多模态模型进行图片理解

        Args:
            image_base64: base64 编码的图片
            image_mime_type: 图片 MIME 类型
            prompt: 提示词
            model: 模型名称

        Returns:
            模型回复内容
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "disable"
        }

        # 构造请求消息
        messages = [
            {
                "role": "user",
                "content": [
                    {"image": f"data:{image_mime_type};base64,{image_base64}"},
                    {"text": prompt}
                ]
            }
        ]

        payload = {
            "model": model,
            "input": {
                "messages": messages
            },
            "parameters": {
                "result_format": "message"
            }
        }

        print(f"Calling DashScope API with model: {model}")
        print(f"API URL: {self.BASE_URL}")

        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                self.BASE_URL,
                headers=headers,
                json=payload
            )

            # 打印响应信息
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text[:500]}")

            # 如果请求失败，打印详细信息
            if response.status_code != 200:
                print(f"DashScope API Error: {response.status_code}")
                response.raise_for_status()

            result = response.json()

            if "output" in result and "choices" in result["output"]:
                return result["output"]["choices"][0]["message"]["content"][0]["text"]

            return str(result)
