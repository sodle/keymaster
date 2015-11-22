from flask import Flask, request, abort, redirect, url_for
import orm
import datetime
from urlparse import urljoin
import config
application = Flask(__name__)

@application.route('/k', methods=['POST'])
def upload_key():
    if 'public_key' in request.form:
        key_hashid = orm.upload_key(request.form['public_key'])
        if key_hashid and key_hashid != '':
            if 'redirect' in request.form:
                return redirect(url_for('show_key', key_id=key_hashid))
            else:
                rel_url = url_for('show_key', key_id=key_hashid)
                fq_url = urljoin(config.BASE_SHORTENER_URL, rel_url)
                return fq_url
        else:
            abort(500)
    else:
        abort(400)

@application.route('/k/<key_id>')
def show_key(key_id):
    key_obj = orm.fetch_key(key_id)
    if key_obj:
        lifetime = key_obj[3] - datetime.datetime.now()
        rel_url = url_for('show_key', key_id=key_id)
        fq_url = urljoin(config.BASE_SHORTENER_URL, rel_url)
        return ("Your public key is: " + key_obj[2] + ". "
                "Expires in " + str(lifetime).split('.')[0] + ". "
                "URL: " + fq_url + "."
                )
    else:
        abort(404)

@application.route('/k/<key_id>/extend', methods=['POST'])
def extend_key(key_id):
    if orm.fetch_key(key_id):
        orm.extend_key(key_id)
        return redirect(url_for('show_key', key_id=key_id))
    else:
        abort(404)

@application.route('/k/<key_id>/expire', methods=['POST'])
def expire_key(key_id):
    if orm.fetch_key(key_id):
        orm.expire_key(key_id)
        return redirect('/')
    else:
        abort(404)

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
