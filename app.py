from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from hybrid_model import HybridSalesPredictor
import json
from datetime import datetime, timedelta

app = Flask(__name__)


# Sample data generator
def generate_sample_data():
    np.random.seed(42)
    dates = pd.date_range(end=datetime.today(), periods=365).tolist()
    data = pd.DataFrame({
        'date': dates,
        'price': np.random.uniform(10, 100, 365),
        'price_max': np.random.uniform(100, 200, 365),
        'promotion': np.random.choice([0, 1, 2], 365, p=[0.7, 0.2, 0.1]),
        'seasonality': np.sin(np.linspace(0, 10, 365)) * 50 + 50,
        'sales': np.random.poisson(500, 365) +
                 np.sin(np.linspace(0, 10, 365)) * 200
    })
    return data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        train_size = int(request.form.get('train_size', 80))

        # Generate and split data
        data = generate_sample_data()
        split_idx = int(len(data) * (train_size / 100))

        X_train = data.iloc[:split_idx][['price', 'price_max', 'promotion', 'seasonality']]
        y_train = data.iloc[:split_idx]['sales']
        X_test = data.iloc[split_idx:][['price', 'price_max', 'promotion', 'seasonality']]
        y_test = data.iloc[split_idx:]['sales']

        # Train model
        predictor = HybridSalesPredictor()
        predictor.train(X_train, y_train)
        predictions = predictor.predict(X_test)

        # Prepare chart data
        chart_data = {
            'dates': data.iloc[split_idx:]['date'].dt.strftime('%Y-%m-%d').tolist(),
            'actual': y_test.tolist(),
            'predicted': predictions.tolist(),
            'metrics': {
                'r2_score': round(predictor.model.score(
                    predictor.scaler.transform(predictor._fuzzy_preprocess(X_test)),
                    y_test
                ), 2),
                'best_params': predictor.best_params
            }
        }

        return render_template('results.html',
                               chart_data=json.dumps(chart_data),
                               metrics=chart_data['metrics'])

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)