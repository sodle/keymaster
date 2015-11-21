from flask import Flask
application = Flask(__name__)

@application.route('/k/<key_hash>')
def index(key_hash):
    return 'Hello key #' + key_hash

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
