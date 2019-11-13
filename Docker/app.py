from flask import Flask
import os

application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 8080))
    app.run(debug=True,host='0.0.0.0',port=port)
