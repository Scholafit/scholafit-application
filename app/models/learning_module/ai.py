from anthropic import Anthropic
import os

# client = Anthropic(
#     api_key= os.getenv("ANTHROPIC_API_KEY")
# )

def generate_questions(subject:str, number_of_questions: int, client:Anthropic):
    print('Generating questions')
    SYSTEM_MESSAGE = f"You are an expert in creating POST-UTME {subject} examination questions for Nigerian universities. Your task it to generate high-quality, questions that assess the {subject} subject proficiency and readiness for higher education in Nigeria."

    PROMPT_MESSAGE = f"""Generate {number_of_questions} POST-UTME {subject} questions for Nigerian universities.
        Please structure each question as a JSON object with the following fields:
            - subject_name: represents the subject the question belongs to
            - type: The type of question (e.g., "multiple_choice", "passage_based")
            - if subject is English and has a passage, include a passage: full passage text. The passage can have more than one question based on the passage.

            - questions: An array of question objects in this format 
                {{
                    "question": "str",
                    "answers": [
                {{"choice": "str", "is_correct_answer": "True/False"}}
        ]
                }}
            - answers are multiple choice questions
            - explanation: A brief explanation of why the answer is correct
            - questions should be a mix of easy, medium and hard difficulty levels 
            Return all questions in a single JSON array."""

    TEMPERATURE = 0.6

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": PROMPT_MESSAGE},
                {"role": "assistant", "content": SYSTEM_MESSAGE}
            ],
            temperature=TEMPERATURE
        )
        return message
    except Exception as err:
        print(str(err))
