# Markdown to PDF Converter

一个基于 FastAPI 的 Markdown 转 PDF Web 应用，支持实时预览和多种主题样式。

## 功能特点

- **Markdown 编辑器** - 基于 CodeMirror，支持语法高亮
- **文件上传** - 支持上传 .md 文件
- **HTML 预览** - 点击按钮即可预览渲染效果
- **多主题支持** - 默认、学术论文、技术文档三种主题
- **PDF 生成** - 使用 WeasyPrint 生成高质量 PDF
- **历史记录** - 24小时内可重新下载已生成的文件

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

> **注意**: WeasyPrint 需要系统安装 GTK+ 库。Windows 用户请参考 [WeasyPrint 安装指南](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation)。

### 2. 运行服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 访问应用

打开浏览器访问 http://localhost:8000

## 主题说明

| 主题 | 适用场景 |
|------|----------|
| 默认主题 | 通用文档，现代简洁风格 |
| 学术论文 | 中文学术论文，宋体正文黑体标题 |
| 技术文档 | 技术文档，代码高亮，适合程序员 |

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 主页面 |
| `/api/preview` | POST | 预览 Markdown 渲染结果 |
| `/api/convert` | POST | 生成 PDF |
| `/api/upload` | POST | 上传 .md 文件 |
| `/api/download/{file_id}` | GET | 下载 PDF |
| `/api/history` | GET | 获取历史记录 |

## 目录结构

```
markdown2pdf/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── routers/
│   │   └── api.py           # API 路由
│   ├── services/
│   │   ├── converter.py     # 转换服务
│   │   └── storage.py       # 存储服务
│   ├── templates/
│   │   └── index.html       # 主页面模板
│   └── static/
│       └── css/
│           └── themes/      # PDF 主题样式
├── temp/                    # 临时 PDF 存储
├── requirements.txt
└── README.md
```

## 技术栈

- **后端**: FastAPI + WeasyPrint + Markdown-it-py
- **前端**: TailwindCSS + CodeMirror + Alpine.js
