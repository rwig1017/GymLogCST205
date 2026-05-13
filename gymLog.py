#Author: Robin Wig
#Date: 5/6/2026
#Course: CST205
#Title: GymLog
#Abstract: Lets users log their gym workouts and manage it


from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import requests
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

logs = []

# This is for the quote API
# Gets a motivational quote
def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        data = response.json()[0]
        return data["q"] + " — " + data["a"]
    except:
        return "Push yourself — GymLog"

# Routes

# Home Page
@app.route('/')
def home():
    quote = get_quote()
    return render_template('home.html', quote=quote)

#Add Workout
@app.route('/add', methods=['GET', 'POST'])
def add_log():
    if request.method == 'POST':
        workout = request.form['workout']
        notes = request.form['notes']
        photo = request.files.get('photo')

        filename = ''

        # Save uploaded image if it exists
        if photo and photo.filename != '':
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        logs.append({
            'workout': workout,
            'notes': notes,
            'image': filename,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        })

        return redirect(url_for('view_logs'))

    return render_template('add.html')

#View Logs
@app.route('/logs')
def view_logs():
    return render_template('logs.html', logs=list(enumerate(logs)))

#Delete Logs
@app.route('/delete/<int:index>')
def delete_log(index):
    if 0 <= index < len(logs):
        logs.pop(index)
    return redirect(url_for('view_logs'))

if __name__ == '__main__':
    app.run(debug=True)