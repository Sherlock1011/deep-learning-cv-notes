from pathlib import Path
import base64
import html
import json
import re

import markdown


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "CV_source" / "CV-main"
OUTPUT = ROOT / "learning_notes" / "notebooks"
INDEX = ROOT / "learning_notes" / "index.html"


STYLE = """
body {
  margin: 0;
  color: #18212f;
  background: #eef3f8;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
  line-height: 1.7;
}
main {
  max-width: 1040px;
  margin: 0 auto;
  padding: 34px 28px 80px;
  background: #fff;
  min-height: 100vh;
  border-left: 1px solid #d8dee8;
  border-right: 1px solid #d8dee8;
}
a { color: #2563eb; text-decoration: none; }
a:hover { text-decoration: underline; }
h1, h2, h3, h4 { line-height: 1.25; margin-top: 1.45em; letter-spacing: 0; }
h1 {
  margin-top: 0;
  padding-bottom: 14px;
  border-bottom: 1px solid #d8dee8;
  font-size: clamp(28px, 4vw, 42px);
}
h2 {
  margin-top: 42px;
  padding: 12px 14px;
  border-left: 5px solid #2563eb;
  background: #f3f6fb;
  border-radius: 8px;
  font-size: 25px;
}
h3 { color: #28364a; }
p {
  margin: 10px 0 14px;
  max-width: 820px;
}
img {
  display: block;
  max-width: min(100%, 900px);
  height: auto;
  margin: 14px auto;
  border: 1px solid #d8dee8;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
}
table { border-collapse: collapse; width: 100%; margin: 12px 0; }
th, td { border: 1px solid #d8dee8; padding: 8px 10px; text-align: left; }
blockquote { border-left: 4px solid #bfd0ea; margin-left: 0; padding: 6px 16px; color: #4d5868; background: #f3f6fb; }
pre {
  overflow-x: auto;
  background: #0f172a;
  color: #e5e7eb;
  border-radius: 8px;
  padding: 14px 16px;
  font-family: "Cascadia Mono", Consolas, monospace;
  font-size: 14px;
  line-height: 1.55;
}
code {
  font-family: "Cascadia Mono", Consolas, monospace;
  background: #eef3fb;
  border-radius: 5px;
  padding: 1px 5px;
}
pre code { background: transparent; padding: 0; }
.top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 18px;
}
.top a {
  display: inline-block;
  border: 1px solid #d8dee8;
  border-radius: 8px;
  padding: 6px 10px;
  background: #f7f9fc;
}
.reader-note {
  color: #4d5868;
  background: #f8fafc;
  border: 1px solid #d8dee8;
  border-radius: 8px;
  padding: 12px 14px;
  margin: 18px 0 24px;
}
.toc {
  background: #ffffff;
  border: 1px solid #d8dee8;
  border-radius: 8px;
  padding: 14px 16px;
  margin: 18px 0 28px;
}
.toc strong {
  display: block;
  margin-bottom: 8px;
}
.toc a {
  display: inline-block;
  margin: 3px 12px 3px 0;
  color: #28364a;
}
.cell {
  margin: 20px 0;
}
.markdown-cell {
  font-size: 16px;
  max-width: 900px;
}
.markdown-cell > :first-child { margin-top: 0; }
.markdown-cell > :last-child { margin-bottom: 0; }
.markdown-cell li { margin: 4px 0; }
.markdown-cell strong { color: #0f172a; }
.heading-cell {
  max-width: 100%;
}
.step-cell {
  position: relative;
  max-width: 900px;
  margin: 16px 0;
  padding: 16px 18px 16px 58px;
  background: #fbfcff;
  border: 1px solid #d8dee8;
  border-left: 5px solid #12805c;
  border-radius: 8px;
}
.step-cell .step-badge {
  position: absolute;
  left: 16px;
  top: 15px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  background: #12805c;
  font-weight: 700;
  line-height: 1;
}
.step-cell p {
  margin: 0 0 8px;
  max-width: 780px;
}
.figure-cell {
  max-width: 100%;
  margin: 12px 0 26px;
}
.figure-cell p {
  max-width: 100%;
}
.markdown-cell hr {
  border: 0;
  border-top: 1px solid #d8dee8;
  margin: 28px 0;
}
.code-cell {
  border: 1px solid #d8dee8;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
}
.code-head {
  font-size: 13px;
  color: #5e6878;
  background: #eef3fb;
  padding: 6px 10px;
  border-bottom: 1px solid #d8dee8;
}
.code-cell pre { margin: 0; border-radius: 0; }
.output {
  border-top: 1px solid #d8dee8;
  padding: 10px 12px;
  background: #fbfcff;
}
.output pre {
  background: #f3f6fb;
  color: #18212f;
  margin: 0;
}
.output img { box-shadow: none; }
.inline-code {
  font-family: "Cascadia Mono", Consolas, monospace;
  color: #0f172a;
  background: #eef3fb;
  border: 1px solid #d8dee8;
  border-radius: 5px;
  padding: 1px 5px;
  word-break: break-word;
}
@media (max-width: 760px) {
  main { padding: 24px 16px 56px; border: 0; }
  .top { flex-direction: column; align-items: stretch; }
  .top a { text-align: center; }
}
"""


def as_text(source) -> str:
    if isinstance(source, list):
        return "".join(source)
    return source or ""


def attachment_to_data_uri(name: str, attachments: dict) -> str:
    payload = attachments.get(name)
    if not payload:
        return f"attachment:{name}"
    for mime in ("image/png", "image/jpeg", "image/gif", "image/webp", "image/svg+xml"):
        if mime in payload:
            data = as_text(payload[mime]).replace("\n", "")
            if mime == "image/svg+xml":
                data = base64.b64encode(data.encode("utf-8")).decode("ascii")
            return f"data:{mime};base64,{data}"
    return f"attachment:{name}"


def inline_attachments(source: str, attachments: dict) -> str:
    if not attachments:
        return source

    def replace_markdown(match: re.Match[str]) -> str:
        alt, name = match.group(1), match.group(2)
        return f"![{alt}]({attachment_to_data_uri(name, attachments)})"

    def replace_html(match: re.Match[str]) -> str:
        name = match.group(1)
        return f'src="{attachment_to_data_uri(name, attachments)}"'

    source = re.sub(r"!\[([^\]]*)\]\(attachment:([^)]+)\)", replace_markdown, source)
    source = re.sub(r'src=["\']attachment:([^"\']+)["\']', replace_html, source)
    return source


def normalize_markdown(source: str) -> str:
    lines = []
    for line in source.splitlines():
        if re.match(r"^#{1,5}\s+", line):
            lines.append("#" + line)
        else:
            lines.append(line)
    return "\n".join(lines)


def format_inline_commands(rendered: str) -> str:
    command_patterns = [
        r"\bjupyter kernelspec list\b",
        r"\bconda create --name [^，。<]+",
        r"\bconda activate [A-Za-z0-9_.-]+",
        r"\bpip install [A-Za-z0-9_.\-\[\]]+",
        r"\bcd [A-Za-z]:\\[^，。<]+",
        r"\bnvidia-smi\b",
        r"\bconda install [^，。<]+",
        r"\bimport [A-Za-z0-9_., ]+",
    ]

    def wrap(match: re.Match[str]) -> str:
        text = match.group(0).strip()
        return f'<span class="inline-code">{html.escape(text)}</span>'

    for pattern in command_patterns:
        rendered = re.sub(pattern, wrap, rendered)
    return rendered


def render_markdown(source: str, attachments: dict | None = None) -> str:
    source = inline_attachments(source, attachments or {})
    source = normalize_markdown(source)
    step_match = re.match(r"^\s*([①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳])\s*(.*)", source, re.S)
    if step_match:
        source = step_match.group(2).strip()
    return markdown.markdown(
        source,
        extensions=["extra", "toc", "sane_lists", "fenced_code"],
        output_format="html5",
    )


def markdown_cell_class(source: str) -> str:
    stripped = source.strip()
    classes = ["cell", "markdown-cell"]
    if re.match(r"^#{1,6}\s+", stripped):
        classes.append("heading-cell")
    if re.match(r"^[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]\s*", stripped):
        classes.append("step-cell")
    if re.fullmatch(r"!\[[^\]]*\]\(attachment:[^)]+\)", stripped) or re.fullmatch(
        r"!\[[^\]]*\]\([^)]+\)", stripped
    ):
        classes.append("figure-cell")
    return " ".join(classes)


def render_markdown_cell(source: str, attachments: dict | None = None) -> str:
    stripped = source.strip()
    step_match = re.match(r"^\s*([①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳])\s*", stripped)
    rendered = format_inline_commands(render_markdown(source, attachments))
    prefix = ""
    if step_match:
        prefix = f'<span class="step-badge">{step_match.group(1)}</span>'
    return f'<section class="{markdown_cell_class(source)}">{prefix}{rendered}</section>'


def extract_headings(notebook: dict) -> list[str]:
    headings: list[str] = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        source = as_text(cell.get("source")).strip()
        match = re.match(r"^#\s+(.+)", source)
        if match:
            headings.append(re.sub(r"[*_`]", "", match.group(1)).strip())
    return headings


def render_output(output: dict) -> str:
    output_type = output.get("output_type")
    if output_type == "stream":
        return f'<div class="output"><pre>{html.escape(as_text(output.get("text")))}</pre></div>'

    if output_type in {"display_data", "execute_result"}:
        data = output.get("data", {})
        if "text/html" in data:
            return f'<div class="output">{as_text(data["text/html"])}</div>'
        if "image/png" in data:
            image = as_text(data["image/png"]).replace("\n", "")
            return f'<div class="output"><img src="data:image/png;base64,{image}" alt="notebook output"></div>'
        if "image/jpeg" in data:
            image = as_text(data["image/jpeg"]).replace("\n", "")
            return f'<div class="output"><img src="data:image/jpeg;base64,{image}" alt="notebook output"></div>'
        if "text/markdown" in data:
            return f'<div class="output">{render_markdown(as_text(data["text/markdown"]))}</div>'
        if "text/plain" in data:
            return f'<div class="output"><pre>{html.escape(as_text(data["text/plain"]))}</pre></div>'

    if output_type == "error":
        traceback = "\n".join(output.get("traceback", []))
        return f'<div class="output"><pre>{html.escape(traceback)}</pre></div>'

    return ""


def render_notebook(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    headings = extract_headings(notebook)
    toc = ""
    if len(headings) > 1:
        toc_links = "".join(f"<a href=\"#section-{i}\">{html.escape(title)}</a>" for i, title in enumerate(headings, 1))
        toc = f'<nav class="toc"><strong>本节目录</strong>{toc_links}</nav>'
    parts = [
        "<!doctype html>",
        '<html lang="zh-CN">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{html.escape(path.stem)}</title>",
        f"<style>{STYLE}</style>",
        "</head>",
        "<body>",
        "<main>",
        '<div class="top"><a href="../index.html">返回讲义目录</a><a href="https://github.com/AccumulateMore/CV/tree/main">原始 notebook 目录</a></div>',
        f"<h1>{html.escape(path.stem)}</h1>",
        '<div class="reader-note">这页由原始 Jupyter Notebook 转为浏览器阅读版：步骤说明会以绿色提示块展示，截图已内嵌到页面中，代码和命令会用深色或浅色代码样式区分。</div>',
        toc,
    ]

    section_index = 0
    for cell in notebook.get("cells", []):
        cell_type = cell.get("cell_type")
        source = as_text(cell.get("source"))
        if cell_type == "markdown":
            rendered = render_markdown_cell(source, cell.get("attachments"))
            if re.match(r"^\s*#\s+", source):
                section_index += 1
                rendered = rendered.replace('<section class="cell markdown-cell heading-cell">', f'<section id="section-{section_index}" class="cell markdown-cell heading-cell">', 1)
            parts.append(rendered)
        elif cell_type == "code":
            outputs = "".join(render_output(output) for output in cell.get("outputs", []))
            parts.append(
                '<section class="cell code-cell">'
                '<div class="code-head">代码</div>'
                f"<pre><code>{html.escape(source)}</code></pre>"
                f"{outputs}"
                "</section>"
            )

    parts.extend(["</main>", "</body>", "</html>"])
    return "\n".join(parts)


def convert_notebooks() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for notebook_path in sorted(SOURCE.glob("*.ipynb")):
        output_path = OUTPUT / f"{notebook_path.stem}.html"
        output_path.write_text(render_notebook(notebook_path), encoding="utf-8")


def rewrite_index_links() -> None:
    text = INDEX.read_text(encoding="utf-8")

    def replace_link(match: re.Match[str]) -> str:
        name = Path(match.group(1)).stem
        return f'href="notebooks/{name}.html"'

    text = re.sub(
        r'href="\.\./CV_source/CV-main/([^"]+?\.ipynb)"',
        replace_link,
        text,
    )

    note = (
        '<div class="box"><strong>浏览器版笔记</strong>'
        '<a href="notebooks/100_配置版本.html">从第 100 节开始阅读</a>，'
        "原始 .ipynb 已转换为 HTML。</div>"
    )
    if "浏览器版笔记" not in text:
        text = text.replace(
            '<div class="box"><strong>建议阅读方式</strong>先看本讲义定路线，再用 Jupyter Notebook 打开对应原笔记实操。</div>',
            note
            + '\n        <div class="box"><strong>建议阅读方式</strong>先看本讲义定路线；想改代码时，再用 Jupyter Notebook 打开原始 .ipynb 实操。</div>',
            1,
        )

    INDEX.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    convert_notebooks()
    rewrite_index_links()
