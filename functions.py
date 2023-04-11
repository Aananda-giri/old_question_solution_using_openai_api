import random, json
import string

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
                if qa['question'] == question:
                    is_present = True
                    break
            break
    return is_present, random_id_of_url

def save_one_qa_to_db(url, qa, title, random_id):
    with open('qa.json', 'r')  as f:
        other_datas = json.load(f)
    if random_id != None and random_id in other_datas['question_answer_pair'].keys():
        other_datas['question_answer_pair'][random_id]['qa'].append(qa)
    else:
        ramdom_id = generate_random_id()
        other_datas['question_answer_pair'][random_id] = {'url': url, 'qa': [qa], 'title': title}
    
    with open('qa.json', 'w')  as f:
        json.dump(other_datas, f)
    return 'savec'

def save_clean_questions(questions, url, title):
    with open('questions.json', 'r') as f:
        old_questions = json.load(f)
    
    old_questions['questions'].append({'questions':questions, 'url':url, 'title':title})
    
    with open('questions.json', 'w') as f:
        json.dump(old_questions, f)
    return 'saved'

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

def extract_text_from_pdf(filename):
    # split pages and convert to text
    import cv2, os
    from pdf2image import convert_from_path
    import pytesseract

    # filePath = 'Project Management.pdf'
    filePath = filename
    doc = convert_from_path(filePath)
    path, fileName = os.path.split(filePath)
    fileBaseName, fileExtension = os.path.splitext(fileName)

    data = []   # list of text from each page
    for page_number, page_data in enumerate(doc):
        page_data.save("temp.jpg", "JPEG")
        img = cv2.imread("temp.jpg")
        text = pytesseract.image_to_string(img, lang="eng", config='--oem 3 --dpi 300 -l eng')
        data.append(text)
        print('page :',page_number)
    return data



import openai  # for OpenAI API calls
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


# with rate limit handling
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_response_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)
# openai_response_with_backoff(model="text-davinci-002", prompt="Once upon a time,")



def get_openai_response(request):
    import os, random
    import dotenv
    dotenv.load_dotenv()
    import openai

    # random api key from few keys
    openai.api_key = os.getenv(random.choice(["OPENAI_API_KEY", "OPENAI_API_KEY1", "OPENAI_API_KEY2"]))

    # response = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=request,
    #     temperature=0,
    #     max_tokens=700,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0
    # )
    
    response = openai_response_with_backoff(model="text-davinci-002", prompt=request, temperature=0, max_tokens=1000, top_p=1, frequency_penalty=0, presence_penalty=0)
    return response['choices'][0]['text']

def get_questions_from_tesseract_output(questions, file_name):
    questions_clean = []
    for question_page in questions:
        request = "below is the tesseract output of question paper of {file_name}. please generate list of questions from text below:" + '\n\n' + question_page + '\n\n' + "questions = "
    
        response = get_openai_response(request)
        
        # one giant list of questions
        questions_clean.extend(response.split('\n'))
    
    return list(set(questions_clean))

def get_answers_from_tesseract_output(questions, file_name, url):
    qa_pairs = []
    for question_page in questions:
        for question in question_page:
            exists, random_id = already_answered(url, question)
            if not exists:
                request = "question: {question}' + '\n\n' + answer = "
            
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

    save_clean_questions(questions, 'questions.json', url, title)
    # get answers from questionss    
    qa_pairs = get_answers_from_tesseract_output(questions, file_name, url)

    # delete file
    import os
    # os.remove(file_name)

    return qa_pairs