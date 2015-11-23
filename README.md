# Keymaster
## *There is no password, only Zuul.*

---
[![Build Status](https://travis-ci.org/sodle/keymaster.svg?branch=master)](https://travis-ci.org/sodle/keymaster)

Keymaster provides an easy way to upload your SSH keys to services like Github and Bitbucket. It's useful for authorizing machines from which you can't easily access a web browser or your LastPass account.

### How it works:
1. You upload your public key to the web app using one of our clients (coming soon):
    - CLI
    - Eclipse plugin
    - IntelliJ plugin
    - GUI
2. The client returns a short URL that can be accessed from any computer.
3. You use the link to authenticate with Github and Bitbucket to install your key.
4. After a short time, the link expires and your key disappears from the server. Privacy protected!

---

The app is written in Flask and connects to a Postgres database.

### Server requirements:
- Linux with systemd (for now)
- Python 2.7
- Postgres server with development headers
- Nginx
- libpcre3 and libpcre3-dev

### Server installation:
1. Install dependencies
    1. Install Python 2.7, headers, PCRE, Nginx, Postgres through your preferred package manager
    2. `sudo pip install -r requirements.txt`
2. Set up your database
    1. Create a Postgres user and database for Keymaster
    2. `psql -d <database> -U <user> -f db_init.sql`
3. Configure uWSGI
    1. Update paths, usernames, and groups in `daemon/keymaster.ini` and `daemon/keymaster.service`
    2. Copy or symlink `daemon/keymaster.service` to `/etc/systemd/system/keymaster.service`
    3. `sudo service keymaster start`
    4. `sudo service keymaster enable`
4. Configure Nginx passthrough
    1. Update paths in `daemon/keymaster.nginx`
    2. Copy or symlink `daemon/keymaster.nginx` to `/etc/nginx/conf.d/keymaster`
    3. `sudo service nginx restart`
5. Copy `config.spec.py` to `config.py` and update the built-in settings.
