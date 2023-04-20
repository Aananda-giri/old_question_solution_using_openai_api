def get_openai_response(request, exam_marks=0):
    import os, random
    import dotenv
    dotenv.load_dotenv()
    import openai

    # random api key from few keys
    # openai.api_key = os.getenv(random.choice(["OPENAI_API_KEY", "OPENAI_API_KEY1", "OPENAI_API_KEY2"]))
    openai.api_key = os.getenv("test_key")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=request,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # response = openai_response_with_backoff(model="text-davinci-002", prompt=request, temperature=0, max_tokens=1000, top_p=1, frequency_penalty=0, presence_penalty=0)
    
    print(response)
    # print(1)
    return response['choices'][0]['text']

# get_openai_response('hi who are you?')
# get_openai_response('Explain how single wire can radiate electromagnetic waves with necessary radiation patterns and conditions.')



import json, os

# check if file exist
# file_to_write = 'questions2.json'
# if not os.path.exists(file_to_write):
file_to_write = 'mannual_questions.json'

# import questions
with open(file_to_write,'r') as f:
    questions = json.load(f)


# propagation and antenna questions
antenna = [question for question in questions if question['subject'] == 'Propagation and Antenna']
# antenna = questions.copy()

# # fetch answer from openai api
# def get_answers(question, marks):
#     # print(question, marks)
#     print('answered')
#     return 'answered'
#     # answers = []
#     # for q, m in zip(question, marks):
#     #     if m == 1:
#     #         answers.append(q)
#     # return answers


for question_by_year in antenna:
    for i in question_by_year['questions']:
        # antenna[0]['questions']['1']['marks']
        question_list = question_by_year['questions'][i]['question']
        marks_list = question_by_year['questions'][i]['marks']
        # print(question_list['question'])
        answer_list = []

        # answer only if not answered
        if 'answer' not in question_by_year['questions'][i].keys() or question_by_year['questions'][i]['answer'] == []:
            for question, mark in zip(question_list, marks_list):
                answer_list.append(get_openai_response(question, mark))
        if answer_list != []:
            # store answer in json
            with open(file_to_write,'r') as f:
                questions_copy = json.load(f)
            
            # antenna_copy = [question for question in questions if question['subject'] == 'Propagation and Antenna']
            questions_copy[questions.index(question_by_year)]['questions'][i]['answer'] = answer_list
            # print(questions_copy)
            with open(file_to_write,'w') as f2:
                json.dump(questions_copy, f2, indent=4)

# print(antenna_copy)
