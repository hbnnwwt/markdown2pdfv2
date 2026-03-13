"""Markdown to PDF conversion service."""
import io
from pathlib import Path
from typing import Literal

from markdown_it import MarkdownIt
from weasyprint import HTML, CSS

ThemeType = Literal["default", "academic", "technical"]

THEMES = {
    "default": {
        "name": "Default",
        "css_file": "default.css",
    },
    "academic": {
        "name": "Academic",
        "css_file": "academic.css",
    },
    "technical": {
        "name": "Technical",
        "css_file": "technical.css",
    },
}


def get_system_font() -> str:
    """获取系统中文字体名称。"""
    # Windows 系统字体
    simhei = Path("C:/Windows/Fonts/simhei.ttf")
    if simhei.exists():
        return "SimHei"

    msyh = Path("C:/Windows/Fonts/msyh.ttc")
    if msyh.exists():
        return "Microsoft YaHei"

    # macOS / Linux 回退
    return "Noto Sans CJK SC"


class MarkdownConverter:
    """Markdown to PDF converter using WeasyPrint."""

    def __init__(self, themes_dir: Path | None = None):
        self.md = MarkdownIt("commonmark", {"html": True})
        self.themes_dir = themes_dir or Path(__file__).parent.parent / "static" / "css" / "themes"
        self.font_name = get_system_font()

    def to_html(self, markdown_text: str) -> str:
        """Convert markdown to HTML."""
        return self.md.render(markdown_text)

    def to_pdf(
        self,
        markdown_text: str,
        theme: ThemeType = "default",
        title: str = "Document",
    ) -> bytes:
        """Convert markdown to PDF bytes."""
        html_content = self.to_html(markdown_text)

        theme_config = THEMES.get(theme, THEMES["default"])
        css_path = self.themes_dir / theme_config["css_file"]

        # 基础 CSS + 中文字体
        base_css = f"""
        @page {{
            size: A4;
            margin: 2cm;
        }}

        @font-face {{
            font-family: 'SimHei';
            src: local('SimHei'), local('Microsoft YaHei'), local('Noto Sans CJK SC');
        }}

        body {{
            font-family: 'SimHei', 'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif;
            font-size: 12pt;
            line-height: 1.8;
            color: #333;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: 'SimHei', 'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif;
            color: #222;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
            font-weight: bold;
        }}

        h1 {{ font-size: 24pt; border-bottom: 2px solid #333; padding-bottom: 0.3em; }}
        h2 {{ font-size: 18pt; border-bottom: 1px solid #666; padding-bottom: 0.2em; }}
        h3 {{ font-size: 14pt; }}

        p {{
            margin: 0.8em 0;
            text-align: justify;
        }}

        ul, ol {{
            padding-left: 2em;
            margin: 0.5em 0;
        }}

        li {{
            margin: 0.3em 0;
        }}

        code {{
            font-family: 'Consolas', 'Courier New', monospace;
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
        }}

        pre {{
            background-color: #f5f5f5;
            padding: 12px;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid #ddd;
        }}

        pre code {{
            background: none;
            padding: 0;
        }}

        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 1em;
            margin: 1em 0;
            color: #666;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}

        th {{
            background-color: #f5f5f5;
            font-weight: bold;
        }}

        a {{
            color: #0066cc;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 2em 0;
        }}
        """

        # 读取主题 CSS（如果存在）
        theme_css = ""
        if css_path.exists():
            theme_css = css_path.read_text(encoding="utf-8")

        # 构建完整 HTML
        full_html = self._build_html_document(html_content, title)

        # 生成 PDF
        html_doc = HTML(string=full_html, base_url=str(self.themes_dir))
        css_doc = CSS(string=base_css + theme_css)

        pdf_buffer = io.BytesIO()
        html_doc.write_pdf(pdf_buffer, stylesheets=[css_doc])

        return pdf_buffer.getvalue()

    def _build_html_document(self, content: str, title: str) -> str:
        """Build complete HTML document."""
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
    <div class="document">
        {content}
    </div>
</body>
</html>"""
