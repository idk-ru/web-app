# Здесь будет код веб-приложения
from flask import Flask, redirect, url_for, session, request, render_template
from db_scripts import get_question_after, get_quizes

def index():
    if request.method == 'GET':
        session['quiz'] = 0
        session['last_question'] = 0
        return render_template('start.html', quizes=get_quizes())
    if request.method == 'POST':
        session['quiz'] = request.form.get('quiz')
        return redirect(url_for('test'))

def test():
    last_question = session['last_question']
    quiz = session['quiz']
    result = get_question_after(last_question, quiz)
    if result is None or len(result) == 0:
        return redirect(url_for('result'))
    else:
        session['last_question'] = result[0]
        return render_template('test.html', quest_id=0, question=result[1], answers=result[2:])

def result():
    return "Result"

import os
app = Flask(__name__, static_folder=os.getcwd(), template_folder=os.getcwd())
app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/test', 'test', test, methods=['GET', 'POST'])
app.add_url_rule('/result', 'result', result)
app.config['SECRET_KEY'] = 'SUPERveryMEGAmaxiSecret'

if __name__ == '__main__':
    app.run()
