#!/bin/bash

# 设置错误时退出
set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "未找到命令: $1"
        return 1
    fi
    return 0
}

# 检查并安装 Node.js
check_and_install_node() {
    if ! check_command node || ! check_command npm; then
        log_info "正在安装 Node.js..."
        
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if check_command apt-get; then
                # Debian/Ubuntu
                curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
                sudo apt-get install -y nodejs
            elif check_command yum; then
                # CentOS/RHEL
                curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
                sudo yum install -y nodejs
            else
                log_error "不支持的 Linux 发行版"
                exit 1
            fi
        else
            log_error "不支持的操作系统"
            exit 1
        fi
        
        # 验证安装
        if ! check_command node || ! check_command npm; then
            log_error "Node.js 安装失败"
            exit 1
        fi
        log_info "Node.js 安装成功"
    fi
}

# 检查目录结构
if [ ! -d "frontend" ]; then
    log_error "目录结构不正确，请确保在项目根目录下运行此脚本"
    exit 1
fi

# 清理函数
cleanup() {
    log_info "正在清理..."
    pkill -f "npm start|expo" || true
    if [ -d "frontend/node_modules" ]; then
        log_info "清理前端依赖..."
        rm -rf frontend/node_modules
    fi
}

# 设置前端环境
setup_frontend() {
    log_info "设置前端环境..."
    cd frontend
    
    # 清理旧的依赖
    log_info "清理旧的依赖..."
    rm -rf node_modules package-lock.json
    
    # 安装依赖
    log_info "安装前端依赖..."
    npm install
    
    cd ..
}

# 构建前端
build_frontend() {
    log_info "构建前端..."
    cd frontend
    
    # 检查环境变量
    if [ -z "$REACT_APP_API_URL" ]; then
        log_warn "REACT_APP_API_URL 环境变量未设置，使用默认值"
        export REACT_APP_API_URL="http://localhost:8000"
    fi
    
    # 构建生产版本
    log_info "构建生产版本..."
    npm run build
    
    cd ..
}

# 启动服务
start_services() {
    # 检查 PORT 环境变量
    if [ -z "$PORT" ]; then
        log_error "PORT 环境变量未设置"
        exit 1
    fi
    
    # 启动前端服务
    log_info "启动前端服务..."
    cd frontend
    
    # 使用 serve 启动静态文件服务
    log_info "使用 serve 启动静态文件服务..."
    npx serve -s build -l $PORT
    
    cd ..
}

# 主函数
main() {
    # 注册清理函数
    trap cleanup EXIT
    
    # 检查必要的命令
    log_info "检查必要的命令..."
    check_and_install_node
    
    # 执行部署步骤
    setup_frontend
    build_frontend
    start_services
}

# 执行主函数
main "$@" 