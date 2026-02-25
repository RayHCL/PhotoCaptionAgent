"""
PhotoCaptionAgent 后端服务
"""
import os
import sys
from pathlib import Path
from typing import List

# 将当前目录添加到 sys.path
sys.path.insert(0, str(Path(__file__).parent))
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.image_analyzer import ImageAnalyzer
from agents.caption_generator import CaptionGenerator
from agents.style_manager import StyleManager
from utils.image_processor import validate_image, resize_image_if_needed

# 创建 FastAPI 应用
app = FastAPI(title="PhotoCaptionAgent", description="朋友圈文案生成工具")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 数据模型
class CaptionRequest(BaseModel):
    styles: List[str]
    emoji: bool = True


class CaptionResult(BaseModel):
    image_summary: str
    captions: dict  # {风格: [文案列表]}


# 初始化 Agent
image_analyzer = ImageAnalyzer()
caption_generator = CaptionGenerator()


@app.get("/")
async def root():
    """根路径"""
    return {"message": "PhotoCaptionAgent API", "version": "1.0.0"}


@app.get("/api/styles")
async def get_styles():
    """获取所有支持的文案风格"""
    styles = []
    for key, value in StyleManager.STYLES.items():
        styles.append({
            "key": key,
            "name": value["name"],
            "description": value["description"]
        })
    return {"styles": styles}


@app.post("/api/generate/caption")
async def generate_caption(
    image: UploadFile = File(...),
    styles: str = Form(...),
    emoji: bool = Form(True)
):
    """
    生成文案接口

    Args:
        image: 上传的图片文件
        styles: 文案风格列表（JSON 字符串）
        emoji: 是否使用 emoji

    Returns:
        image_summary: 图片分析结果
        captions: 按风格分类的文案列表
    """
    import json

    # 验证文件类型
    if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(status_code=400, detail="仅支持 JPG/PNG 格式图片")

    # 读取图片内容
    image_content = await image.read()

    # 验证图片
    if not validate_image(image_content):
        raise HTTPException(status_code=400, detail="无效的图片文件")

    # 尝试压缩大图
    image_content = resize_image_if_needed(image_content)

    # 解析风格列表
    try:
        style_list = json.loads(styles)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="无效的风格格式")

    if not style_list:
        raise HTTPException(status_code=400, detail="请至少选择一个风格")

    # 验证风格
    valid_styles = StyleManager.get_all_styles()
    for style in style_list:
        if style not in valid_styles:
            raise HTTPException(status_code=400, detail=f"不支持的风格: {style}")

    try:
        # 1. 分析图片
        image_summary = image_analyzer.analyze(image_content)
        summary = image_summary.get("image_summary", "")

        # 2. 为每个风格生成文案
        result_captions = {}
        for style in style_list:
            captions = caption_generator.generate(
                image_content=image_content,
                image_summary=summary,
                style=style,
                emoji_enabled=emoji
            )
            result_captions[style] = captions

        return {
            "image_summary": summary,
            "captions": result_captions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
