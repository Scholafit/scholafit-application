from anthropic import Anthropic
import os

# client = Anthropic(
#     api_key= os.getenv("ANTHROPIC_API_KEY")
# )

def create_anthropic_client():
    #throw exception if api_key is unavailable
    api_key = os.getenv("ANTHROPIC_API_KEY")
    return Anthropic(api_key=api_key)


class AI:

    TEMPERATURE = 0.6
    def __init__(self, redis_client, gpt_client):
        self._redis_client = redis_client
        self._gpt_client = gpt_client

    def send_prompt(self, prompt_message: str, system_message: str):
        try:
            message = self._gpt_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt_message},
                    {"role": "assistant", "content": system_message}
                ],
                temperature=self.TEMPERATURE
            )
            return message
        except Exception as err:
            print(str(err))

    
    def generate_questions(self, subject:str, number_of_questions: int):
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
                - one of the answers has to be the correct answer and marked as true while rest are false
                - explanation: A brief explanation of why the answer is correct
                - questions should be a mix of easy, medium and hard difficulty levels 
                Return all questions in a single JSON array."""
        return self.send_prompt(PROMPT_MESSAGE, SYSTEM_MESSAGE)




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
            - one of the answers has to be the correct answer and marked as true while rest are false
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
