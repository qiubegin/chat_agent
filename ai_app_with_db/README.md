# AI 应用平台

一个基于 Streamlit + SQLite + Ollama 的简易 AI 对话应用，支持用户注册、登录、聊天记录持久化、流式输出。

## 功能特性
- 用户注册 / 登录（密码哈希存储）
- 多模型选择（qwen2.5:0.5b / 7b / 9b）
- 流式对话输出（打字机效果）
- 聊天记录保存到数据库
- 历史记录查询
- 导出对话记录

## 快速开始

### 1. 克隆项目
git clone https://gitee.com/qiu-begin/python-ai-learning.git
cd employment/projects/ai_app_with_db

### 2. 安装依赖
pip install -r requirements.txt

### 3. 初始化数据库
python -c "from utils.db import init_db; init_db()"

### 4. 启动应用
streamlit run app.py

### 项目结构
ai_app_with_db/
├── app.py              # 主入口
├── pages/              # 页面目录
│   ├── login.py        # 用户登录
│   ├── register.py     # 用户注册
│   ├── chat.py         # AI 对话
│   └── history.py      # 历史记录
├── utils/              # 工具模块
│   ├── db.py           # 数据库操作
│   └── auth.py         # 密码哈希
├── app.db              # SQLite 数据库（自动生成）
├── requirements.txt    # 项目依赖
└── README.md           # 项目说明
### 技术栈
Streamlit：前端界面
SQLite：数据持久化
Ollama：本地大模型
Python：业务逻辑
### 后续计划
支持对话搜索
增加模型使用统计
支持多用户并发

## 在线体验
- 部署地址：[http://120.78.72.2:8501](http://120.78.72.2:8501)
- 可直接注册体验，模型调用基于本地 Ollama (deepseek-r1:1.5b / qwen2.5:0.5b)
todo:开发完善中
```bash