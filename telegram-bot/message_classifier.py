import openai
from datetime import datetime
import os


openai.api_key = os.getenv("OPENAI_API_KEY")


def classify_message(message):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": generate_prompt(message)}
            ],
            temperature=0
        )

        # Get the classified response
        classified_text = response.choices[0].message.content.strip()
        print(f"Classified text: {classified_text}")

        try:
            classified_json = eval(classified_text)
        except:
            print("Error parsing the response to JSON.")
            return None

        if classified_json.get('type') == 'signal':
            signal_data = extract_signal_details(classified_json)
            return 'signal', signal_data
        elif classified_json.get('type') == 'news':
            news_data = {
                'news': classified_json.get('message'),
                'timestamp': int(datetime.now().timestamp())
            }
            return 'news', news_data
        elif classified_json.get('type') == 'null':
            return None, None
        else:
            return None

    except Exception as e:
        print(f"Error during classification: {e}")
        return None


def generate_prompt(message):
    """
    Generate the prompt for OpenAI model to classify the message and return a JSON-like structure.
    Args:
    - message (str): The message text to be classified.

    Returns:
    - str: The formatted prompt for the OpenAI API.
    """
    return f"""
    Classify the following message as either a 'signal' for a trade, 'news' about crypto, or 'null' if it doesn't fit either category:

    Message: "{message}"

    If it is a 'signal', return the following JSON:
    {{
        "type": "signal",
        "symbol": "XXXUSDT",  # The trading pair (e.g., 'BTCUSDT', 'ETHUSDT')
        "entry": "entry price",  # The price entry point
        "stop_loss": "stop loss price",  # The stop loss price, or 4% lower than the entry price if not specified
        "take_profit": "take profit price"  # The take profit price, or 4% higher than the entry price if not specified
    }}

    If it is 'news', return the following JSON:
    {{
        "type": "news",
        "message": "{message}"
    }}

    If it is 'null' (neither a signal nor news), return the following JSON:
    {{
        "type": "null"
    }}
    """


def extract_signal_details(classified_json):
    """
    Extract the trade signal details from the classified JSON.
    Args:
    - classified_json (dict): The dictionary containing signal information.

    Returns:
    - dict: The signal details extracted from the text.
    """
    signal_data = {
        'type': classified_json.get('type'),
        'symbol': classified_json.get('symbol'),
        'entry': float(classified_json.get('entry', 0)),
        'stop_loss': float(classified_json.get('stop_loss', 0)),
        'take_profit': float(classified_json.get('take_profit', 0)),
        'timestamp': int(datetime.now().timestamp())
    }
    return signal_data
