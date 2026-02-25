# PhotoCaptionAgent

一个基于 AI 的朋友圈图片文案生成工具。用户上传图片后，系统会自动分析图片内容，并生成多种风格的朋友圈文案。

## 功能特性

- 图片上传（支持 JPG/PNG 格式）
- 拖拽或点击上传
- 6 种文案风格可选：文艺、搞笑、高级感、治愈、丧、恋爱脑
- 支持 emoji 开关
- 一键复制文案

## 技术栈

### 后端
- Python 3.12+
- FastAPI
- 阿里云百炼（通义千问 VL 多模态模型）

### 前端
- Vue 3
- Vite
- Element Plus
- Axios

## 项目结构

```
PhotoCaptionAgent/
├── backend/                 # 后端服务
│   ├── main.py              # FastAPI 入口
│   ├── agents/              # AI Agent 模块
│   │   ├── image_analyzer.py
│   │   ├── caption_generator.py
│   │   └── style_manager.py
│   ├── utils/               # 工具模块
│   │   ├── dashscope_client.py
│   │   └── image_processor.py
│   └── .env                 # 环境变量
└── frontend/                # 前端应用
    ├── src/
    │   ├── App.vue
    │   ├── api/
    │   └── components/
    └── package.json
```

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd PhotoCaptionAgent
```

### 2. 后端配置

```bash
cd backend

# 创建虚拟环境
uv venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
uv pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的阿里云百炼 API Key
# 获取 API Key: https://dashscope.console.aliyun.com/

# 启动后端
uvicorn main:app --reload
```

后端服务将在 http://localhost:8000 运行

### 3. 前端配置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 http://localhost:3000 运行

### 4. 使用

1. 打开浏览器访问 http://localhost:3000
2. 上传一张图片
3. 选择想要的文案风格
4. 点击"生成文案"按钮
5. 复制喜欢的文案

## API 接口

### 获取支持的风格列表
```
GET /api/styles
```

### 生成文案
```
POST /api/generate/caption

参数:
- image: 图片文件
- styles: 风格列表 (JSON 数组)
- emoji: 是否使用 emoji (布尔值)
```

## 许可证

MIT License
