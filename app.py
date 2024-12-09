from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_page():
    return 'Hakuna matata'

if __name__ == '__main__':
    app.run(debug=True)