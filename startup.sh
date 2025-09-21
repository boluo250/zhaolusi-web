#!/bin/bash

# ZhaoLuSi.life 一键启动脚本
# 快速启动前后端服务

# 颜色定义
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}🚀 启动 ZhaoLuSi.life...${NC}"

# 使用 manage.sh 启动
sudo /home/ubuntu/zhaolusi-web/manage.sh start