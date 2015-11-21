from flask import Flask
applicationlication = Flask(__name__)

@application.route('/')
def index():
    return 'Hello world!'

if __name__ == '__main__':
    application.run(host='0.0.0.0')
