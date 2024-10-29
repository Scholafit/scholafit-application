from anthropic import Anthropic
import anthropic
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
    def __init__(self, gpt_client):
        self._gpt_client = gpt_client

    def send_prompt(self, prompt_message: str, system_message: str):
        print(f'sending prompt: {prompt_message}')
        try:
            message = self._gpt_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=2000,
                messages=[
                    {"role": "assistant", "content": system_message},
                    {"role": "user", "content": prompt_message}
                ],
                temperature=self.TEMPERATURE
            )
            return message
        except anthropic.APIError as e:
            if e.status_code == 429:
                print('Rate limit exceeded. Please wait and try again')
            elif e.status_code == 401:
                print('Authentication Error. Check API Key')
            elif e.status_code == 400:
                print(f'Bad request: {e.message}')
            else:
                print(f'API Error: {e}')

        except Exception as err:
            print(str(err))

    def send_follow_up_prompt(self, messages:list):
        try:
            message = self._gpt_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=2000,
                messages=messages,
                temperature=self.TEMPERATURE
            )
            return message
        except anthropic.APIError as e:
            if e.status_code == 429:
                print('Rate limit exceeded. Please wait and try again')
            elif e.status_code == 401:
                print('Authentication Error. Check API Key')
            elif e.status_code == 400:
                print(f'Bad request: {e.message}')
            else:
                print(f'API Error: {e}')

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
                - make sure each question is unique
                Return all questions in a single VALID JSON array. Every thing should be well terminated"""
        return self.send_prompt(PROMPT_MESSAGE, SYSTEM_MESSAGE)

    def ai_chat(self, prompt_message: str):
        
        SYSTEM_MESSAGE = f"""You are a university lecturer in Nigeria. Your task is to help students prepare for the POST-UTME exams. Answer questions they ask and provide guidance. As part of the answer, provide a title that summarizes your response or summarizes the topic that the student has asked about.Provide a subject tag. That states which subject the question belongs.
        Available UTME subjects are:
        subjects = ['Mathematics', 'english','physics', 'accounting', 'chemistry', 'commerce', 'animal husbandry', 'fishery', 'agricultural science', 'economics', 'geography', 'further mathematics', 'literature in English', 'government']. 
        If the question does not fit into any of this subjects, the subject can be left blank
       
            IMPORTANT: Your response MUST be a valid JSON object with the following structure:
            {{
                "title": "summary of question/topic asked",
                "subject":"subjects"/None
                "response": "your response to the question"
            }}

            Ensure that:
            1. The entire response is a single JSON object.
            2. Both "title" and "response" keys are in double quotes.
            3. The values for both keys are strings enclosed in double quotes.
            4. Any double quotes within the text are escaped with a backslash (\\).
            5. Avoid using single quotes, newline characters, or any other special characters that might break the JSON structure.

            Example of correct formatting:
            {{
                "title": "Example Topic",
                "response": "This is an example response. Notice how \\"quotes\\" are escaped."
            }}
            """.rstrip()
       
        return self.send_prompt(prompt_message, SYSTEM_MESSAGE)
        

    def continue_chat_ai(self, prompt_message: str,data:list):
       
        SYSTEM_MESSAGE = f"""You are a university lecturer in Nigeria. Your task is to help students prepare for the POST-UTME exams. Answer questions they ask and provide guidance.
        You can reference other parts of the conversation that you have already had with the student in the chat history sent with the new question.
            IMPORTANT: Your response MUST be a valid JSON object with the following structure:
            {{
                "response": "your response to the question"
            }}

            Ensure that:
            1. The entire response is a single JSON object.
            2. "response" key in double quotes.
            3. The value for the key is a string enclosed in double quotes.
            4. Any double quotes within the text are escaped with a backslash (\\).
            5. Avoid using single quotes, newline characters, or any other special characters that might break the JSON structure.

            Example of correct formatting:
            {{
                "response": "This is an example response. Notice how \\"quotes\\" are escaped."
            }}
            """.rstrip()
        
        messages = []
        for x in range(len(data) - 1):
            data_point = data[x]
            messages.append({
                "role": "assistant",
                "content": data_point["assistant"]
            })
            messages.append({
                "role": "user",
                "content": data_point["user"]
            })
        
        messages.append({
            "role": "assistant",
            "content": SYSTEM_MESSAGE
        })
        messages.append({
            "role": "user",
            "content": prompt_message
        })
        print(messages)
        return self.send_follow_up_prompt(messages)
            





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

