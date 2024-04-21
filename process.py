from openai import OpenAI
from groq import Groq

def get_chatgpt_response(question, api_key):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": question}
    ]
    )
    #print(completion.choices[0].message)
    return str(completion.choices[0].message.content).strip()

def get_groq_response(question, api):
    
    client = Groq(
        api_key=api,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="mixtral-8x7b-32768",
    )

    return str(chat_completion.choices[0].message.content)