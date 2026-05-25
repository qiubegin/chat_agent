#!/bin/bash
# AI 应用平台一键部署脚本
# 使用方法: chmod +x deploy.sh && ./deploy.sh

set -e

echo "========================================="
echo "AI 应用平台 Docker 部署脚本"
echo "========================================="

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查 Ollama 容器是否运行
if ! docker ps | grep -q ollama; then
    echo "警告: Ollama 容器未运行"
    echo "请先启动 Ollama: docker run -d --name ollama -p 11434:11434 ollama/ollama"
    echo "然后拉取模型: docker exec ollama ollama pull deepseek-r1:1.5b"
    read -p "是否继续部署？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 创建数据目录
mkdir -p data

# 构建镜像
echo "正在构建 Docker 镜像..."
docker build -t ai_app .

# 停止并删除旧容器
if docker ps -a | grep -q ai_app; then
    echo "停止并删除旧容器..."
    docker stop ai_app 2>/dev/null
    docker rm ai_app 2>/dev/null
fi

# 运行新容器
echo "启动新容器..."
docker run -d \
  --name ai_app \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  --link ollama:ollama \
  -e OLLAMA_HOST=http://ollama:11434 \
  --restart always \
  ai_app

echo "========================================="
echo "部署完成！"
echo "访问地址: http://localhost:8501"
echo "查看日志: docker logs -f ai_app"
echo "========================================="