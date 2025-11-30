# model_adapter.py
from typing import Optional
from io import BytesIO


class Text2ImageModel:
    """
    占位封装：
    - 你可以用 diffusers 本地加载 SD 模型
    - 或在这里发 HTTP 请求到你自己的推理服务
    """

    def __init__(self):
        # TODO: 在这里初始化 Stable Diffusion / SDXL 等模型
        # 例如: 从 Hugging Face 加载权重，或设置推理服务 URL
        self.initialized = False

    def generate(self, prompt: str, negative_prompt: Optional[str] = None) -> BytesIO:
        """
        根据文本生成图片，返回 BytesIO(PNG)
        """
        # TODO: 替换为真实推理逻辑
        # 这里先抛异常，提醒你实现
        raise NotImplementedError(
            "请在 model_adapter.Text2ImageModel.generate 中接入你选定的开源文生图模型"
        )


# 单例
model = Text2ImageModel()
