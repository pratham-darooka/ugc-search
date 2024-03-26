import google.generativeai as genai
import json
from globals import GOOGLE_API_KEY
from prompts import REWRITE_QUERY_FOR_REDDIT, REWRITE_QUERY_FOR_YT

def rewrite_yt_query(user_request: str) -> str:
    genai.configure(api_key=GOOGLE_API_KEY)

    # Set up the model
    generation_config = {
    "temperature": 0,
    "top_p": 0,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    convo = model.start_chat(history=[
    ])

    convo.send_message(REWRITE_QUERY_FOR_YT.format(user_request=user_request))

    new_query = json.loads(convo.last.text)['new_query']

    return new_query

def rewrite_reddit_query(user_request: str) -> str:
    genai.configure(api_key=GOOGLE_API_KEY)

    # Set up the model
    generation_config = {
    "temperature": 0,
    "top_p": 0,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    convo = model.start_chat(history=[
    ])

    convo.send_message(REWRITE_QUERY_FOR_REDDIT.format(user_request=user_request))

    new_query = json.loads(convo.last.text)['new_query']

    return new_query
