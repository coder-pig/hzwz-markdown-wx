#!/bin/bash

# 确保脚本抛出遇到的错误
set -e

echo "🚀 开始更新项目..."

# 1. 拉取最新代码
echo "📥 正在拉取最新代码 (git pull)..."
git pull

# 2. 重建并重启容器
# --build: 确保如果 Dockerfile 或依赖变了，会重新构建镜像
# -d: 后台运行
echo "🔄 正在重建并重启服务..."
docker compose up -d --build

# 3. 清理无用的旧镜像 (可选，节省磁盘空间)
echo "🧹 清理旧镜像..."
docker image prune -f

echo "✅ 更新完成！"
