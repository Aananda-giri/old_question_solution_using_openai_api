from flask import Flask, render_template, request, redirect, url_for
from functions import pdf_url_to_qa, get_questions_by_id, get_title_id_pair_from_db, get_mannual_subjects, get_mannual_questions
import json
app = Flask(__name__, template_folder='templates')

@app.route('/questions/<string:question_id>')
def show_question(question_id):
    # questions = [
    #     {'question': 'What is the capital city of France?', 'answer': 'Paris'},
    #     {'question': 'Who invented the telephone?', 'answer': 'Alexander Graham Bell'},
    #     {'question': 'What is the symbol for sodium on the periodic table?', 'answer': 'Na'}
    # ]
    data_by_id = get_questions_by_id(question_id)
    question_answers = data_by_id['qa']
    print(data_by_id)
    page_title = data_by_id['title']
    url = data_by_id['url']

    return render_template('questions.html', questions=question_answers, title=page_title, url=url)

@app.route('/')
def home():
    if request.method == 'GET':
        import json
        url = request.args.get('url')
        title = request.args.get('titlee')
        if url:
            # extract and save question answers to db
            pdf_url_to_qa(url, title)

            # update database
            # title_id_pairs = save_to_db(url, title, question_answers)
            print(f'\n\n request: {request}, url:{url},  title:{title}')
            # print(f'url: {url}, title: {title}, question_answers: {question_answers}')
            # return render_template('home.html', title_id_pairs = title_id_pairs)
    # else:
    # print(f'data: {data}')
    return render_template('home.html', title_id_pairs = get_title_id_pair_from_db(), mannual_subjects = get_mannual_subjects())


# @app.route('/mannual')
# def index():
#     with open ('mannual_questions.json', 'r') as f:
#         qna = json.load(f)

    # for item in qna:
    #     for _, value in item['questions'].items():
    #         # for _, value in all_questions.items():
    #             value['num_parts'] = len(value['question'])
    #             if 'answer' not in value.keys():
    #                 value['answer'] = ['']*value['num_parts']
#     return render_template('mannual_questions.html', qna=qna)

@app.route('/mannual/<string:subject>')
def index(subject):
    
    qna = get_mannual_questions(subject)
    # print(qna)
    for item in qna:
        for _, value in item['questions'].items():
            # for _, value in all_questions.items():
                value['num_parts'] = len(value['question'])
                if 'answer' not in value.keys():
                    value['answer'] = ['']*value['num_parts']
    return render_template('mannual_questions.html', qna=qna)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8001)