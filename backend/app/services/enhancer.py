from app.models import Question
from app.extensions import db
from app.ai.gemini import gemini_ai


def enhance_question_with_gemini_html(question_id):
    """Regenerate the question using Gemini with beautifully formatted HTML."""
    question = Question.query.get(question_id)
    if not question:
        return False

    prompt = f"""
    Generate a professionally formatted HTML coding interview question for the problem titled "{question.title}". This is a {question.difficulty} level question related to {question.topic}.

    Format the output as clean HTML that can be directly rendered on a web application. Do NOT include any markdown formatting, bullet points with asterisks, or code template.

    The HTML must include:

    1. A <h2> for the title
    2. A <p><strong>Difficulty:</strong> ...</p>
    3. A <p><strong>Topic:</strong> ...</p>
    4. A <h3>Description</h3> followed by <p> tags for the full description
    5. A <h3>Examples</h3> section using <div class="example-block"> for each example:
    - Highlight **Input**, **Output**, and **Explanation** using <strong> tags
    6. A <h3>Constraints</h3> section using <ul><li>...</li></ul>
    7. A <h3>Expected Complexity</h3> section with <p> for time and space complexity
    8. A <h3>Notes</h3> section for any extra hints or edge case remarks
    9. Do NOT include a code template or sample function signature

    Ensure proper indentation and visual readability.
    """

    try:
        response = gemini_ai.generate_content(prompt)
        response_json = gemini_ai.extract_json_from_response(response)
        question.content = response_json.get("content", question.content)
        db.session.commit()
        return True
    except Exception as e:
        print(f"❌ Failed to format with Gemini: {e}")
        return False


def enhance_sample_questions():
    """Run Gemini-based enhancement on 5 selected questions for preview."""
    sample_ids = [1, 2, 3, 4, 5]  # Replace with actual question IDs
    enhanced = 0

    for qid in sample_ids:
        print(f"🔄 Enhancing question ID: {qid}")
        success = enhance_question_with_gemini_html(qid)
        if success:
            print(f"✅ Enhanced question {qid}")
            enhanced += 1
        else:
            print(f"❌ Failed to enhance question {qid}")

    print(f"\n✅ Completed: {enhanced}/{len(sample_ids)} questions enhanced with Gemini HTML.")


if __name__ == "__main__":
    from app import create_app

    app = create_app()
    with app.app_context():
        enhance_sample_questions()