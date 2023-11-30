from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


RESPONSES = []
@app.get('/')
def survey_start_page():
    '''Shows user the title, instructions, and button to start survey'''
    title = survey.title
    survey_instructions = survey.instructions
    return render_template("survey_start.html",
                           title=title,
                           survey_instructions =survey_instructions)
@app.post("/begin")
def begin_survey():
    return redirect ("/question/0")

@app.get("/question/<int:question_id>")
def handle_question_page(question_id):
    '''List question and choices for use as buttons'''

    question = survey.questions[question_id]

    return render_template("question.html",
                           question=question)




