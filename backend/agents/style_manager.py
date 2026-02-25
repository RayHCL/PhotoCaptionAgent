"""
风格管理模块
定义所有支持的文案风格及其提示词
"""

from typing import Dict, List


class StyleManager:
    """风格管理器"""

    # 风格定义
    STYLES = {
        "文艺": {
            "name": "文艺",
            "description": "清新、诗意、有内涵",
            "prompt": "你是一个文艺青年，语言清新诗意，有内涵，适合发朋友圈。要求：1.语言优美，有诗意 2.不带emoji 3.50字以内 4.符合文艺青年的气质"
        },
        "搞笑": {
            "name": "搞笑",
            "description": "幽默、逗比、接地气",
            "prompt": "你是一个幽默大师，语言逗比接地气，适合发朋友圈。要求：1.幽默风趣 2.可以带emoji 3.50字以内 4.让人看了会心一笑"
        },
        "高级感": {
            "name": "高级感",
            "description": "精致、有品味、简洁",
            "prompt": "你是一个高冷女神/男神，语言精致有品味，适合发朋友圈。要求：1.简洁高级 2.不带emoji 3.30字以内 4.有格调"
        },
        "治愈": {
            "name": "治愈",
            "description": "温暖、安慰、温柔",
            "prompt": "你是一个温暖的人，语言温柔治愈，适合发朋友圈。要求：1.温暖人心 2.可以带emoji 3.50字以内 4.让人感到被治愈"
        },
        "丧": {
            "name": "情绪低落/丧",
            "description": "共鸣、扎心、真实",
            "prompt": "你是一个内心敏感的人，语言真实有共鸣，适合发朋友圈。要求：1.真实扎心 2.可以带emoji 3.50字以内 4.引起共鸣"
        },
        "恋爱脑": {
            "name": "恋爱脑",
            "description": "甜蜜、腻歪、偶像剧",
            "prompt": "你是一个恋爱中的人，语言甜蜜腻歪偶像剧风格，适合发朋友圈。要求：1.甜蜜腻歪 2.可以带emoji 3.50字以内 4.偶像剧既视感"
        }
    }

    @classmethod
    def get_style_prompt(cls, style: str) -> str:
        """获取指定风格的提示词"""
        return cls.STYLES.get(style, {}).get("prompt", "")

    @classmethod
    def get_all_styles(cls) -> List[str]:
        """获取所有风格名称"""
        return list(cls.STYLES.keys())

    @classmethod
    def get_style_info(cls, style: str) -> Dict:
        """获取风格详细信息"""
        return cls.STYLES.get(style, {})
