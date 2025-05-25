from app.models import Question
from app.extensions import db
from dotenv import load_dotenv
import re
import time

load_dotenv()

def regenerate_question_with_visual_formatting(question_id):
    from app.ai.gemini import gemini_ai  # Local import to avoid circular import

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
            raise ValueError("Empty or malformed response from Gemini.")

        # Remove markdown code fences like ```html ... ```
        cleaned = re.sub(r"^```html\s*|```$", "", response.strip(), flags=re.MULTILINE)

        question.content = cleaned
        db.session.commit()
        print(f"✅ Regenerated: {question.id} — {question.title}")
        return True

    except Exception as e:
        print(f"❌ Error for Q{question.id}: {e}")
        return False


def regenerate_all_questions():
    questions = Question.query.order_by(Question.id).all()
    total = len(questions)
    count = 0

    for i, q in enumerate(questions, 1):
        print(f"\n🔄 [{i}/{total}] {q.title}")
        if regenerate_question_with_visual_formatting(q.id):
            count += 1
        if i % 10 == 0:
            db.session.commit()
            time.sleep(2)  # optional rate limiting

    db.session.commit()
    print(f"\n✅ Regenerated {count}/{total} questions.")

if __name__ == "__main__":
    from app import create_app
    app = create_app()

    with app.app_context():
        regenerate_all_questions()