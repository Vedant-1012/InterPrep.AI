from app.models import Question
from app.extensions import db
from dotenv import load_dotenv
import re

load_dotenv()

def enhance_question_with_visual_formatting(question_id):
    from app.ai.gemini import gemini_ai  # ✅ FIXED: local import to avoid circular issues

    question = Question.query.get(question_id)
    if not question:
        print(f"⚠️ Question ID {question_id} not found.")
        return False

    prompt = f"""
    Generate a beautifully formatted HTML coding interview question titled "{question.title}".
    It is a {question.difficulty} level {question.topic} question.

    Include:
    - A professional summary card with question ID, difficulty, and topic
    - A detailed problem description
    - At least 2 examples (inside <details> for collapsibility)
    - A list of constraints styled with colored tags
    - Time & space complexity as styled badges
    - NO function signature or code block unless part of an example
    - Use clean, semantic HTML and add CSS classnames like 'summary-card', 'tag', 'badge', 'example-block'

    Respond only with a single HTML <div class="question-content"> block.
    """

    try:
        response = gemini_ai.generate_content(prompt)

        if not response or "<div" not in response:
            raise ValueError("Invalid or empty response from Gemini.")

        # 🔥 Remove ```html and ``` markers
        response_cleaned = re.sub(r"^```html\s*|```$", "", response.strip(), flags=re.MULTILINE)

        question.content = response_cleaned
        db.session.commit()
        print(f"✅ Enhanced: {question.title}")
        return True

    except Exception as e:
        print(f"❌ Failed to format Q{question_id}: {str(e)}")
        return False


def enhance_visual_sample():
    sample_ids = [1, 2, 3, 4, 5]
    for i, qid in enumerate(sample_ids):
        print(f"\n🔄 Enhancing visually (HTML+) ID: {qid}")
        enhance_question_with_visual_formatting(qid)


if __name__ == "__main__":
    from app import create_app
    app = create_app()

    with app.app_context():
        enhance_visual_sample()