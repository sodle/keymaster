from flask import Flask
application = Flask(__name__)

@application.route('/k/asdf')
def index():
    return 'Hello key #'

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
