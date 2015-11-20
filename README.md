# Keymaster
## *There is no password, only Zuul.*

---

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
- Linux (for now)
- Python 2.7
- Postgres server
- Nginx

### Installation:
1. `sudo pip install -r requirements.txt`
2. *insert instructions for initializing database*
3. *insert instructions for setting up WSGI server*
4. *insert instructions for setting up Nginx reverse proxy*
5. *insert instructions for local configuration*
