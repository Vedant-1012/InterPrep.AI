import re
from app.extensions import db
from app.models.question import Question
from dotenv import load_dotenv
load_dotenv()

def format_existing_content(question_id):
    """Format existing question content with professional HTML without regenerating."""
    question = Question.query.get(question_id)
    if not question or not question.content:
        return False

    content = question.content
    formatted_content = ""

    # Split content into sections
    sections = re.split(r'(\*\*.*?\*\*|##.*?(?=\n))', content)

    # Initialize HTML structure
    formatted_content = '<div class="question-content">\n'

    current_section = "description"
    in_example = False
    in_constraints = False

    for section in sections:
        if not section.strip():
            continue

        # Handle section headers
        if section.startswith("##") or section.startswith("**"):
            section_text = section.replace("##", "").replace("**", "").strip()

            # Determine section type
            if "example" in section_text.lower() or "input" in section_text.lower():
                current_section = "example"
                in_example = True
                in_constraints = False
                formatted_content += f'<div class="example-section">\n<h3>{section_text}</h3>\n'
            elif "constraint" in section_text.lower():
                current_section = "constraints"
                in_example = False
                in_constraints = True
                formatted_content += f'<div class="constraints-section">\n<h3>{section_text}</h3>\n'
            elif "time complexity" in section_text.lower() or "space complexity" in section_text.lower():
                in_example = False
                in_constraints = False
                formatted_content += f'<div class="complexity-block">\n<h3>{section_text}</h3>\n'
            elif "note" in section_text.lower():
                in_example = False
                in_constraints = False
                formatted_content += f'<div class="note-block">\n<h3>{section_text}</h3>\n'
            else:
                in_example = False
                in_constraints = False
                formatted_content += f'<h3>{section_text}</h3>\n'
        else:
            if in_example:
                example_content = section.strip()
                example_content = re.sub(r'Input:', '<strong>Input:</strong>', example_content)
                example_content = re.sub(r'Output:', '<strong>Output:</strong>', example_content)
                example_content = re.sub(r'Explanation:', '<strong>Explanation:</strong>', example_content)
                example_content = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code>\2</code></pre>', example_content, flags=re.DOTALL)
                formatted_content += f'<div class="example-block">\n{example_content}\n</div>\n'
            elif in_constraints:
                constraints_content = section.strip()
                constraints_lines = constraints_content.split('\n')
                formatted_content += '<div class="constraints-block">\n<ul>\n'
                for line in constraints_lines:
                    if line.strip() and line.strip() != '*':
                        formatted_content += f'<li>{line.strip()}</li>\n'
                formatted_content += '</ul>\n</div>\n'
            else:
                content_text = section.strip()
                content_text = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code>\2</code></pre>', content_text, flags=re.DOTALL)
                content_text = re.sub(r'`(.*?)`', r'<code>\1</code>', content_text)
                paragraphs = content_text.split('\n\n')
                for p in paragraphs:
                    if p.strip():
                        formatted_content += f'<p>{p.strip()}</p>\n'

    if in_example or in_constraints:
        formatted_content += '</div>\n'

    formatted_content += '</div>'
    question.content = formatted_content
    db.session.commit()
    return True

def format_all_existing_questions():
    """Format all existing questions with professional HTML."""
    questions = Question.query.all()
    total = len(questions)
    formatted = 0

    for i, question in enumerate(questions):
        print(f"\U0001F501 Processing {i+1}/{total} - {question.title}")
        if format_existing_content(question.id):
            formatted += 1
            print(f"✅ Formatted: {question.title}")
        else:
            print(f"❌ Failed to format: {question.title}")

        if i % 20 == 0:
            db.session.commit()
            print(f"💾 Committed batch {i//20 + 1}")

    db.session.commit()
    print(f"✅ Formatted {formatted}/{total} questions with professional HTML.")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        format_all_existing_questions()
