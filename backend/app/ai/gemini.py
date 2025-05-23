"""
AI integration with Gemini for InterPrep-AI Next Generation.
"""
import os
import google.generativeai as genai
from ..config import Config

# Configure the Gemini API
genai.configure(api_key=Config.GOOGLE_API_KEY)

def generate_question(topic, difficulty, company=None):
    """Generate a coding question using Gemini."""
    print(f"🔮 Generating question for topic={topic}, difficulty={difficulty}, company={company}")
    # Create the prompt
    prompt = f"Generate a {difficulty} difficulty coding interview question about {topic}"
    if company:
        prompt += f" that might be asked at {company}"
    
    # Generate the question
    model = genai.GenerativeModel(Config.GENERATIVE_MODEL_NAME)
    response = model.generate_content(prompt)
    
    # Parse the response
    question_text = response.text
    
    # Extract title and content
    lines = question_text.split('\n')
    title = lines[0].strip()
    content = '\n'.join(lines[1:]).strip()
    
    # Generate code template
    template_prompt = f"Create a code template for this question: {title}\n{content}"
    template_response = model.generate_content(template_prompt)
    code_template = template_response.text
    
    # Generate solution
    solution_prompt = f"Provide a solution for this question: {title}\n{content}"
    solution_response = model.generate_content(solution_prompt)
    solution = solution_response.text
    
    # Generate test cases
    test_prompt = f"Generate 3 test cases for this question: {title}\n{content}"
    test_response = model.generate_content(test_prompt)
    test_cases = test_response.text
    
    return {
        'title': title,
        'content': content,
        'difficulty': difficulty,
        'topic': topic,
        'company': company,
        'code_template': code_template,
        'solution': solution,
        'test_cases': [test_cases]
    }

def evaluate_solution(question, code, language, solution=None, test_cases=None):
    """Evaluate a solution using Gemini."""
    # Create the prompt
    prompt = f"""
    Question: {question}
    
    User's solution ({language}):
    ```{language}
    {code}
    ```
    
    Evaluate this solution for correctness, efficiency, and code quality.
    """
    
    if solution:
        prompt += f"""
        Reference solution:
        ```
        {solution}
        ```
        """
    
    if test_cases:
        prompt += f"""
        Test cases:
        {test_cases}
        """
    
    # Generate the evaluation
    model = genai.GenerativeModel(Config.GENERATIVE_MODEL_NAME)
    response = model.generate_content(prompt)
    
    # Parse the response
    evaluation_text = response.text
    
    # Determine status based on evaluation
    status = 'accepted'
    if 'incorrect' in evaluation_text.lower() or 'wrong' in evaluation_text.lower():
        status = 'wrong_answer'
    elif 'time limit' in evaluation_text.lower() or 'too slow' in evaluation_text.lower():
        status = 'time_limit_exceeded'
    elif 'memory limit' in evaluation_text.lower() or 'too much memory' in evaluation_text.lower():
        status = 'memory_limit_exceeded'
    
    return {
        'status': status,
        'feedback': evaluation_text,
        'runtime': None,  # Not available without actual execution
        'memory': None    # Not available without actual execution
    }
def generate_similar_question(title, content, difficulty, topic):
    """Generate a similar question using the existing one as context."""
    prompt = (
        f"Generate a different {difficulty} coding question similar to this one on {topic}:\n"
        f"Title: {title}\n"
        f"Content: {content}\n"
        f"Do not repeat the same question. Keep difficulty level and topic consistent."
    )

    model = genai.GenerativeModel(Config.GENERATIVE_MODEL_NAME)
    response = model.generate_content(prompt)
    question_text = response.text

    lines = question_text.split('\n')
    new_title = lines[0].strip()
    new_content = '\n'.join(lines[1:]).strip()

    return {
        'title': new_title,
        'content': new_content
    }