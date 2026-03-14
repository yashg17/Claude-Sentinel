from flask import Flask, request
import logging

app = Flask(__name__)
# Production style logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

@app.route('/')
def home():
    user_input = request.args.get('user', 'guest')
    app.logger.info(f"Access from user: {user_input}")
    return f"Welcome {user_input}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
