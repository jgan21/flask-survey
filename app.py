from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

#put more blank spaces after doc strings, inbetween routes put two spaces
#put blank spaces between separate operations

#lower case responses
RESPONSES = []

@app.get('/')
def survey_start_page():
    '''Shows user the title, instructions, and button to start survey'''
    #move clearing out responses to begin_survey

    title = survey.title
    survey_instructions = survey.instructions
    #could have passed in the entire survey object instead of the separate properties
    return render_template("survey_start.html",
                           title=title,
                           survey_instructions=survey_instructions)


#if making modifications to a overall variable make it post
@app.post("/begin")
def begin_survey():
    '''redirect to the first question page'''
    global RESPONSES
    RESPONSES = []
    return redirect ("/question/0")


@app.get("/question/<int:question_id>")
def handle_question_page(question_id):
    '''List question and choices for use as buttons'''

    #add more conditionals for accessing ids beyond size to maybe redirect back
    #to beginning
    if question_id > len(survey.questions)-1:
        return redirect('/completion')
    else:
        question = survey.questions[question_id]

        return render_template("question.html",
                            question=question,
                            question_id=question_id)


@app.post("/answer")
def handle_answer_page():
    '''Appends answer given in previous question form to response list
    and redirect to next question'''
    RESPONSES.append(request.form['answer'])
    #why does this somehow double the responses variable in jinja
    #probably cause not emptying RESPONSES globally
    print(RESPONSES)
    #make a separate variable for line below
    #could check length of responses is less than total questions to redirect
    #to complete page
    return redirect(f"/question/{int(request.form['curr_question_id'])+1}")


@app.get("/completion")
def handle_completion_page():
    '''render the completion / thank you page and pass the responses and
    corresponding questions to it'''
    return render_template("completion.html",
                            responses=RESPONSES,
                            questions=survey.questions)


