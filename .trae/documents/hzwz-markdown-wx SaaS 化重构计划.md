# 重构计划：Python 后端 (FastAPI) + React 前端

我将基于现有的 Python 渲染逻辑，将其改造为高性能的 Web 服务，并提供现代化的前端编辑器。

## 1. 架构设计

### 1.1 总体架构

* **前端 (Web)**: 使用 **React + TypeScript + Vite** 构建。负责提供编辑器 (Monaco Editor)、实时预览界面、主题切换和导出功能。

* **后端 (Server)**: 使用 **FastAPI (Python)**。负责核心的 Markdown 解析、模板渲染和样式注入。

* **通信**: 前后端通过 RESTful API 交互 (`POST /api/render`)。

* **部署**: 使用 **Docker Compose** 编排，Nginx 负责反向代理和静态资源服务，FastAPI 负责 API 计算。

### 1.2 关键重构点 (解决性能与并发问题)

* **移除 Node.js 依赖**: 原项目在 `highlight/renderer_code.py` 中调用 `os.system('node ...')` 并读写临时文件来进行代码高亮。这种方式速度慢且在多用户并发时会冲突（文件竞争）。

  * **解决方案**: 改用 Python 原生的 **Pygments** 库进行代码高亮。它纯内存操作，速度快且线程安全，能直接生成带内联样式的 HTML，完美适配微信公众号。

* **配置内存化**: 原项目每次渲染都读取磁盘上的 `.ini` 和 `.html` 模板。

  * **解决方案**: 服务启动时将所有 `styles/` 和 `template/` 加载到内存缓存中，大幅提升渲染响应速度。

***

## 2. 实施步骤

### 第一阶段：后端重构 (Server Core)

1. **环境搭建**: 创建 `server` 目录，初始化 FastAPI 项目，引入 `pygments` 等依赖。
2. **资源加载器 (`ThemeManager`)**: 编写逻辑，启动时扫描并加载所有 `.ini` 样式配置和 Jinja2 模板到内存。
3. **渲染引擎改造**:

   * 重写 `StyleRenderer`，使其不再依赖文件路径，而是接受内存中的配置对象。

   * 重写代码高亮逻辑，使用 `pygments` 替代原来的 Node.js 调用。
4. **API 开发**:

   * `GET /api/themes`: 返回所有可用主题列表。

   * `POST /api/render`: 接收 Markdown 和主题 ID，返回渲染后的 HTML。

### 第二阶段：前端开发 (Web Client)

1. **项目初始化**: 使用 Vite 创建 React + TypeScript 项目。
2. **编辑器集成**: 集成 `Monaco Editor` 或 `React-CodeMirror`，实现左侧编辑区。
3. **预览区开发**: 右侧使用 `Shadow DOM` 或 `iframe` 展示渲染后的 HTML，防止样式污染。
4. **工具栏功能**:

   * **主题切换**: 下拉框选择后端返回的主题。

   * **复制功能**: 实现 "复制到公众号" (HTML + Inline Styles) 和 "复制 Markdown"。

   * **导出功能**: 使用客户端库 (`html2canvas`, `jspdf` 或浏览器原生打印) 实现导出图片/PDF。

### 第三阶段：部署与交付

1. **Docker 化**: 编写 `Dockerfile` (构建前端 + 运行后端) 和 `docker-compose.yml`。
2. **验证**: 在模拟的 Linux 环境中测试启动和性能。

***

## 3. 目录结构规划

```text
hzwz-markdown-wx/
├── server/                 # Python 后端
│   ├── app/
│   │   ├── core/           # 核心逻辑 (渲染、高亮)
│   │   ├── routers/        # API 路由
│   │   └── main.py         # 启动入口
│   ├── styles/             # (迁移原 styles 目录)
│   ├── template/           # (迁移原 template 目录)
│   └── requirements.txt
├── web/                    # React 前端
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── Dockerfile              # 统一构建镜像
└── docker-compose.yml      # 运行配置
```

