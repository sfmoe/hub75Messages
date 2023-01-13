import flask

import database
request = flask.request
import makegif


message_queue, default_messages = database.message_db()

app = flask.Flask(__name__)
app.config.update(
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True
    
)


@app.route("/")
def home():
    return flask.render_template("index.html", default_messages=default_messages, message_queue=message_queue)
@app.route('/messages', methods= ['POST', 'PUT', 'DELETE'])
def messages():
    if request.method == 'POST':
        multiline = False
        scrolltype = request.form.get("scrolltype")

        message = request.form.get("message")

        if(request.form.get("multiline")=="multiline"):
            multiline=True

        makegif.makeGif(message, scrolltype, multiline)
        return({"status": "Created image", "message": message, "multiline": multiline, "scrolltype": scrolltype})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    con.close()
