import sqlite3
db_name = 'quiz.sqlite'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

    
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    do('''CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        name VARCHAR
    )''')
    do('''CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY,
        question VARCHAR,
        answer VARCHAR,
        wrong1 VARCHAR,
        wrong2 VARCHAR,
        wrong3 VARCHAR
    )''')
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz (id),
        FOREIGN KEY (question_id) REFERENCES question (id)
    )''')
    close()

def add_question():
    question = [
        ('Тестовый вопрос №1', 'Да', 'Нет', 'Что?', 'Почему?'),
        ('Тестовый вопрос №2', 'Да', 'Нет', 'Что?', 'Почему?'),
        ('Тестовый вопрос №3', 'Да', 'Нет', 'Что?', 'Почему?'),
        ('Тестовый вопрос №4', 'Да', 'Нет', 'Что?', 'Почему?'),
        ('Тестовый вопрос №5', 'Да', 'Нет', 'Что?', 'Почему?'),
        ('Тестовый вопрос №6', 'Да', 'Нет', 'Что?', 'Почему?')
    ]
    open()
    query = '''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?, ?, ?, ?, ?)'''
    cursor.executemany(query, question)
    conn.commit()
    close()

def add_quiz():
    quizes = [
        ('Викторина №1', ),
        ('Викторина №2', ),
        ('Викторина №3', )
    ]
    open()
    query = '''INSERT INTO quiz (name) VALUES (?)'''
    cursor.executemany(query, quizes)
    conn.commit()
    close()

def get_quizes():
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result

def add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = '''INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)'''
    answer = input('Добавить связь? (yes/no):')
    while answer != 'n':
        quiz_id = int(input('id викторины: '))
        question_id = int(input('id вопроса: '))
        cursor.execute(query, (quiz_id, question_id))
        conn.commit()
        answer = input('Добавить связ? (yes/no):')
    close()

def get_question_after(question_id=0,quiz_id=1):
    open()
    query = '''SELECT quiz_content.id, question.question, question.answer,
            question.wrong1, question.wrong2, question.wrong3
            FROM question, quiz_content WHERE quiz_content.question_id == question.id
            AND quiz_content.id > ? AND quiz_content.quiz_id == ?
            ORDER BY quiz_content.id'''
    cursor.execute(query, (question_id, quiz_id))
    result = cursor.fetchone()
    close()
    return result


def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def main():
    clear_db()
    create()
    add_question()
    add_quiz()
    add_links()
    show_tables()

if __name__ == "__main__":
    main()
