## Introduction
    * A project developed for [Stranger Hacks](https://strangerhacks.devfolio.co/) hackathon
    

    * Tagline: `Old questions solution`
    
    ### working
    Enter url to old exam questions
    * It will give you questions and corresponding answers

## Running Code:
    * Install Requirements: `pip install -r requirements.txt`
    * Install `tesseract-ocr`
    * Run `python main.py`

## Internal Working
    * Download pdf from url given
    * Convert pdf to images
    * Extract text from images using `pytesseract`
    * Extract questions from `pytesseract` output using `openai-api`
    * Extract answers of questions output using `openai-api`
    * Store Answers and put link to question_answers in home page

## problems:
    * openAI API Rate Limit: `RateLimitError: You exceeded your current quota, please check your plan and billing details.`


## Stored Data Format

'''
        * `qa.json` format
        * using random_id to allow multiple qa with same title
        * todo: store to database
        
        {
                "random_id": 
                [
                    {
                        "url":<url>,
                        "title":<title>",
                        "qa": [
                                {
                                    "question": "question1",
                                    "answer" : "answer1"
                                },
                                {
                                    "question": "question2",
                                    "answer": "answer2"
                                },
                    },

                    {
                        "url":"<url2>",
                        
                    },
                    
                ],
                
                "random_id2": 
                [
                    {
                        "url":"<url>",
                        "title":"<title>",
                        "qa": [
                                {
                                    "question": "question1",
                                    "answer" : "answer1"
                                },
                                {
                                    "question": "question2",
                                    "answer": "answer2"
                                },
                    },

                    {
                        "url":"<url2>",
                        
                    },
                    
                ],
            ],

        }
        '''

### TODO
    * use database instead of json file for storing data
    * option to upload images and pdfs files
    * save as soon as each question is extracted or answered
    * buy openai api key to remove rate limit

## References
    0. [consider this bible](https://github.com/openai/openai-cookbook)

    1. [kickoff + workshop](https://youtu.be/zAjiu60Le8I)
    
    2. [Hackers' Guide](https://nsb.dev/stranger-hacks-hackers-guide)
    
    3. [Devfolio Code of Conduct](https://devfolio.co/code-of-conduct)


    https://platform.openai.com/