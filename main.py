import flask

import database
request = flask.request

message_queue, default_messages = database.message_db()

app = flask.Flask(__name__)
app.config.update(
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True
    
)

def save_message(message):
     return(message)


@app.route("/")
def home():
    return flask.render_template("index.html", default_messages=default_messages, message_queue=message_queue)
@app.route('/messages', methods= ['POST', 'PUT', 'DELETE'])
def messages():
    if request.method == 'POST':
        message = request.form
        return save_message(message)



if __name__ == '__main__':
    app.run()
    con.close()