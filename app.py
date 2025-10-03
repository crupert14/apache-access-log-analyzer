from flask import Flask, render_template
import logAnalyzer

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', ip_addr_app_count=logAnalyzer.ip_addr_app_count)

if __name__ == '__main__':
    app.run(debug=True)