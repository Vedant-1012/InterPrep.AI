import re

def markdown_to_html(content: str) -> str:
    """Convert basic markdown-style content to professional HTML."""
    if not content:
        return ""

    formatted_content = '<div class="question-content">\n'

    sections = re.split(r'(\*\*.*?\*\*|##.*?(?=\n))', content)
    in_example = False
    in_constraints = False

    for section in sections:
        if not section.strip():
            continue

        # Headers
        if section.startswith("##") or section.startswith("**"):
            section_text = section.replace("##", "").replace("**", "").strip()

            if "example" in section_text.lower() or "input" in section_text.lower():
                in_example = True
                in_constraints = False
                formatted_content += f'<div class="example-section">\n<h3>{section_text}</h3>\n'
            elif "constraint" in section_text.lower():
                in_constraints = True
                in_example = False
                formatted_content += f'<div class="constraints-section">\n<h3>{section_text}</h3>\n'
            else:
                in_example = in_constraints = False
                formatted_content += f'<h3>{section_text}</h3>\n'
        else:
            if in_example:
                section = re.sub(r'Input:', '<strong>Input:</strong>', section)
                section = re.sub(r'Output:', '<strong>Output:</strong>', section)
                section = re.sub(r'Explanation:', '<strong>Explanation:</strong>', section)
                section = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code>\2</code></pre>', section, flags=re.DOTALL)
                formatted_content += f'<div class="example-block">\n{section.strip()}\n</div>\n'

            elif in_constraints:
                constraints = section.strip().split('\n')
                formatted_content += '<div class="constraints-block">\n<ul>\n'
                for line in constraints:
                    if line.strip():
                        formatted_content += f'<li>{line.strip()}</li>\n'
                formatted_content += '</ul>\n</div>\n'

            else:
                section = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code>\2</code></pre>', section, flags=re.DOTALL)
                section = re.sub(r'`(.*?)`', r'<code>\1</code>', section)
                paragraphs = section.strip().split('\n\n')
                for p in paragraphs:
                    formatted_content += f'<p>{p.strip()}</p>\n'

    formatted_content += '</div>'
    return formatted_content