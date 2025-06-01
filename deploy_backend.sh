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

# 检查并安装 Python 3.11
check_and_install_python() {
    if ! check_command python3.11; then
        log_info "正在安装 Python 3.11..."
        
        # 检查操作系统类型
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if check_command apt-get; then
                # Debian/Ubuntu
                sudo apt-get update
                sudo apt-get install -y software-properties-common
                sudo add-apt-repository -y ppa:deadsnakes/ppa
                sudo apt-get update
                sudo apt-get install -y python3.11 python3.11-venv
            elif check_command yum; then
                # CentOS/RHEL
                sudo yum install -y python3.11
            else
                log_error "不支持的 Linux 发行版"
                exit 1
            fi
        else
            log_error "不支持的操作系统"
            exit 1
        fi
        
        # 验证安装
        if ! check_command python3.11; then
            log_error "Python 3.11 安装失败"
            exit 1
        fi
        log_info "Python 3.11 安装成功"
    fi
}

# 检查目录结构
if [ ! -d "backend" ]; then
    log_error "目录结构不正确，请确保在项目根目录下运行此脚本"
    exit 1
fi

# 清理函数
cleanup() {
    log_info "正在清理..."
    pkill -f "uvicorn|gunicorn" || true
    if [ -d "backend/venv" ]; then
        log_info "清理后端虚拟环境..."
        rm -rf backend/venv
    fi
}

# 设置后端环境
setup_backend() {
    log_info "设置后端环境..."
    cd backend
    
    # 清理旧的虚拟环境
    if [ -d "venv" ]; then
        log_info "清理旧的虚拟环境..."
        rm -rf venv
    fi
    
    # 创建虚拟环境
    log_info "创建 Python 虚拟环境..."
    python3.11 -m venv venv
    source venv/bin/activate
    
    # 升级 pip
    log_info "升级 pip..."
    pip install --upgrade pip
    
    # 安装依赖
    log_info "安装后端依赖..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        log_error "未找到 requirements.txt"
        exit 1
    fi
    
    cd ..
}

# 启动服务
start_services() {
    # 检查 PORT 环境变量
    if [ -z "$PORT" ]; then
        log_error "PORT 环境变量未设置"
        exit 1
    fi
    
    # 启动后端
    log_info "启动后端服务..."
    cd backend
    source venv/bin/activate
    
    # 使用 gunicorn 启动服务
    log_info "使用 gunicorn 启动服务..."
    gunicorn app.main:app --bind 0.0.0.0:$PORT --workers 4 --worker-class uvicorn.workers.UvicornWorker
    
    cd ..
}

# 主函数
main() {
    # 注册清理函数
    trap cleanup EXIT
    
    # 检查必要的命令
    log_info "检查必要的命令..."
    check_and_install_python
    
    # 执行部署步骤
    setup_backend
    start_services
}

# 执行主函数
main "$@" 