"""Markdown to PDF conversion service."""
import io
from pathlib import Path
from typing import Literal

from markdown_it import MarkdownIt
from xhtml2pdf import pisa
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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

# Register Chinese fonts
def register_fonts():
    """Register Chinese fonts for PDF generation."""
    font_paths = [
        # Windows
        Path("C:/Windows/Fonts/msyh.ttc"),  # Microsoft YaHei
        Path("C:/Windows/Fonts/simhei.ttf"),  # SimHei
        Path("C:/Windows/Fonts/simsun.ttc"),  # SimSun
        # macOS
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
        # Linux
        Path("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    ]

    for font_path in font_paths:
        if font_path.exists():
            try:
                pdfmetrics.registerFont(TTFont("ChineseFont", str(font_path)))
                return "ChineseFont"
            except Exception:
                continue

    return "Helvetica"


class MarkdownConverter:
    """Markdown to PDF converter."""

    def __init__(self, themes_dir: Path | None = None):
        self.md = MarkdownIt("commonmark", {"html": True})
        self.themes_dir = themes_dir or Path(__file__).parent.parent / "static" / "css" / "themes"
        self.font_name = register_fonts()

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

        css_content = ""
        if css_path.exists():
            css_content = css_path.read_text(encoding="utf-8")

        # Add font-face for Chinese support
        font_css = f"""
        @font-face {{
            font-family: ChineseFont;
            src: url("C:/Windows/Fonts/msyh.ttc");
        }}
        body {{
            font-family: ChineseFont, {self.font_name}, sans-serif;
        }}
        """

        full_html = self._build_html_document(html_content, title, font_css + css_content)

        pdf_buffer = io.BytesIO()
        pisa_status = pisa.CreatePDF(
            full_html,
            dest=pdf_buffer,
            encoding="utf-8",
            path=str(self.themes_dir)  # For relative paths in CSS
        )

        if pisa_status.err:
            raise RuntimeError(f"PDF generation failed with {pisa_status.err} errors")

        return pdf_buffer.getvalue()

    def _build_html_document(self, content: str, title: str, css: str) -> str:
        """Build complete HTML document with CSS."""
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        {css}
    </style>
</head>
<body>
    <div class="document">
        {content}
    </div>
</body>
</html>"""
