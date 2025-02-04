from flask import Flask, request, redirect, render_template
import urllib.parse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/redirect/<path:url>')
def secure_redirect(url):
    original_url = urllib.parse.unquote(url)
    return render_template('redirect.html', url=original_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)