# Markdown to PDF Converter

一个基于 FastAPI 的 Markdown 转 PDF Web 应用，支持实时预览和多种主题样式。

## 功能特点

- **Markdown 编辑器** - 基于 CodeMirror，支持语法高亮
- **文件上传** - 支持上传 .md 文件
- **HTML 预览** - 点击按钮即可预览渲染效果
- **多主题支持** - 默认、学术论文、技术文档三种主题
- **PDF 生成** - 使用 WeasyPrint 生成高质量 PDF
- **历史记录** - 24小时内可重新下载已生成的文件
- **中文支持** - 自动检测并使用系统中文字体

## 安装

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装 Python 依赖
pip install -r requirements.txt
```

### 2. 安装 GTK+（WeasyPrint 依赖）

WeasyPrint 需要系统安装 GTK+ 库。

#### Windows

1. 下载 GTK+ 安装包：https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
2. 运行安装程序，使用默认选项即可
3. 重启终端或 IDE 使环境变量生效

#### Linux (Debian/Ubuntu)

```bash
sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

#### macOS

```bash
brew install pango gdk-pixbuf libffi
```

### 3. 验证安装

```bash
python -c "from weasyprint import HTML; print('WeasyPrint 安装成功')"
```

## 运行

```bash
# 激活虚拟环境后
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000 即可使用。

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

### API 示例

**转换为 PDF：**

```bash
curl -X POST http://localhost:8000/api/convert \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# 标题\n\n内容", "theme": "default", "filename": "document"}'
```

**响应：**

```json
{
  "success": true,
  "file_id": "abc123",
  "download_url": "/api/download/abc123",
  "filename": "document.pdf",
  "file_size": 7168,
  "expires_at": "2024-01-02T12:00:00"
}
```

## 目录结构

```
markdown2pdfv2/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── deps.py              # 依赖注入
│   ├── routers/
│   │   └── api.py           # API 路由
│   ├── services/
│   │   ├── converter.py     # Markdown 转 PDF 服务
│   │   └── storage.py       # 文件存储服务
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

- **后端**: FastAPI + WeasyPrint + markdown-it-py
- **前端**: TailwindCSS + CodeMirror + Alpine.js

## 许可证

MIT License
