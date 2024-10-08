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
    prompt = f"""You are tasked with compiling a comprehensive report for an In-House Health Audit. Your role involves analyzing the information provided based on the guidance and evaluation criteria we outline.\n
    
    **GRADING SYSTEM**
    Each response to the audit questions is graded on a scale of A, B, C, or D, as defined:
    
    A = 30
    
    B = 20
    
    C = 10
    
    D = 0
    
    
    **INSTRUCTIONS**
    Your report should cover the each section, each containing multiple questions and their corresponding responses. For each section, you will:
    Grade and Score each questions based on their responses
    Summarize the overall performance based on the grades.
    Highlight key strengths and areas for improvement, referencing specific responses.
    Provide actionable recommendations where needed.\n 
    
    Here is the information in a json format which you will use to create the report:\n
    
    {message}
    \nGenerate the response in a json structure:\n
    {{
        "sections": [
            {{
                "section": "<section_name>",
                "summary": {{
                    "score": <total_score>,
                    "grade": "<overall_grade>",
                    "strengths": [],
                    "areas_for_improvement": [],
                    "recommendations": []
                }},
                "question_scores": [
                    {{
                        "question": "<question_1>",
                        "score": <score_1>,
                        "grade": "<grade_1>"
                    }},
                    {{
                        "question": "<question_2>",
                        "score": <score_2>,
                        "grade": "<grade_2>"
                    }}
                ]
            }}
        ]
    }}"""

    print(prompt)
    return prompt
    
def bedrock_invoke(prompt):
    print("!!!!!!!INVOKING BEDROCK!!!!!!")
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
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

##TEST EVENT##
# {
#   "Records": [
#     {
#       "messageId": "658ba5c8-e64b-43cb-92d1-457d6e202943",
#       "receiptHandle": "AQEEfUGbahpmL8ZT5xOhHCh7iMvZZKEf6tE4TtaTSWRQD0KaCSTT2K2wuGOYXQBkiOMUoISCOdldHMT4fCICMT9wqQWE9wR558Qft7k0OxL9786cGvfV31Wbt60HOFgWXoOtIrhmyLPHWljObHCthfLqSFwV9bFGiP9mqvyVS63h7WnILzMp8eZd41qZYp4Rn665253Nyto3sK/",
#       "body": {
#         "sections": [
#           {
#             "section": "Workplace Health Policy and Promotion",
#             "questions": [
#               {
#                 "question": "Do you have a written, up-to-date workplace health and wellbeing strategy that is visible and experienced by your employees every day?",
#                 "response": [
#                   "It was felt that although documented, this strategy is poorly communicated or provided with any guidance. The strategy is regarded by the team as difficult to find and navigate.",
#                   "Yes, we do, and it is actively shared during team meetings. However, some employees feel it could be more visible in everyday operations.",
#                   "The strategy exists, but the team feels it lacks proper implementation, making it less effective than it could be.",
#                   "We have a strategy in place, but it is outdated and does not reflect current employee wellbeing needs.",
#                   "The strategy is comprehensive, but only senior staff are aware of its details; more should be done to share it with all levels."
#                 ]
#               },
#               {
#                 "question": "Do you measure workplace health and wellbeing KPIs, and are these integrated into board-level reporting?",
#                 "response": [
#                   "Basic data collection is in place.",
#                   "Yes, these KPIs are measured, but they are rarely reviewed at board meetings.",
#                   "No, workplace wellbeing KPIs are not currently part of our board-level discussions, but there are plans to integrate them.",
#                   "We collect health-related data, but it's not clear how it's used to drive decisions.",
#                   "KPIs are measured sporadically, but they do not consistently contribute to executive decision-making."
#                 ]
#               },
#               {
#                 "question": "Does the executive management team set and check the progress of workplace health and wellbeing KPIs regularly?",
#                 "response": [
#                   "The team only knows about limited areas that are measured, such as short and long term sickness absence. It is not known what is done with these KPIs.",
#                   "Yes, though these KPIs are not always the primary focus of discussions.",
#                   "Executive management sets KPIs, but progress reviews are irregular and inconsistent.",
#                   "There are some KPIs set, but employees are unsure of what metrics are actually being tracked.",
#                   "No, there is no clear process for setting or reviewing wellbeing KPIs at the management level."
#                 ]
#               },
#               {
#                 "question": "Are your policies effectively communicated to employees so they are aware of the health and wellbeing support available to them?",
#                 "response": [
#                   "There was a mixed level of knowledge on what policies exist and where they are located. It was felt there was inconsistency in sharing this information. However, a range of policies do exist.",
#                   "We regularly communicate policies, but employees often forget where they are stored or what they entail.",
#                   "Some employees are aware of the policies, but many are not familiar with the details or where to find them.",
#                   "Yes, these policies are communicated well, but follow-up is needed to ensure people understand them.",
#                   "Policy communication happens mainly via email, but there is no consistent follow-up to ensure employees understand their rights and options."
#                 ]
#               },
#               {
#                 "question": "Are appropriate policies in place to support good employee health and wellbeing? Flexible working, remote working, mental health, menopause, miscarriage, childcare, etc.",
#                 "response": [
#                   "Yes, however, there could be a wider range of policies on offer that are more inclusive and diverse.",
#                   "Yes, most policies exist, but employees have expressed that they lack support in certain areas such as mental health and childcare.",
#                   "We have a few core policies in place, but some are outdated and do not reflect the modern workforce needs.",
#                   "The policies exist, but many employees feel that the actual support provided is inadequate for their specific needs.",
#                   "We have a broad range of policies, but employees feel they could be more flexible and tailored to individual circumstances."
#                 ]
#               },
#               {
#                 "question": "Are workplace health and wellbeing initiatives considered as part of the training and retraining of employees, including the management team, and are policies in place to support this?",
#                 "response": [
#                   "This has been considered, and some form of e-learning is available. However, it is felt that the level of training is not sufficient enough to help managers feel confident in dealing with certain topics.",
#                   "Yes, there are some training programs available, but the depth and coverage of health and wellbeing topics could be improved.",
#                   "The management team undergoes training, but there is minimal focus on health and wellbeing as part of these sessions.",
#                   "We offer training, but it is primarily focused on technical skills rather than health and wellbeing.",
#                   "There is a push to include wellbeing in training, but managers feel they need more resources and dedicated sessions."
#                 ]
#               }
#             ]
#           },
#           {
#             "section": "Workplace Culture and Social Responsibility",
#             "questions": [
#               {
#                 "question": "Does your organisation promote recognition? Praising staff for good work, making them feel valued and appreciated?",
#                 "response": [
#                   "There has been good work done in this area. There are performance and reflective practices regularly and recognition is being provided at team meetings. However, more can be done in this area and organisation wide.",
#                   "Yes, recognition is actively promoted, but it’s not consistent across all departments.",
#                   "We have a recognition system in place, but it is mostly used for senior-level employees.",
#                   "Recognition happens, but it often feels tokenistic rather than genuine and meaningful.",
#                   "Some teams are very good at recognizing achievements, while others rarely acknowledge success."
#                 ]
#               },
#               {
#                 "question": "Are line managers assigned suitable time, training, and resources to ensure they balance business KPIs with concerns for the health and wellbeing of their teams?",
#                 "response": [
#                   "No. The team have a heavy workload and is stretched thin, therefore time pushed. Having time to embed and deliver good health and wellbeing practices is difficult. There is also a lack of training.",
#                   "Managers try their best, but they don’t have the time or resources to focus on wellbeing alongside KPIs.",
#                   "No, managers are under pressure to deliver KPIs and health and wellbeing often takes a back seat.",
#                   "There is little emphasis on providing managers with the necessary resources to balance these concerns.",
#                   "We are working on this, but currently, managers are overwhelmed with their workloads."
#                 ]
#               },
#               {
#                 "question": "Is workload organised so that employees avoid the risk of work-related stress and burnout?",
#                 "response": [
#                   "No. Priorities are always shifting as the team grows. The workload is high and they're at maximum capacity with limited resources.",
#                   "No, employees frequently feel overworked and overwhelmed by shifting priorities.",
#                   "Workloads are high, but there is an effort to monitor and adjust them to avoid burnout.",
#                   "The team is often overworked, leading to stress and occasional burnout.",
#                   "There is some effort to distribute workloads evenly, but employees still feel they are under pressure."
#                 ]
#               },
#               {
#                 "question": "Are employees given control (where possible) over flexible hours, how they do their work and where they work from?",
#                 "response": [
#                   "Yes. Although the team feels that flexibility is good, there’s been a drop in togetherness.",
#                   "Yes, we offer flexibility in hours and work locations, but it can sometimes lead to a feeling of isolation.",
#                   "Employees appreciate the flexibility, but it has led to some challenges in coordination and teamwork.",
#                   "Yes, but some employees would prefer more structure in their working hours.",
#                   "We provide a high level of flexibility, but it’s important to balance that with regular team interactions."
#                 ]
#               },
#               {
#                 "question": "Does the organisation support a good balance and provide opportunities for purpose and connection? E.g., volunteering, fundraising, team challenges, etc.",
#                 "response": [
#                   "No. The level of workload and project delivery does not allow for balance. The team feels there could be more opportunities for social and purposeful activities. This may bring more meaning to their work.",
#                   "There are some initiatives in place, but they are not widely promoted or accessible to all employees.",
#                   "The organisation supports balance in theory, but in practice, the workload makes it difficult to engage.",
#                   "We have a few opportunities for connection, but they are infrequent and poorly attended.",
#                   "Some opportunities exist, but many employees feel they don't have the time or energy to participate."
#                 ]
#               },
#               {
#                 "question": "Do all employees have the necessary skills to perform their work and/or are they given the opportunity to acquire these skills?",
#                 "response": [
#                   "There’s a wide range of roles in the team and training has been provided in the past. However, it’s felt that current learning and development takes a back seat due to workload and a lack of people resources.",
#                   "Yes, but many employees feel they could benefit from more consistent training and development opportunities.",
#                   "We provide some training, but employees feel that it doesn’t always align with their current needs.",
#                   "Employees are encouraged to develop skills, but heavy workloads limit their ability to engage in training.",
#                   "Yes, though training programs have been less frequent in recent years due to resource constraints."
#                 ]
#               }
#             ]
#           },
#           {
#             "section": "Planning of workplace health promotion",
#             "questions": [
#               {
#                 "question": "Are your workplace health promotion measures based on a careful and regularly updated analysis of work stress, health indicators, risk factors, accident rates, absenteeism due to work-related illness, etc?",
#                 "response": [
#                   "There are some absence-related measurements in place but there is a lack of transparency on what is fully measured and what it’s used for.",
#                   "We have basic measures in place, but they are not regularly updated or reviewed.",
#                   "No, the analysis is limited, and there’s little follow-up on what is measured.",
#                   "Yes, we track absenteeism and other indicators, but this data is not shared transparently.",
#                   "There is no clear system for regularly updating these measures, and they are not tied to strategic initiatives."
#                 ]
#               },
#               {
#                 "question": "Are wellbeing initiatives planned to help improve the successful achievement of business KPIs?",
#                 "response": [
#                   "This doesn’t appear to be considered strategically.",
#                   "Yes, wellbeing initiatives are aligned with our business KPIs, but their impact is not always measured.",
#                   "Wellbeing initiatives are planned but are rarely linked directly to business KPIs.",
#                   "Some initiatives are linked to performance metrics, but this isn’t consistent across the organisation.",
#                   "No, wellbeing initiatives are largely treated as separate from business KPIs."
#                 ]
#               },
#               {
#                 "question": "Are workplace health promotion measures planned and effectively communicated throughout the organisation?",
#                 "response": [
#                   "This is done but it is felt that this could be better communicated to all members of the team, especially senior leaders.",
#                   "Yes, but employees often feel out of the loop or unaware of new initiatives.",
#                   "Some communication happens, but it is often after the fact and not part of a proactive strategy.",
#                   "We have measures in place, but they are not communicated well, especially to frontline employees.",
#                   "Communication is improving, but there’s still a long way to go before all employees feel informed."
#                 ]
#               },
#               {
#                 "question": "When considering employee benefits, is a holistic approach taken to offer benefits that positively impact all areas of health and wellbeing?",
#                 "response": [
#                   "The main offering is an employee assistance programme. It covers a range of health issues and support, but it is felt that it is a reactive benefit and used after the point of need, rather than preventatively.",
#                   "Yes, but employees feel the current benefits are too reactive and not enough is done to prevent issues.",
#                   "The benefits package is broad, but employees feel it lacks some depth in key areas such as mental health.",
#                   "Yes, but there’s room for improvement, especially in preventative health measures.",
#                   "Our benefits are diverse, but employees feel they don’t always address their most pressing needs."
#                 ]
#               }
#             ]
#           }
#         ]
#       },
#       "attributes": {
#         "ApproximateReceiveCount": "1",
#         "SentTimestamp": "1727181327495",
#         "SenderId": "AROAQE3RORXUGD4GATBVU:bpadiari@cloudcombinator.ai",
#         "ApproximateFirstReceiveTimestamp": "1727181327497"
#       },
#       "messageAttributes": {},
#       "md5OfBody": "ebc0996df439970ec4fed297fef7134d",
#       "eventSource": "aws:sqs",
#       "eventSourceARN": "arn:aws:sqs:us-east-1: 010438479336:SecondQueue",
#       "awsRegion": "us-east-1"
#     }
#   ]
# }