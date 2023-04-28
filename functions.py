import random, json
import string
import cv2, os
from pdf2image import convert_from_path
import pytesseract

# -----------------------
# Database operations
# -----------------------

def save_to_db(url, title, question_answers):
    # see README.md for qa.json format
    with open ('qa.json', 'r') as f:
        # load old qa
        old_qa = json.load(f)
        
        # append new qa
        random_id = generate_random_id()
        old_qa[random_id] = {
                                "url":url,
                                "title":title,
                                "qa": question_answers
        }
        
        # update title_id_pairs
        old_qa["title_id_pairs"].append({
            "title":title,
            "id":random_id
        })

        # save to qa.json
        with open('qa.json', 'w') as f:
            json.dump(old_qa, f)
        
        return old_qa["title_id_pairs"]
        
        

# get qa stored data
def get_data_from_db():
    # with open ('qa.json', 'r') as f:
    #     qa = json.load(f)
    # return qa
    with open('qa.json', 'r')  as f:
        other_datas = json.load(f)
    return other_datas['question_answer_pair']

def get_title_id_pair_from_db():
    with open('qa.json', 'r')  as f:
        other_datas = json.load(f)
    # print(other_datas)
    return other_datas['title_id_pairs']

def get_questions_by_id(question_id):
    with open('qa.json', 'r')  as f:
        other_datas = json.load(f)
    return_val = other_datas['question_answer_pair'][question_id]
    # print(return_val)
    return return_val

def generate_random_id(digits=5):
    # Generate a random 5-digit alphanumeric string
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=digits))
    # print(random_string)
    return random_string

def already_answered(url, question):
    with open('qa.json', 'r')  as f:
            other_datas = json.load(f)
    
    is_present = False
    random_id_of_url = None
    for random_id in other_datas['question_answer_pair'].keys():
        
        if other_datas['question_answer_pair'][random_id]['url'] == url:
            random_id_of_url = random_id
            question_answer_pair = other_datas['question_answer_pair'][random_id]['qa']
            
            for qa in question_answer_pair:
                if qa['question'] == question and 'answer' in qa.keys() and qa['answer'] != '':
                    is_present = True
                    break
            break
    return is_present, random_id_of_url

def save_one_qa_to_db(url, qa, title, random_id):
    # print(f'\n\n got_random_id:{random_id}\n\n  is None?{random_id==None} type:{type(random_id)}')
    with open('qa.json', 'r')  as f:
        other_datas = json.load(f)
    if random_id != None and random_id in other_datas['question_answer_pair'].keys():
        other_datas['question_answer_pair'][random_id]['qa'].append({'question':qa['question'], 'answer':qa['answer']})
        # print('\n\n -------------------- update existing')
    else:
        # print('\n\n -------------------- new question')
        random_id = generate_random_id()
        other_datas['question_answer_pair'][random_id] = {'url': url, 'qa': [qa], 'title': title}
        not_present = True
        for title_id in other_datas['title_id_pairs']:
            if random_id == title_id['random_id']:
                not_present = False
                break
        if not_present:
            other_datas['title_id_pairs'].append({'title': title, 'random_id': random_id})
    # print(f'\n\n random id is: {random_id} is None?{random_id==None}  type:{type(random_id)}')
    with open('qa.json', 'w')  as f:
        json.dump(other_datas, f)
    return 'savec'

def save_clean_questions(questions, url, title):
    with open('questions.json', 'r') as f:
        old_questions = json.load(f)
    
    old_questions['questions'].append({'url':url, 'title':title, 'questions':questions, })
    
    with open('questions.json', 'w') as f:
        json.dump(old_questions, f)
    return 'saved'

# ------------------
# Mannual Questions
# ------------------

def get_mannual_subjects():
    with open ('mannual_questions.json', 'r') as f:
        qna = json.load(f)
    mannual_subjects = []
    for question_paper in qna:
        if question_paper['subject'] not in mannual_subjects:
            mannual_subjects.append(question_paper['subject'])
    return mannual_subjects

def get_mannual_questions(subject):
    with open ('mannual_questions.json', 'r') as f:
        qna = json.load(f)
    
    question_papers = []
    for question_paper in qna:
        if question_paper['subject'] == subject:
            question_papers.append(question_paper)
    # short by year
    question_papers.sort(key=lambda x: x['date_year'], reverse=True)
    return question_papers
# ------------------
# File operations
# ------------------
def download_file(title, url="https://acem.edu.np/uploads/userfiles/files/old_question/6th%20Semester/BCTBEXBEL/Object%20Oriented%20Analysis%20and%20Design.pdf"):
    # Download a file from a URL and save it to the specified filename
    import requests, urllib
    # Replace with the name you want to save the PDF as
    # print(url)
    if title == 0 or title == None or title == '':    
        url_strings = urllib.parse.unquote(url).split('/')
        for reversed_url_part in reversed(url_strings):
            if '.pdf' in reversed_url_part:
                filename = reversed_url_part
                break
        if not filename:
            filename = url_strings[-1] + '.pdf'
    else:
        filename = title + '.pdf'
    
    # print(filename) # "Project Management.pdf"
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
    # print("PDF downloaded successfully.")
    return filename

def img_to_text(img):
    # img = cv2.imread(file_path)

    # Preprocess the image (e.g. resize, threshold, etc.)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply OCR using Pytesseract
    text = pytesseract.image_to_string(gray, lang='eng')

    # # Print the recognized text
    # print("Original Text:")
    # print(text)

    # Perform post-processing on the text (e.g. remove non-alphanumeric characters, correct spelling errors, etc.)
    processed_text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace('  ','')
    
    # this line removes all non-alphanumeric characters from the text
    # processed_text = ' '.join(word for word in processed_text.split() if word.isalnum())

    # # Print the processed text
    # print("Processed Text:")
    # print(processed_text)
    
    return processed_text

def extract_text_from_pdf(filename):
    # split pages and convert to text

    # filePath = 'Project Management.pdf'
    filePath = filename
    doc = convert_from_path(filePath)
    path, fileName = os.path.split(filePath)
    fileBaseName, fileExtension = os.path.splitext(fileName)

    data = []   # list of text from each page
    for page_number, page_data in enumerate(doc):
        page_data.save("temp.jpg", "JPEG")
        img = cv2.imread("temp.jpg")
        # text = pytesseract.image_to_string(img, lang="eng", config='--oem 3 --dpi 300 -l eng')
        text = img_to_text(img)
        data.append(text)
        print('page :',page_number)
    return data



import openai  # for OpenAI API calls
import dotenv
dotenv.load_dotenv()

def get_openai_response(request, exam_marks=0):
    # random api key from few keys
    # openai.api_key = os.getenv(random.choice(["OPENAI_API_KEY", "OPENAI_API_KEY1", "OPENAI_API_KEY2"]))
    openai.api_key = os.getenv("test_key")
    print(request)

    response = openai.Completion.create(
        model="text-davinci-003",
        # model = "gpt-3.5-turbo",
        prompt=request,
        temperature=0.3,  # 0 temperature controls the randomness of predictions. 0 means only the most likely word is predicted. 1 means picking a word is completely random. We generally recommend using values between 0.9 and 1.2.
        max_tokens=3000,    # 1000 max_tokens controls the maximum number of tokens to generate. Requests can use up to 2048 tokens shared between prompt and completion. (One token is roughly 4 characters for normal English text)
        top_p=0.2,    # 1 top_p controls diversity via nucleus sampling: 0.0 = no diversity, 1.0 = maximum diversity
        frequency_penalty=0.3,    # 0 frequency_penalty adjusts how much the model favors repeating existing lines
        presence_penalty=.03      # 0.3 presence_penalty adjusts how much the model favors generating new lines rather than repeating existing ones
    )
    
    # response = openai_response_with_backoff(model="text-davinci-002", prompt=request, temperature=0, max_tokens=1000, top_p=1, frequency_penalty=0, presence_penalty=0)
    
    print(response)
    # print(1)
    return response['choices'][0]['text']

def get_questions_from_tesseract_output(questions, file_name):
    questions_clean = []
    for question_page in questions:
        request = f"below is the tesseract output of question paper of {file_name}. please generate a python list of questions from text below:" + '\n\n' + question_page + '\n\n' + "questions_list_for_python = "
    
        response = get_openai_response(request)
        
        # one giant list of questions
        questions_clean.extend(response.split('\n'))
    
    return list(set(questions_clean))
import re
def is_valid_question(question):
    is_valid = True
    # remove all special characters and numeric characters
    question = re.sub('[^A-Za-z]+', ' ', question).replace('\n', '').replace('\t','').replace('\r','').replace('  ','')
    if question == '' or len(question) < 8:
        is_valid = False
    return is_valid
def get_answers_from_tesseract_output(questions, file_name, url):
    qa_pairs = []
    for question_page in questions:
        for question in question_page:
            exists, random_id = already_answered(url, question)
            if not exists:
                if not is_valid_question(question):
                    continue
                request = f"question: {question}' + '\n\n' + answer = "
            
                response = get_openai_response(request)
                qa = {'question': question, 'answer': response}
                qa_pairs.append(qa)

                # save to db
                save_one_qa_to_db(url, qa, file_name, random_id)
    
    return qa_pairs


def pdf_url_to_qa(url, title):
    # Download file from url
    file_name = download_file(title, url)
    print(f"\n got file {file_name}")

    # Extract text from PDF
    # format: list of text from each page
    text_data = extract_text_from_pdf(file_name)
    print(f"\n extracted text from {file_name}")
    # get questions from tesseract text
    questions = get_questions_from_tesseract_output(text_data, file_name)
    print(f"\n got questions from {file_name}")

    save_clean_questions(questions, url, title)
    # get answers from questionss    
    # with open('questions.json','r') as f:
    #     saved_questions = json.load(f)
    # questions = saved_questions['questions'][0]['questions']
    # file_name = saved_questions['questions'][0]['title']
    # url = saved_questions['questions'][0]['url']
    # print(f'loaded questions:{len(questions)} url:{url}, file_name:{file_name}')
    
    qa_pairs = get_answers_from_tesseract_output([questions], file_name, url)

    # delete file
    import os
    # os.remove(file_name)

    return qa_pairs