from flask import Flask, render_template, request
from fuzzy_module import predict_performance
from ga_optimizer import generate_study_plan

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=["POST"])
def predict():
    attendance = float(request.form['attendance'])
    study_hours = float(request.form['study_hours'])
    prev_score = float(request.form['prev_score'])

    performance = predict_performance(attendance, study_hours, prev_score)
    study_plan = generate_study_plan(attendance, study_hours, prev_score)

    return render_template("result.html", performance=performance, plan=study_plan)

if __name__ == '__main__':
    app.run(debug=True)