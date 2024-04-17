from flask import Flask, render_template, request, redirect
from conversion import decimal_to_binary
from random import randint
import csv

with open('Definition Dataset.csv', 'r') as f:
    definitions = list(csv.reader(f))

app = Flask(__name__)

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
    if request.method == "POST":
        if "decimal-to-binary" in request.form:
            input_value = request.form["decimal-digits"]
            decimal = int(input_value)
            steps, result, instructions_list = decimal_to_binary(decimal)
            curr_instructions = instructions_list.head
            steps = steps.split('\n')
            return render_template('number-bases.html', input_value=input_value, steps=steps, result=result, curr_instructions=curr_instructions)
    return render_template('number-bases.html')

@app.route('/flashcards', methods=['GET', 'POST'])
def flashcards():
    correct_index = randint(0, len(definitions)-1)
    wrong_indices = [randint(0, len(definitions)-1), randint(0, len(definitions)-1)]
    while wrong_indices[0] == correct_index or wrong_indices[1] == correct_index or wrong_indices[0] == wrong_indices[1]:
        wrong_indices = [randint(0, len(definitions)-1), randint(0, len(definitions)-1)]
    return render_template('flashcards.html', correct_term=definitions[correct_index][0], correct_definition=definitions[correct_index][1], wrong_term=definitions[wrong_indices[0]][0], wrong_definition=definitions[wrong_indices[1]][1])

app.run(debug=True)
