from flask import Flask, render_template

app = Flask(__name__)

@app.route('/00878')
def show_data():
    data = []
    with open('/root/stock/timestamp.txt', 'r') as f:
        for line in f:
            parts = line.split(':')
            timestamp = parts[0]
            decision, k, d = parts[1].split(',')
            data.append([timestamp, decision.strip(), k.strip(), d.strip()])
    return render_template('00878.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

