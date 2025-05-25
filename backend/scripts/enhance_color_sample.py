import re
from app.models import Question
from app.extensions import db
from dotenv import load_dotenv
load_dotenv()


def highlight_keywords(text):
    """Add color to common section titles and keywords."""
    replacements = [
        (r'Time Complexity:', '<span style="color: #e67e22; font-weight: bold">Time Complexity:</span>'),
        (r'Space Complexity:', '<span style="color: #3498db; font-weight: bold">Space Complexity:</span>'),
        (r'Constraints:', '<span style="color: #c0392b; font-weight: bold">Constraints:</span>'),
        (r'Examples:', '<span style="color: #2c3e50; font-weight: bold">Examples:</span>'),
        (r'Explanation:', '<span style="color: #16a085; font-weight: bold">Explanation:</span>'),
        (r'Input:', '<span style="color: #8e44ad">Input:</span>'),
        (r'Output:', '<span style="color: #8e44ad">Output:</span>')
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text


def color_format_question(question_id):
    question = Question.query.get(question_id)
    if not question or not question.content:
        return False

    try:
        question.content = highlight_keywords(question.content)
        db.session.commit()
        print(f"✅ Colored: {question.title}")
        return True
    except Exception as e:
        print(f"❌ Failed to apply color to Q{question_id}: {e}")
        return False


def color_format_sample_questions():
    sample_ids = [1, 2, 3, 4, 5]
    for qid in sample_ids:
        print(f"🎨 Enhancing color for question {qid}...")
        color_format_question(qid)


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        color_format_sample_questions()