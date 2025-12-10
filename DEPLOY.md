# 🚀 阿里云部署指南

本项目已经配置了 Docker 和 Docker Compose，部署非常简单。以下是详细步骤。

## 1. 购买服务器

推荐选择 **阿里云轻量应用服务器** 或 **ECS 云服务器**。

*   **地域**：选择距离你（或你的用户）较近的地区。
*   **镜像 (系统)**：推荐选择 **Ubuntu 22.04** 或 **Debian 11** (本项目以 Ubuntu 为例)。
*   **配置**：最低配置 1核 2G 内存即可运行。

## 2. 登录服务器

使用 SSH 工具登录你的服务器。
*   Windows 用户可以使用 CMD/PowerShell 自带的 `ssh` 命令，或者下载 [FinalShell](https://www.hostbuf.com/), [Xshell](https://www.xshell.com/) 等工具。

```bash
ssh root@你的服务器公网IP
# 输入密码
```

## 3. 安装 Docker 环境

在服务器终端执行以下命令来安装 Docker 和 Docker Compose：

```bash
# 更新软件源
apt-get update

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 启动 Docker 并设置开机自启
systemctl start docker
systemctl enable docker

# 安装 Docker Compose (新版 Docker 已内置 compose 插件)
# 验证是否安装成功
docker compose version
# 如果显示 version ... 则安装成功
```

## 4. 上传代码

你有两种方式将代码上传到服务器：

### 方式 A：使用 Git (推荐)

如果你已经将代码托管在 GitHub/Gitee：

```bash
# 在服务器上安装 git
apt-get install -y git

# 拉取代码
git clone https://你的仓库地址.git
cd hzwz-markdown-wx
```

### 方式 B：直接上传文件 (适用于未托管代码)

在你的 **本地电脑** (Windows) 上，打开 PowerShell，使用 `scp` 命令将项目上传：

```powershell
# 在项目根目录下执行
# 假设服务器IP是 1.2.3.4
scp -r . root@1.2.3.4:/root/hzwz-markdown-wx
```

*注意：这会上传所有文件，包括 `node_modules` (如果本地有)，建议先删除本地的 `node_modules` 和 `.venv` 再上传，或者使用 Git 方式。*

## 5. 启动项目

回到 **服务器终端**，进入项目目录并启动：

```bash
cd /root/hzwz-markdown-wx

# 使用 Docker Compose 一键构建并启动
docker compose up -d --build
```

等待构建完成（第一次构建可能需要几分钟，因为要下载依赖）。

## 6. 配置阿里云安全组 (防火墙)

项目默认运行在 **8000** 端口。你需要去阿里云控制台开放这个端口：

1.  登录阿里云控制台。
2.  找到你的实例 (ECS 或 轻量应用服务器)。
3.  找到 **“安全组”** 或 **“防火墙”** 设置。
4.  添加规则：
    *   **协议**：TCP
    *   **端口范围**：8000
    *   **授权对象**：0.0.0.0/0 (允许所有IP访问)

## 7. 访问

打开浏览器，访问：`http://你的服务器公网IP:8000`

你应该能看到项目已经成功运行了！🎉

---

## 进阶：使用 Nginx 配置域名 (可选)

如果你想用域名访问 (如 `http://www.example.com`) 且不加端口号，可以在服务器上安装 Nginx 进行反向代理。

1.  **安装 Nginx**: `apt-get install -y nginx`
2.  **配置 Nginx**: 编辑 `/etc/nginx/sites-available/default`
    ```nginx
    server {
        listen 80;
        server_name 你的域名或IP;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    ```
3.  **重启 Nginx**: `systemctl restart nginx`

## 8. 日常维护与更新

当你在本地修改了代码（比如增加了新的样式、修改了前端页面）并推送到 Git 仓库后，需要在服务器上进行更新。

### 方式 A：使用一键更新脚本 (推荐)

我在项目里准备了一个 `update.sh` 脚本。

1.  **首次使用前**，给脚本添加执行权限：
    ```bash
    chmod +x update.sh
    ```

2.  **以后每次更新**，只需要运行：
    ```bash
    ./update.sh
    ```
    这个脚本会自动执行 `git pull` 拉取代码，并重建、重启 Docker 容器。

### 方式 B：手动更新

如果你没有使用 Git，或者想手动控制，可以按以下步骤操作：

1.  **上传新文件**：
    *   如果是 **代码/前端修改**：上传覆盖对应的文件。
    *   如果是 **样式/模板修改**：将新的 `.ini` 或 `.html` 文件上传到 `server/styles` 或 `server/template` 目录。

2.  **重启服务**：
    *   **情况 1：修改了 Python 代码或前端 React 代码**
        必须重新构建镜像：
        ```bash
        docker compose up -d --build
        ```
    
    *   **情况 2：只修改了样式 (.ini) 或模板 (.html)**
        由于我们配置了文件挂载，你不需要重新构建镜像，只需要重启容器让后台重新加载配置即可（速度更快）：
        ```bash
        docker compose restart
        ```

### 常见问题

*   **Q: 我增加了一个样式文件，为什么刷新页面没看到？**
    *   A: 后端服务会在启动时扫描并加载所有主题配置到内存中。所以即使你上传了文件，也**必须重启服务** (`docker compose restart`) 才能生效。

*   **Q: 磁盘空间满了怎么办？**
    *   A: Docker 构建过程中会产生一些临时镜像。可以使用 `docker system prune -a` 清理不再使用的镜像和缓存。

