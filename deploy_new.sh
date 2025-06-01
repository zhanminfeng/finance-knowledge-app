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

# 检查并安装 Node.js
check_and_install_node() {
    if ! check_command node || ! check_command npm; then
        log_info "正在安装 Node.js..."
        
        # 检查 nvm
        if ! check_command nvm; then
            log_info "正在安装 nvm..."
            curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
            export NVM_DIR="$HOME/.nvm"
            [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
        fi
        
        # 安装 Node.js 18
        nvm install 18
        nvm use 18
        
        # 验证安装
        if ! check_command node || ! check_command npm; then
            log_error "Node.js 安装失败"
            exit 1
        fi
        log_info "Node.js 安装成功"
    fi
}

# 检查必要的命令
log_info "检查必要的命令..."
check_and_install_python
check_and_install_node

# 检查目录结构
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    log_error "目录结构不正确，请确保在项目根目录下运行此脚本"
    exit 1
fi

# 清理函数
cleanup() {
    log_info "正在清理..."
    pkill -f "uvicorn|npm start|expo" || true
    if [ -d "backend/venv" ]; then
        log_info "清理后端虚拟环境..."
        rm -rf backend/venv
    fi
    if [ -d "frontend/node_modules" ]; then
        log_info "清理前端依赖..."
        rm -rf frontend/node_modules
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

# 设置前端环境
setup_frontend() {
    log_info "设置前端环境..."
    cd frontend
    
    # 确保使用 Node.js 18
    log_info "确保使用 Node.js 18..."
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm use 18
    
    # 清理旧的依赖
    log_info "清理旧的依赖..."
    rm -rf node_modules package-lock.json
    
    # 安装依赖
    log_info "安装前端依赖..."
    npm install
    
    cd ..
}

# 启动服务
start_services() {
    # 启动后端
    log_info "启动后端服务..."
    cd backend
    source venv/bin/activate
    uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload &
    BACKEND_PID=$!
    cd ..
    
    # 启动前端
    log_info "启动前端服务..."
    cd frontend
    # 使用 LAN 模式启动
    EXPO_DEVTOOLS_LISTEN_ADDRESS=0.0.0.0 npx expo start --lan &
    FRONTEND_PID=$!
    cd ..
    
    # 等待服务启动
    sleep 5
    
    # 检查服务是否正常运行
    if ! curl -s http://localhost:$PORT/docs > /dev/null; then
        log_error "后端服务启动失败"
        exit 1
    fi
    
    log_info "服务启动成功！"
    log_info "后端 API 文档: http://localhost:$PORT/docs"
    log_info "前端开发服务器: 请确保手机和电脑在同一网络下"
    log_info "在 iOS 设备上："
    log_info "1. 打开 Expo Go 应用"
    log_info "2. 点击 'Scan QR Code' 扫描终端中显示的二维码"
    log_info "3. 如果扫描失败，请确保："
    log_info "   - 手机和电脑连接到同一个 WiFi 网络"
    log_info "   - 允许相机权限"
    log_info "   - 检查电脑防火墙设置"
}

# 主函数
main() {
    # 注册清理函数
    trap cleanup EXIT
    
    # 检查是否在后台运行
    if [ "$1" == "--background" ]; then
        log_info "在后台运行服务..."
        nohup $0 > deploy.log 2>&1 &
        echo $! > deploy.pid
        log_info "服务已在后台启动，PID: $(cat deploy.pid)"
        log_info "查看日志: tail -f deploy.log"
        exit 0
    fi
    
    # 执行部署步骤
    setup_backend
    setup_frontend
    start_services
    
    # 等待用户中断
    log_info "按 Ctrl+C 停止服务"
    wait
}

# 执行主函数
main "$@" 