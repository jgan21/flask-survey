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
# responses = []

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

    session["responses"] = []

    # global responses
    # responses = []

    return redirect ("/question/0")


@app.get("/question/<int:question_id>")
def handle_question_page(question_id):
    '''List question and choices for use as buttons'''

    #add more conditionals for accessing ids beyond size to maybe redirect back
    #to beginning

    track_answer_count = 0
    print("track=", track_answer_count)
    if track_answer_count == len(survey.questions)-1:
        return redirect('/completion')

    if question_id == track_answer_count:
        question = survey.questions[question_id]
        track_answer_count += 1
        return render_template("question.html",
                            question=question,
                            question_id=question_id)
    # elif question_id > track_answer_count and question_id < track_answer_count:
    else:
        return redirect(f"/question/{question_id}")


@app.post("/answer")
def handle_answer_page():
    '''Appends answer given in previous question form to response list
    and redirect to next question'''

    current_list = session["responses"]
    current_list.append(request.form['answer'])
    session["responses"] = current_list

    print(session["responses"])

    #make a separate variable for line below
    #could check length of responses is less than total questions to redirect
    #to complete page

    return redirect(f"/question/{int(request.form['curr_question_id'])+1}")


@app.get("/completion")
def handle_completion_page():
    '''render the completion / thank you page and pass the responses and
    corresponding questions to it'''

    return render_template("completion.html",
                            responses=session["responses"],
                            questions=survey.questions)


