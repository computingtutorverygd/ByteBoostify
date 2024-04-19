from flask import Flask, render_template, session, redirect, url_for, request
from conversion import decimal_to_binary, binary_to_decimal, decimal_to_hexadecimal, hexadecimal_to_decimal
from random import randint
import csv

with open('Definition Dataset.csv', 'r') as f:
    definitions = list(csv.reader(f))

app = Flask(__name__)
app.secret_key = 'GPT_for_the_W'


curr_conversion = None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if 'content-box-1' in request.form:
            return redirect('/number-bases')
        if 'content-box-2' in request.form:
            return redirect('/flashcards')
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


app.run(debug=True)