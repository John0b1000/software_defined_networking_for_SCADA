#https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Flask, render_template
#from flask_cors import CORS, cross_origin
import sys

app = Flask(__name__)
#CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

def main(argv):
    """ Main Program """

    app.run(host="127.0.0.1", port=5001, debug=True, ssl_context=("cert.pem", "key.pem"))
    # exit gracefully
    return 0

if __name__ == "__main__":
  main(sys.argv)