from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API Configuration
API_KEY = 'Q0LUVFF4MI34YEOZ'
ALPHA_BASE_URL = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE'
CURRENCY_LIST_URL = 'https://open.er-api.com/v6/latest/USD'  # Free API for fetching supported currencies

@app.route('/')
def home():
    # Fetch the list of currencies dynamically
    try:
        response = requests.get(CURRENCY_LIST_URL)
        data = response.json()
        currencies = data.get('rates', {}).keys()
    except Exception as e:
        currencies = []  # Fallback to an empty list if API call fails
    return render_template('index.html', currencies=currencies)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Extract data from the form
        amount = float(request.form['amount'])
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']

        # Build the API URL
        main_url = f"{ALPHA_BASE_URL}&from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}"
        response = requests.get(main_url)
        result = response.json()

        # Extract the exchange rate
        key = result.get('Realtime Currency Exchange Rate', {})
        exchange_rate = float(key.get('5. Exchange Rate', 0))

        if exchange_rate:
            converted_amount = exchange_rate * amount
            return jsonify({
                'converted_value': round(converted_amount, 2),
                'exchange_rate': exchange_rate,
                'success': True
            })
        else:
            return jsonify({'success': False, 'error': 'Unable to fetch exchange rate'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
