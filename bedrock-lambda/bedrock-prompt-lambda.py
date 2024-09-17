import json
import boto3
import os

sqs = boto3.client("sqs")
bedrock = boto3.client("bedrock-runtime")

def handler(event, context):
    print("Second Lambda received an event: ", event)
    records = event.get('Records', [])
    for record in records:
        print("-------------")
        # Extract the 'body' from the current record
        body = record.get('body', None)
    prompt = write_prompt(body)
    response = bedrock_invoke(prompt)
    # response = "Bedrock function call is commented."
    print(response)
    return response
    
    

def write_prompt(message):
    prompt = f"""You are tasked with compiling a comprehensive report for an In-House Health Audit. Your role involves analyzing and synthesizing the information provided based on the guidance and evaluation criteria we outline.\n
    
    **GRADING SYSTEM**
    Each response to the audit questions is graded on a scale of A, B, C, or D, as defined:
    
    A = Fully in Place
    An outstanding result was achieved overall
    Excellent function
    
    B = Partially in Place
    Clear indication of some implementation
    Some weaknesses due to projects not being implemented organization-wide or practiced fully
    
    C = Considered
    Some signs of development
    Occasional review of the improvements achieved
    
    D = Not Started
    No activities engaged with
    
    **SCORING SYSTEM**
    Based on the M.E.T.A Wellbeing RISK Audit scoring system, here is the percentage-based likelihood of successful health promotion within the organization:

    - **0-20% (NO to LOW)**: Reflects a minimal chance of successful health promotion and engagement with health initiatives.
    - **21-40% (LOW to AVERAGE)**: Indicates some basic levels of implementation, but significant gaps remain.
    - **41-60% (AVERAGE)**: Shows the company is making progress with its wellbeing initiatives, but some key areas require more attention.
    - **61-80% (AVERAGE to HIGH)**: Suggests that the organization has implemented many successful measures but still has room to improve in some areas.
    - **81-100% (HIGH)**: Demonstrates an excellent chance of success in health promotion, with most programs in place and operating effectively.
    
    **INSTRUCTIONS**
    Your report should cover the each section, each containing multiple questions and their corresponding graded responses. For each section, you will:
    Summarize the overall performance based on the grades.
    Highlight key strengths and areas for improvement, referencing specific responses.
    Provide actionable recommendations where needed.\n Generate the response in the following structure:\n
    #Structure#
    Overall Grading : *(overall grade)*
    
    Section 1: *Information*
    Grade: *Grade for current section*
    Overall Score: *Score for current section*
    Strengths: *Information*
    Areas for improvement: *Information*
    Recommendations: *Information*
    
    Section 2: *Information*
    Grade: *Grade for current section*
    Overall Score: *Score for current section*
    Strengths: *Information*
    Areas for improvement: *Information*
    Recommendations: *Information*
    .
    .
    and so on
    #Structure#
    Here is the information you will use to create the report:\n
    
    {message}
    
    """

    print(prompt)
    return prompt
    
def bedrock_invoke(prompt):
    print("!!!!!!!INVOKING BEDROCK!!!!!!")
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
    # print(response_text)
            
    return response_text


# {
#     ["question":"Do you have a written, up-to-date workplace health and wellbeing strategy that is visible and experienced by your employees every day?",
#     "response":"It was felt that although documented, this strategy is poorly communicated or provided with any guidance. The strategy is regarded by the team as difficult to find and navigate."],
    
#     ["question":"Do you measure workplace health and wellbeing KPIs, and are these integrated into board-level reporting?",
#     "response":"Basic data collection is in place."],
    
#     ["question":"Does the executive management team set and check the progress of workspace health and wellbeing KPIs regularly ?",
#     "response":"The team only knows about limited areas that are measures such as short and long term sickness absence, it is not known what is done with these KPIs."],
    
#     ["question":"Are your policies effectively communicated to employees so they are aware of the health and wellbeing support available to them?",
#     "response":"There was a mixed levelof knowledge on what policies exist and where they are located. It was felt there was inconsistency in sharing this information. However a range of policies do exist"],
    
#     ["question":"Are appropriate policies in place to support good employee health and wellbeing? Flexible working, remote working, mental health, menopause, miscarriage, childcare, etc",
#     "response":"Yes, however there could be a wider range of policieson offer that are more inclusive and diverse."],
    
#     ["question":"Are workplace health and wellbeing initiatives consodered as part of the training and retraining of employees, including the management team and are policies in place to support this?",
#     "response":"This has been considered and some form of e-learning is available. However it is felt that the level of training is not sufficient enough to help managers feel confident in dealing with certain topics."]
# }