import json
import boto3
import os

# QUEUE_URL = os.environ['QUEUE_URL']
QUEUE_URL = "https://sqs.eu-central-1.amazonaws.com/058264391934/SecondQueue"
sqs = boto3.client("sqs")
bedrock = boto3.client("bedrock-runtime")
# event = {'Records': [{'messageId': '9dc2f420-9b16-48d3-8a88-ed45aa8e1686', 'receiptHandle': 'AQEBM0bj1b4uvoNJhjNkZUJYxS5zK/AXY5ngyD1h3NA53Ht+JY3gY5cAn8jPi7Cy9HgPjEijvMaT0ddKGkQd/iDKiClYkBVDYPlR3x5qoJ59WFgZ+Vr3D9A12f3pcqSC0+sBSiyfwM5E8PiG3/JbpDXWuCuDKQC4dt7sVGMqpFfUF4PtLZExiwb9XLpm5ClJLc5UaIvW5yyzuERyl6J5cOvQEM4z3RWravPazoAPiuPZthxinJfNQdKejpsjdHO1prfmppuZB5lDD2C5HEB0b6mXSe+60GJreXgz40QYKDcB/At8U8caUtY/B37QdhKayXCeKJWc7cneHByrQUsLu0NKrZI7D9R3cfdqna+s2F+LepA/N7zRH2upidIxd8VTXPqzO4hEkzZi3cotXs71C+UeWQ==', 'body': 'qwerty', 'attributes': {'ApproximateReceiveCount': '1', 'SentTimestamp': '1724664588679', 'SenderId': 'AROAQ3EGUCD7FJTAMPWEL:bikash.padhiari@3gi.co.uk', 'ApproximateFirstReceiveTimestamp': '1724664588684'}, 'messageAttributes': {}, 'md5OfBody': 'd8578edf8458ce06fbc5bb76a58c5ca4', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:eu-central-1:058264391934:FirstQueue', 'awsRegion': 'eu-central-1'}]}
def handler(event, context):
    print(f"TYPE OF EVENT: {type(event)}")
    print("First Lambda received an event: ", event)
    records = event.get('Records', [])
        
        # Iterate over each record in 'Records'
    for record in records:
        # Extract the 'body' from the current record
        body = record.get('body', None)
    print("Body: ", body)
    user_input = body
    prompt = f"""
    As an AI, you are tasked with monitoring and detecting any instances of misuse or unethical behavior. Please evaluate the following input provided by a user and determine if there is any misuse of AI or unethical practices involved:
    
    User Input:
    "{user_input}"
    
    Evaluate the input and provide a detailed explanation of your assessment, including any specific aspects that raise concerns:
    
    1. Does the input involve using AI to deceive or manipulate individuals?
    2. Is the AI being used in a manner that could cause harm, either physically, emotionally, or financially, to any individuals or groups?
    3. Are there any privacy or security concerns related to the use of AI in this input?
    4. Is the AI being used to generate or distribute misinformation or harmful content?
    5. Does the input involve any unauthorized access to or misuse of data?
    6. Is the AI being used in a way that violates any laws, regulations, or ethical guidelines?
    
    Please analyze and explain any potential issues you identify, and suggest how the AI could be used more responsibly in this context.
    """
    print(prompt)
    send_message(prompt)

def send_message(message):
    response = sqs.send_message(
        MessageBody=message,
        QueueUrl=QUEUE_URL
    )
    return response
    
def bedrock_invoke(prompt):
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }
    
    # Convert the native request to JSON.
    request = json.dumps(native_request)
    response = bedrock.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    
    # Extract and print the response text.
    response_text = model_response["content"][0]["text"]
    print(response_text)
            
            
    return response_text
