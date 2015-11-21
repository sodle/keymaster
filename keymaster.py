from flask import Flask, request
application = Flask(__name__)

@application.route('/k', methods=['POST'])
def upload_key():
    return str(request.form)

@application.route('/k/<key_id>')
def index(key_id):
    return 'Hello key #' + key_id

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
