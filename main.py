from flask import Flask, render_template, session, redirect, url_for, request
from conversion import decimal_to_binary, binary_to_decimal, decimal_to_hexadecimal, hexadecimal_to_decimal
from random import randint, shuffle
import csv

with open('Definition Dataset.csv', 'r') as f:
    definitions = list(csv.reader(f))

with open('questions.csv', 'r') as f:
    questions = list(csv.reader(f))

correct_answers = {}

# initialise the correct answers for the MCQ questions
for (question,correct_ans,_,_,_) in questions:
    correct_answers[correct_ans] = question

app = Flask(__name__)
app.secret_key = 'GPT_for_the_W'

curr_conversion = None
total_qns = 0

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if 'content-box-1' in request.form:
            return redirect('/number-bases')
        if 'content-box-2' in request.form:
            return redirect('/flashcards')
        if 'content-box-3' in request.form:
            return redirect('/quiz')
    return render_template('index.html')

@app.route('/number-bases', methods=['GET', 'POST'])
def number_bases():
    global curr_conversion, start_conversion, end_conversion
    if curr_conversion is None:
        curr_conversion = 'Decimal-Binary'
        start_conversion, end_conversion = 'Decimal', 'Binary'
    if request.method == "POST":
        for conversion in ['Decimal-Binary', 'Binary-Decimal', 'Decimal-Hexadecimal', 'Hexadecimal-Decimal']:
            if conversion in request.form:
                curr_conversion = conversion
                start_conversion, end_conversion = conversion.split('-')
                break
        if "digits" in request.form:
            if curr_conversion == 'Decimal-Binary':
                input_value = request.form["digits"]
                if not(input_value.isdigit()):
                    return render_template('number-bases.html', type_error=True)
                decimal = int(input_value)
                steps, result = decimal_to_binary(decimal)
                steps = steps.split('\n')
                return render_template('number-bases.html', input_value=decimal, steps=steps, result=result, start_conversion=start_conversion, end_conversion=end_conversion)
            if curr_conversion == 'Binary-Decimal':
                binary = request.form["digits"]
                if any(digit not in ['0', '1'] for digit in binary):
                    return render_template('number-bases.html', type_error=True)
                steps, result = binary_to_decimal(binary)
                steps = steps.split('\n')[:-1]
                return render_template('number-bases.html', input_value=binary, steps=steps, result=result, start_conversion=start_conversion, end_conversion=end_conversion)
            if curr_conversion == 'Decimal-Hexadecimal':
                input_value = request.form["digits"]
                if not(input_value.isdigit()):
                    return render_template('number-bases.html', type_error=True)
                decimal = int(input_value)
                steps, result = decimal_to_hexadecimal(decimal)
                steps = steps.split('\n')
                return render_template('number-bases.html', input_value=decimal, steps=steps, result=result, start_conversion=start_conversion, end_conversion=end_conversion)
            if curr_conversion == 'Hexadecimal-Decimal':
                hexadecimal = request.form["digits"]
                hexadecimal_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
                if any(digit not in hexadecimal_digits for digit in hexadecimal):
                    return render_template('number-bases.html', type_error=True)
                steps, result = hexadecimal_to_decimal(hexadecimal)
                steps = steps.split('\n')[:-1]
                return render_template('number-bases.html', input_value=hexadecimal, steps=steps, result=result, start_conversion=start_conversion, end_conversion=end_conversion)
    return render_template('number-bases.html')

@app.route('/flashcards', methods=['GET', 'POST'])
def flashcards():
    points = request.args.get('points', session.get('points', 0))
    
    correct_index = randint(0, len(definitions) - 1)
    wrong_indices = [randint(0, len(definitions) - 1), randint(0, len(definitions) - 1)]
    while wrong_indices[0] == correct_index or wrong_indices[1] == correct_index or wrong_indices[0] == wrong_indices[1]:
        wrong_indices = [randint(0, len(definitions) - 1), randint(0, len(definitions) - 1)]
    
    return render_template('flashcards.html', correct_term=definitions[correct_index][0],
                           correct_definition=definitions[correct_index][1],
                           wrong_term=definitions[wrong_indices[0]][0],
                           wrong_definition=definitions[wrong_indices[1]][1],
                           points=points)

@app.route('/increment_points', methods=['GET', 'POST'])
def increment_points():
    points = int(request.args.get('points', 0))
    is_correct = request.args.get('is_correct', '').lower() == 'true'

    session['points'] = points
    return redirect(url_for('flashcards', points=points)) # Return a success message to the AJAX request

@app.route('/reset_points', methods=['GET', 'POST'])
def reset_points():
    session['points'] = 0
    return redirect(url_for('flashcards', points=0))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global total_qns, tested_questions
    if request.method == "POST":
        if 'total_qns' in request.form:
            total_qns = int(request.form['total_qns'])
            # extract questions from questions.csv to test users
            question_indices = [randint(0, len(questions)-1) for _ in range(total_qns)]
            tested_questions = list(map(lambda qn_index: questions[qn_index], question_indices))
            # shuffle options
            for i in range(len(tested_questions)):
                options = tested_questions[i][1:]
                shuffle(options)
                tested_questions[i] = tested_questions[i][:1] + options
            session['current_question_index'] = 0
            score = session['score'] = 0
        current_question_index = session.get('current_question_index', 0)
        score = session.get('score', 0)
        if 'answer' in request.form:
            # Validate if the answer is correct
            if request.form['answer'] in correct_answers and correct_answers[request.form['answer']] == tested_questions[current_question_index][0]:
                score += 1
            current_question_index += 1

            session['current_question_index'] = current_question_index
            session['score'] = score

        if current_question_index >= len(tested_questions):
            return render_template('score.html', score=score, total_qns=total_qns)
        
        return render_template('question.html', question=tested_questions[current_question_index], qn_index=current_question_index)
    return render_template('quiz.html')

app.run(debug=True)