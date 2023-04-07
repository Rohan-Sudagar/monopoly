from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users or users[username]['password'] != password:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('dashboard', username=username))
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            error = 'Username already taken. Please choose another.'
        else:
            users[username] = {'password': password, 'balance': 1500}
            return redirect(url_for('dashboard', username=username))
    return render_template('signup.html', error=error)

@app.route('/dashboard/<username>', methods=['GET', 'POST'])
def dashboard(username):
    user = users[username]
    if request.method == 'POST':
        if 'buy_property' in request.form:
            property_name = request.form['buy_property']
            property_price = int(request.form['buy_price'])
            if user['balance'] >= property_price:
                user['balance'] -= property_price
                if 'properties' not in user:
                    user['properties'] = []
                user['properties'].append(property_name)
        elif 'sell_property' in request.form:
            property_name = request.form['sell_property']
            property_price = int(request.form['sell_price'])
            if property_name in user['properties']:
                user['balance'] += property_price
                user['properties'].remove(property_name)
        elif 'buy_stock' in request.form:
            stock_name = request.form['buy_stock']
            stock_price = int(request.form['buy_price'])
            stock_quantity = int(request.form['buy_quantity'])
            if user['balance'] >= stock_price * stock_quantity:
                user['balance'] -= stock_price * stock_quantity
                if 'stocks' not in user:
                    user['stocks'] = {}
                if stock_name not in user['stocks']:
                    user['stocks'][stock_name] = 0
                user['stocks'][stock_name] += stock_quantity
        elif 'sell_stock' in request.form:
            stock_name = request.form['sell_stock']
            stock_price = int(request.form['sell_price'])
            stock_quantity = int(request.form['sell_quantity'])
            if stock_name in user['stocks'] and user['stocks'][stock_name] >= stock_quantity:
                user['balance'] += stock_price * stock_quantity
                user['stocks'][stock_name] -= stock_quantity
                if user['stocks'][stock_name] == 0:
                    del user['stocks'][stock_name]
    return render_template('dashboard.html', user=user)
