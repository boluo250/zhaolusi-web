#!/bin/bash

# ZhaoLuSi.life Nginx 配置部署脚本
# 适配现有 Nginx 环境

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== ZhaoLuSi.life Nginx 配置部署 ===${NC}"

# 检查是否以 root 运行
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}请使用 sudo 运行此脚本${NC}"
   exit 1
fi

# 1. 复制配置文件到 sites-available
echo -e "${GREEN}[1/6]${NC} 复制配置文件..."
cp /home/ubuntu/zhaolusi-web/nginx/zhaolusi /etc/nginx/sites-available/zhaolusi
echo "配置文件已复制到 /etc/nginx/sites-available/zhaolusi"

# 2. 创建符号链接启用站点
echo -e "${GREEN}[2/6]${NC} 启用站点配置..."
if [ ! -L /etc/nginx/sites-enabled/zhaolusi ]; then
    ln -s /etc/nginx/sites-available/zhaolusi /etc/nginx/sites-enabled/zhaolusi
    echo "已创建符号链接：/etc/nginx/sites-enabled/zhaolusi"
else
    echo "符号链接已存在"
fi

# 3. 测试 Nginx 配置
echo -e "${GREEN}[3/6]${NC} 测试 Nginx 配置..."
if nginx -t; then
    echo -e "${GREEN}✓ Nginx 配置测试通过${NC}"
else
    echo -e "${RED}✗ Nginx 配置测试失败${NC}"
    exit 1
fi

# 4. 创建项目目录结构
echo -e "${GREEN}[4/6]${NC} 创建项目目录..."
mkdir -p /home/ubuntu/zhaolusi-web/frontend
mkdir -p /home/ubuntu/zhaolusi-web/media

# 确保权限正确
chown -R ubuntu:ubuntu /home/ubuntu/zhaolusi-web
echo "项目目录结构已创建"

# 5. 获取 SSL 证书（如果不存在）
echo -e "${GREEN}[5/6]${NC} 检查 SSL 证书..."
if [ ! -d "/etc/letsencrypt/live/zhaolusi.life" ]; then
    echo -e "${YELLOW}SSL 证书不存在，正在获取...${NC}"
    echo -e "${YELLOW}确保域名 zhaolusi.life 已指向此服务器${NC}"
    echo "按 Enter 继续，或 Ctrl+C 取消..."
    read -r
    
    certbot --nginx -d zhaolusi.life -d www.zhaolusi.life \
        --email your-email@example.com \
        --agree-tos \
        --no-eff-email \
        --redirect
    
    echo -e "${GREEN}✓ SSL 证书获取成功${NC}"
else
    echo -e "${GREEN}✓ SSL 证书已存在${NC}"
fi

# 6. 重载 Nginx 配置
echo -e "${GREEN}[6/6]${NC} 重载 Nginx 配置..."
systemctl reload nginx

if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓ Nginx 重载成功${NC}"
else
    echo -e "${RED}✗ Nginx 重载失败${NC}"
    systemctl status nginx
    exit 1
fi

# 显示部署结果
echo
echo -e "${GREEN}=== 部署完成！ ===${NC}"
echo -e "${GREEN}网站地址：${NC}"
echo "  • https://zhaolusi.life"
echo "  • https://www.zhaolusi.life"
echo
echo -e "${YELLOW}接下来的步骤：${NC}"
echo "1. 确保 FastAPI 后端在端口 8001 运行"
echo "2. 将前端文件复制到 /home/ubuntu/zhaolusi-web/frontend/"
echo "3. 将媒体文件复制到 /home/ubuntu/zhaolusi-web/media/"
echo "4. 测试网站功能"
echo
echo -e "${YELLOW}有用的命令：${NC}"
echo "• 查看 Nginx 状态: systemctl status nginx"
echo "• 查看访问日志: tail -f /var/log/nginx/zhaolusi.access.log"
echo "• 查看错误日志: tail -f /var/log/nginx/zhaolusi.error.log"
echo "• 测试配置: nginx -t"
echo "• 重载配置: systemctl reload nginx"