# Здесь будет код веб-приложения
from flask import Flask, redirect, url_for, session, request, render_template
from db_scripts import get_question_after, get_quizes


def quiz_choose_form():
    html = '<html><head><title>Выбери викторину</title></head>'
    html += '<body><h2>Выберите викторину:</h2><form method="POST" action="/">'
    html += '<select name="quiz">'
    for id, name in get_quizes():
        html += '<option value="' + str(id) + '">' + str(name) + '</option>'
    html += '<p><input type="submit" value="Выбрать"></p></select></form></body></html>'
    return html

def question_form(result):
    html = '<form method="POST" action="/test">'
    html += '<h2>' + result[1] + '</h2>'
    html += '<p><input type="radio" value="' + result[2] + '">' + result[2] + '</p>'
    html += '<p><input type="radio" value="' + result[3] + '">' + result[3] + '</p>'
    html += '<p><input type="radio" value="' + result[4] + '">' + result[4] + '</p>'
    html += '<p><input type="radio" value="' + result[5] + '">' + result[5] + '</p>'
    html += '<p><input type="submit" value="Отвеить"></p></form>'
    return html

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
        return question_form(result)

def result():
    return "Result"

import os
app = Flask(__name__, static_folder=os.getcwd(), template_folder=os.getcwd())
app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/test', 'test', test)
app.add_url_rule('/result', 'result', result)
app.config['SECRET_KEY'] = 'SUPERveryMEGAmaxiSecret'

if __name__ == '__main__':
    app.run()