# """
# AI integration with Gemini for InterPrep-AI Next Generation.
# """
# import os
# import google.generativeai as genai
# from ..config import Config

# # Configure the Gemini API
# genai.configure(api_key=Config.GOOGLE_API_KEY)

# def generate_question(topic, difficulty, company=None):
#     """Generate a coding question using Gemini."""
#     print(f"🔮 Generating question for topic={topic}, difficulty={difficulty}, company={company}")
#     # Create the prompt
#     prompt = f"Generate a {difficulty} difficulty coding interview question about {topic}"
#     if company:
#         prompt += f" that might be asked at {company}"
    
#     # Generate the question
#     model = genai.GenerativeModel(Config.GENERATIVE_MODEL_NAME)
#     response = model.generate_content(prompt)
    
#     # Parse the response
#     question_text = response.text
    
#     # Extract title and content
#     lines = question_text.split('\n')
#     title = lines[0].strip()
#     content = '\n'.join(lines[1:]).strip()
    
#     # Generate code template
#     template_prompt = f"Create a code template for this question: {title}\n{content}"
#     template_response = model.generate_content(template_prompt)
#     code_template = template_response.text
    
#     # Generate solution
#     solution_prompt = f"Provide a solution for this question: {title}\n{content}"
#     solution_response = model.generate_content(solution_prompt)
#     solution = solution_response.text
    
#     # Generate test cases
#     test_prompt = f"Generate 3 test cases for this question: {title}\n{content}"
#     test_response = model.generate_content(test_prompt)
#     test_cases = test_response.text
    
#     return {
#         'title': title,
#         'content': content,
#         'difficulty': difficulty,
#         'topic': topic,
#         'company': company,
#         'code_template': code_template,
#         'solution': solution,
#         'test_cases': [test_cases]
#     }

# def evaluate_solution(question, code, language, solution=None, test_cases=None):
#     """Evaluate a solution using Gemini."""
#     # Create the prompt
#     prompt = f"""
#     Question: {question}
    
#     User's solution ({language}):
#     ```{language}
#     {code}
#     ```
    
#     Evaluate this solution for correctness, efficiency, and code quality.
#     """
    
#     if solution:
#         prompt += f"""
#         Reference solution:
#         ```
#         {solution}
#         ```
#         """
    
#     if test_cases:
#         prompt += f"""
#         Test cases:
#         {test_cases}
#         """
    
#     # Generate the evaluation
#     model = genai.GenerativeModel(Config.GENERATIVE_MODEL_NAME)
#     response = model.generate_content(prompt)
    
#     # Parse the response
#     evaluation_text = response.text
    
#     # Determine status based on evaluation
#     status = 'accepted'
#     if 'incorrect' in evaluation_text.lower() or 'wrong' in evaluation_text.lower():
#         status = 'wrong_answer'
#     elif 'time limit' in evaluation_text.lower() or 'too slow' in evaluation_text.lower():
#         status = 'time_limit_exceeded'
#     elif 'memory limit' in evaluation_text.lower() or 'too much memory' in evaluation_text.lower():
#         status = 'memory_limit_exceeded'
    
#     return {
#         'status': status,
#         'feedback': evaluation_text,
#         'runtime': None,  # Not available without actual execution
#         'memory': None    # Not available without actual execution
#     }
# def generate_similar_question(title, content, difficulty, topic):
#     """Generate a similar question using the existing one as context."""
#     prompt = (
#         f"Generate a different {difficulty} coding question similar to this one on {topic}:\n"
#         f"Title: {title}\n"
#         f"Content: {content}\n"
#         f"Do not repeat the same question. Keep difficulty level and topic consistent."
#     )

#     model = genai.GenerativeModel(Config.GENERATIVE_MODEL_NAME)
#     response = model.generate_content(prompt)
#     question_text = response.text

#     lines = question_text.split('\n')
#     new_title = lines[0].strip()
#     new_content = '\n'.join(lines[1:]).strip()

#     return {
#         'title': new_title,
#         'content': new_content
#     }

"""
Gemini API integration for InterPrep-AI Next Generation.
"""
import os
import json
import re
from typing import Dict, List, Any, Optional

from ..services.retriever import find_similar_questions
import google.generativeai as genai
from ..extensions import db
from ..models.question import Question
from ..models.learning import LearningTopic, LearningContent


class GeminiAI:
    """Class for interacting with Google's Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini API client."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_content(self, prompt: str) -> str:
        """Generate content using Gemini API."""
        response = self.model.generate_content(prompt)
        return response.text

    def extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON from a text response."""
        try:
            # Try to find JSON in code blocks
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response_text)
            if json_match:
                json_str = json_match.group(1)
            else:
                # If no code blocks, try to parse the entire response
                json_str = response_text
            
            # Clean up the string and parse JSON
            json_str = json_str.strip()
            return json.loads(json_str)
        except Exception as e:
            print(f"Error extracting JSON: {str(e)}")
            raise ValueError(f"Failed to extract JSON from response: {str(e)}")


# Initialize the GeminiAI instance
gemini_ai = GeminiAI()


def generate_question(topic: str, difficulty: str, company: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate an interview question using Gemini API.
    
    Args:
        topic (str): The topic for the question (e.g., arrays, linked_lists)
        difficulty (str): The difficulty level (e.g., easy, medium, hard)
        company (str, optional): Target company for the question
    
    Returns:
        dict: Generated question with title, description, examples, constraints
    """
    # Craft a detailed prompt
    company_context = f"commonly asked at {company}" if company else "commonly asked in technical interviews"
    
    prompt = f"""
    Generate a detailed {difficulty} level coding interview question about {topic} that is {company_context}.
    
    The question should include:
    1. A clear title
    2. A detailed problem description
    3. At least 2 examples with input and expected output
    4. Constraints on the input
    5. Expected time and space complexity requirements
    
    Format the response as a JSON object with the following structure:
    {{
        "title": "Question title",
        "description": "Detailed problem description",
        "examples": [
            {{"input": "Example input 1", "output": "Expected output 1"}},
            {{"input": "Example input 2", "output": "Expected output 2"}}
        ],
        "constraints": ["Constraint 1", "Constraint 2"],
        "difficulty": "{difficulty}",
        "topic": "{topic}",
        "company": "{company if company else 'general'}",
        "expected_complexity": {{"time": "e.g., O(n)", "space": "e.g., O(1)"}}
    }}
    
    Ensure the question is challenging but solvable, and relevant to the topic and difficulty level.
    """
    
    try:
        # Generate content
        response_text = gemini_ai.generate_content(prompt)

        print("🔁 Gemini raw response:\n", response_text) ## Debugging
        # Parse the response to extract JSON
        question_data = gemini_ai.extract_json_from_response(response_text)
        
        return question_data
        
    except Exception as e:
        print(f"Error generating question: {str(e)}")
        # Return a fallback question if generation fails
        return {
            "title": f"{difficulty.capitalize()} {topic.replace('_', ' ').title()} Problem",
            "description": f"There was an error generating a question. Please try again.",
            "examples": [{"input": "Example", "output": "Example"}],
            "constraints": ["None"],
            "difficulty": difficulty,
            "topic": topic,
            "company": company if company else "general",
            "expected_complexity": {"time": "Unknown", "space": "Unknown"}
        }


def generate_similar_question(question_id: int) -> Dict[str, Any]:
    """
    Generate a similar question to an existing one.
    
    Args:
        question_id (int): ID of the existing question
    
    Returns:
        dict: Generated similar question
    """
    # Get the original question
    original_question = Question.query.get(question_id)
    if not original_question:
        raise ValueError(f"Question with ID {question_id} not found")
    
    # Craft a prompt for generating a similar question
    prompt = f"""
    Generate a coding interview question similar to the following question but with different specifics:
    
    Original Question:
    Title: {original_question.title}
    Description: {original_question.description}
    Topic: {original_question.topic}
    Difficulty: {original_question.difficulty}
    
    Create a new question with the same topic and difficulty, but with a different problem statement and examples.
    
    Format the response as a JSON object with the following structure:
    {{
        "title": "New question title",
        "description": "Detailed problem description",
        "examples": [
            {{"input": "Example input 1", "output": "Expected output 1"}},
            {{"input": "Example input 2", "output": "Expected output 2"}}
        ],
        "constraints": ["Constraint 1", "Constraint 2"],
        "difficulty": "{original_question.difficulty}",
        "topic": "{original_question.topic}",
        "company": "{original_question.company if original_question.company else 'general'}",
        "expected_complexity": {{"time": "e.g., O(n)", "space": "e.g., O(1)"}}
    }}
    """
    
    try:
        # Generate content
        response_text = gemini_ai.generate_content(prompt)
        
        # Parse the response to extract JSON
        question_data = gemini_ai.extract_json_from_response(response_text)
        
        return question_data
        
    except Exception as e:
        print(f"Error generating similar question: {str(e)}")
        raise


def evaluate_solution(question: str, solution: str, language: str = "python") -> Dict[str, Any]:
    """
    Evaluate a solution to a coding question.
    
    Args:
        question (str): The question description
        solution (str): The submitted solution code
        language (str): The programming language of the solution
    
    Returns:
        dict: Evaluation results including correctness, feedback, and suggestions
    """
    prompt = f"""
    Evaluate the following {language} solution to this coding problem:
    
    PROBLEM:
    {question}
    
    SOLUTION:
    ```{language}
    {solution}
    ```
    
    Provide a detailed evaluation including:
    1. Is the solution correct? (yes/no/partially)
    2. Does it handle all edge cases?
    3. What is the time complexity?
    4. What is the space complexity?
    5. Are there any bugs or issues?
    6. How can the solution be improved?
    
    Format your response as a JSON object with the following structure:
    {{
        "correctness": "yes/no/partially",
        "time_complexity": "e.g., O(n)",
        "space_complexity": "e.g., O(1)",
        "handles_edge_cases": true/false,
        "bugs": ["Bug description 1", "Bug description 2"],
        "feedback": "Detailed feedback on the solution",
        "improvements": ["Improvement suggestion 1", "Improvement suggestion 2"],
        "score": 0-100
    }}
    """
    
    try:
        # Generate content
        response_text = gemini_ai.generate_content(prompt)
        
        # Parse the response to extract JSON
        evaluation_data = gemini_ai.extract_json_from_response(response_text)
        
        return evaluation_data
        
    except Exception as e:
        print(f"Error evaluating solution: {str(e)}")
        # Return a fallback evaluation if generation fails
        return {
            "correctness": "unknown",
            "time_complexity": "unknown",
            "space_complexity": "unknown",
            "handles_edge_cases": False,
            "bugs": ["Could not analyze solution"],
            "feedback": "There was an error evaluating your solution. Please try again.",
            "improvements": ["N/A"],
            "score": 0
        }


def generate_learning_content(topic: str, subtopic: str = None) -> Dict[str, Any]:
    """
    Generate learning content for a specific topic.
    
    Args:
        topic (str): The main topic (e.g., arrays, linked_lists)
        subtopic (str, optional): A specific subtopic
    
    Returns:
        dict: Generated learning content
    """
    subtopic_text = f" focusing on {subtopic}" if subtopic else ""
    
    prompt = f"""
    Create comprehensive learning content about {topic}{subtopic_text} for interview preparation.
    
    The content should include:
    1. A clear explanation of the concept
    2. Key techniques and patterns
    3. Common interview questions related to this topic
    4. Code examples demonstrating the concepts
    5. Time and space complexity analysis
    
    Format the response as a JSON object with the following structure:
    {{
        "title": "Topic title",
        "introduction": "Brief introduction to the topic",
        "key_concepts": [
            {{"concept": "Concept 1", "explanation": "Detailed explanation"}},
            {{"concept": "Concept 2", "explanation": "Detailed explanation"}}
        ],
        "techniques": [
            {{"name": "Technique 1", "description": "How and when to use it", "code_example": "Code snippet"}},
            {{"name": "Technique 2", "description": "How and when to use it", "code_example": "Code snippet"}}
        ],
        "common_questions": [
            {{"question": "Question 1", "approach": "How to approach it"}},
            {{"question": "Question 2", "approach": "How to approach it"}}
        ],
        "complexity_analysis": "Explanation of time and space complexity considerations",
        "additional_resources": ["Resource 1", "Resource 2"]
    }}
    """
    
    try:
        # Generate content
        response_text = gemini_ai.generate_content(prompt)
        
        # Parse the response to extract JSON
        content_data = gemini_ai.extract_json_from_response(response_text)
        
        return content_data
        
    except Exception as e:
        print(f"Error generating learning content: {str(e)}")
        raise

def rag_enhanced_question_generation(topic: str, difficulty: str, company: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a question using RAG (Retrieval-Augmented Generation).
    """
    similar_questions = find_similar_questions(
        question_text=f"{topic} {difficulty} coding question",
        n=3,
        topic=topic,
        difficulty=difficulty,
        company=company
    )
    
    context = "Here are some similar questions for reference:\n\n"
    for i, q in enumerate(similar_questions):
        context += f"{i+1}. {q['Title']}\n"
        context += f"Topic: {q['Topic']}, Difficulty: {q['Difficulty']}\n"
        context += f"Description: {q.get('Content', '')[:200]}...\n\n"
    
    company_context = f"commonly asked at {company}" if company else "commonly asked in technical interviews"
    
    prompt = f"""
    Using the following reference materials as context, generate a detailed {difficulty} level coding interview question about {topic} that is {company_context}.
    
    CONTEXT:
    {context}
    
    The question should include:
    1. A clear title
    2. A detailed problem description
    3. At least 2 examples with input and expected output
    4. Constraints on the input
    5. Expected time and space complexity requirements
    
    Format the response as a JSON object with the following structure:
    {{
        "title": "Question title",
        "content": "Detailed problem description",
        "examples": [
            {{"input": "Example input 1", "output": "Expected output 1"}},
            {{"input": "Example input 2", "output": "Expected output 2"}}
        ],
        "constraints": ["Constraint 1", "Constraint 2"],
        "difficulty": "{difficulty}",
        "topic": "{topic}",
        "company": "{company if company else 'general'}",
        "expected_complexity": {{"time": "e.g., O(n)", "space": "e.g., O(1)"}}
    }}
    """
    
    try:
        response_text = gemini_ai.generate_content(prompt)
        return gemini_ai.extract_json_from_response(response_text)
    except Exception as e:
        print(f"Error generating RAG question: {str(e)}")
        return generate_question(topic, difficulty, company)

