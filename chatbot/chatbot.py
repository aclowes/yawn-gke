# TODO:
#   Tell it we have beer and sake, but don't talk about it unless they ask
#   Include URL?
#   Structured response with URL, price, photo URL, description why.

import os

import gradio

from openai import OpenAI
from openai.types.responses.response_prompt_param import ResponsePromptParam
from openai.types.responses.response_input_param import EasyInputMessageParam

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)


def predict(message, history):
    print(f"User input: {message}")
    response = client.responses.create(
        model="gpt-4.1",
        prompt=ResponsePromptParam(id="pmpt_68571d5f865881938d46b7a7defc77c100c288bd4c2fc620"),
        input=[EasyInputMessageParam(content=row['content'], role=row['role']) for row in history]
              + [EasyInputMessageParam(content=message, role='user')],
        # TODO utilize previous_response_id and stream
    )

    print(f"Consumed {response.usage.total_tokens} tokens")
    return response.output_text


demo = gradio.ChatInterface(
    predict,
    type="messages",
    examples=["Recommend a Sardinian red, please!", "What kind of sake and beer do you have?",
              "Is there a creamy white from Italy?"],
    css="footer {display:none !important}",
    save_history=True,
    cache_examples=True,
    cache_mode="lazy",
    title="Welcome to Bevi Bene's Sommelier Chatbot"
)

demo.launch()
