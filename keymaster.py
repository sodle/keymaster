from flask import Flask, request, abort, redirect, url_for, render_template
import orm
import datetime
from urlparse import urljoin
import config
import crontab
import logging
from logging.handlers import TimedRotatingFileHandler as TRFHandler

application = Flask(__name__, template_folder='templates')
application.url_map.strict_slashes = False

# Logging handler
file_rotator = TRFHandler(config.LOGGING_LOCATION,
                          when=config.LOGGING_FREQUENCY,
                          backupCount=config.LOGGING_RETENTION
                          )
formatter = logging.Formatter('%(asctime)s %(message)s')
file_rotator.setLevel(logging.INFO)
file_rotator.setFormatter(formatter)
application.logger.addHandler(file_rotator)
application.logger.setLevel(logging.INFO)


application.logger.info("Server starting.")


@application.before_request
def pre_request_logging():
    if not(application.testing):
        application.logger.info(' '.join([
            request.remote_addr,
            request.method,
            request.url,
            request.data,
            ', '.join([': '.join(x) for x in request.headers])])
        )


@application.after_request
def post_request(response):
    log = "Finished with " + response.status
    application.logger.info(log)
    crontab.schedule.run_pending()
    return response


@application.route('/k', methods=['POST'])
def upload_key():
    if 'public_key' in request.form:
        if not(application.testing):
            log_entry = ("Uploading key \"" + request.form['public_key'] + "\""
                         " for IP " + request.remote_addr
                         )
            application.logger.info(log_entry)
        key_hashid = orm.upload_key(request.form['public_key'])
        if key_hashid and key_hashid != '':
            if 'redirect' in request.form:
                return redirect(url_for('show_key', key_id=key_hashid))
            else:
                rel_url = url_for('show_key', key_id=key_hashid)
                fq_url = urljoin(config.BASE_SHORTENER_URL, rel_url)
                return fq_url
        else:
            application.logger.error('Didn\'t get a db id back!')
            abort(500)
    else:
        application.logger.error('Request didn\'t contain a public key!')
        abort(400)


@application.route('/k/<key_id>')
@application.route('/k/<key_id>/')
def show_key(key_id):
    application.logger.info('Getting public key ' + key_id)
    key_obj = orm.fetch_key(key_id)
    if key_obj:
        lifetime = key_obj[3] - datetime.datetime.now()
        rel_url = url_for('show_key', key_id=key_id)
        fq_url = urljoin(config.BASE_SHORTENER_URL, rel_url)
        return render_template('show_key.html',
                               key_id=key_id,
                               public_key=key_obj[2],
                               expires_in=str(lifetime).split('.')[0]
                               )
    else:
        application.logger.error('Key not found!')
        abort(404)


@application.route('/k/<key_id>/key')
@application.route('/k/<key_id>/key/')
def show_raw_key(key_id):
    application.logger.info('Getting raw public key ' + key_id)
    key_obj = orm.fetch_key(key_id)
    if key_obj:
        return key_obj[2]
    else:
        application.logger.error('Key not found!')
        abort(404)


@application.route('/k/<key_id>/extend', methods=['POST'])
def extend_key(key_id):
    application.logger.info('Extending key ' + key_id)
    if orm.fetch_key(key_id):
        orm.extend_key(key_id)
        return redirect(url_for('show_key', key_id=key_id))
    else:
        application.logger.error('Key not found!')
        abort(404)


@application.route('/k/<key_id>/expire', methods=['POST'])
def expire_key(key_id):
    application.logger.info('Expiring key ' + key_id)
    if orm.fetch_key(key_id):
        orm.expire_key(key_id)
        return redirect('/')
    else:
        application.logger.error('Key not found!')
        abort(404)

if __name__ == '__main__':
    application.run(host='0.0.0.0')
