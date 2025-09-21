#!/bin/bash

# ZhaoLuSi.life 服务管理脚本
# 用于启动、停止、重启服务

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# 项目配置
PROJECT_NAME="zhaolusi"
PROJECT_DIR="/home/ubuntu/zhaolusi-web"
VENV_DIR="$PROJECT_DIR/venv"
SERVICE_NAME="zhaolusi.service"

# 函数定义
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# 检查是否以 root 运行
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "请使用 sudo 运行此脚本"
        exit 1
    fi
}

# 安装依赖
install_deps() {
    print_header "安装 Python 依赖"
    
    if [ ! -d "$VENV_DIR" ]; then
        print_status "创建虚拟环境..."
        sudo -u ubuntu python3 -m venv "$VENV_DIR"
    fi
    
    print_status "安装依赖包..."
    sudo -u ubuntu "$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/backend/requirements.txt"
    
    print_status "依赖安装完成"
}

# 配置 systemd 服务
setup_service() {
    print_header "配置 systemd 服务"
    
    # 复制服务文件
    cp "$PROJECT_DIR/deploy/zhaolusi.service" "/etc/systemd/system/"
    
    # 重载 systemd
    systemctl daemon-reload
    
    # 启用服务
    systemctl enable zhaolusi.service
    
    print_status "systemd 服务配置完成"
}

# 启动服务
start_service() {
    print_header "启动 ZhaoLuSi 服务"
    
    print_status "启动 Gunicorn 服务..."
    systemctl start zhaolusi.service
    
    sleep 2
    
    if systemctl is-active --quiet zhaolusi.service; then
        print_status "✓ Gunicorn 服务启动成功"
    else
        print_error "✗ Gunicorn 服务启动失败"
        systemctl status zhaolusi.service
        return 1
    fi
    
    print_status "重载 Nginx 配置..."
    systemctl reload nginx
    
    if systemctl is-active --quiet nginx; then
        print_status "✓ Nginx 重载成功"
    else
        print_error "✗ Nginx 重载失败"
        return 1
    fi
    
    print_status "等待服务稳定运行..."
    sleep 3
    
    print_status "服务启动完成"
    print_status "网站访问地址: https://zhaolusi.life"
}

# 一键启动（后台运行）
quick_start() {
    print_header "一键启动 ZhaoLuSi.life"
    
    start_service
    
    print_status "服务已在后台运行"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✓ ZhaoLuSi.life 已成功启动并运行在后台${NC}"
    echo -e "${GREEN}✓ 访问地址: https://zhaolusi.life${NC}"
    echo -e "${GREEN}✓ 后端 API: https://zhaolusi.life/api${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo
    echo -e "${YELLOW}常用管理命令:${NC}"
    echo "  停止服务: sudo $0 stop"
    echo "  重启服务: sudo $0 restart"
    echo "  查看状态: sudo $0 status"
    echo "  查看日志: sudo $0 logs system"
}

# 停止服务
stop_service() {
    print_header "停止 ZhaoLuSi 服务"
    
    print_status "停止 Gunicorn 服务..."
    systemctl stop zhaolusi.service
    
    print_status "服务已停止"
}

# 重启服务
restart_service() {
    print_header "重启 ZhaoLuSi 服务"
    
    print_status "重启 Gunicorn 服务..."
    systemctl restart zhaolusi.service
    
    sleep 2
    
    if systemctl is-active --quiet zhaolusi.service; then
        print_status "✓ 服务重启成功"
    else
        print_error "✗ 服务重启失败"
        systemctl status zhaolusi.service
        return 1
    fi
    
    print_status "重载 Nginx 配置..."
    systemctl reload nginx
    
    print_status "服务重启完成"
}

# 查看服务状态
status_service() {
    print_header "服务状态"
    
    echo -e "${BLUE}Gunicorn 服务状态:${NC}"
    systemctl status zhaolusi.service --no-pager
    
    echo -e "\n${BLUE}Nginx 服务状态:${NC}"
    systemctl status nginx --no-pager
    
    echo -e "\n${BLUE}最近的日志:${NC}"
    journalctl -u zhaolusi.service --no-pager -n 10
}

# 查看日志
logs_service() {
    print_header "查看服务日志"
    
    case "$2" in
        "access")
            tail -f /var/log/gunicorn/zhaolusi-access.log
            ;;
        "error")
            tail -f /var/log/gunicorn/zhaolusi-error.log
            ;;
        "nginx")
            tail -f /var/log/nginx/zhaolusi.access.log
            ;;
        "system")
            journalctl -u zhaolusi.service -f
            ;;
        *)
            echo "日志类型: access, error, nginx, system"
            echo "用法: $0 logs [access|error|nginx|system]"
            ;;
    esac
}

# 完整部署
deploy() {
    print_header "完整部署 ZhaoLuSi.life"
    
    install_deps
    setup_service
    start_service
    
    echo
    print_header "部署完成！"
    echo -e "${GREEN}网站地址: https://zhaolusi.life${NC}"
    echo -e "${YELLOW}管理命令:${NC}"
    echo "  启动: sudo $0 start"
    echo "  停止: sudo $0 stop"
    echo "  重启: sudo $0 restart"
    echo "  状态: sudo $0 status"
    echo "  日志: sudo $0 logs [access|error|nginx|system]"
}

# 主函数
main() {
    case "$1" in
        "install")
            check_root
            install_deps
            ;;
        "setup")
            check_root
            setup_service
            ;;
        "start")
            check_root
            quick_start
            ;;
        "stop")
            check_root
            stop_service
            ;;
        "restart")
            check_root
            restart_service
            ;;
        "status")
            status_service
            ;;
        "logs")
            logs_service "$@"
            ;;
        "deploy")
            check_root
            deploy
            ;;
        "auto-start")
            check_root
            setup_service
            print_status "✓ 开机自启动已配置"
            ;;
        *)
            echo "ZhaoLuSi.life 服务管理脚本"
            echo
            echo "用法: $0 {install|setup|start|stop|restart|status|logs|deploy|auto-start}"
            echo
            echo "命令说明:"
            echo "  install    - 安装 Python 依赖"
            echo "  setup      - 配置 systemd 服务"
            echo "  start      - 一键启动（后台运行）"
            echo "  stop       - 停止服务"
            echo "  restart    - 重启服务"
            echo "  status     - 查看服务状态"
            echo "  logs       - 查看日志 [access|error|nginx|system]"
            echo "  deploy     - 完整部署（推荐首次使用）"
            echo "  auto-start - 配置开机自启动"
            echo
            echo "快速使用："
            echo "  首次部署: sudo $0 deploy"
            echo "  一键启动: sudo $0 start"
            echo
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"