import flask
import requests
import database
request = flask.request
import makegif
import subprocess
import pathlib
import os
import scroll_redemption
from threading import Thread

working_dir = pathlib.Path(__file__).parent.absolute()
dirscroll = os.path.join(working_dir, "scroll_redemption.py")

message_queue, default_messages = database.message_db()

app = flask.Flask(__name__)
app.config.update(
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True
    
)


def signstatus(option):
    sub = subprocess.run([f"systemctl {option} displaygif"], shell=True)
    return sub


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


@app.route("/sys", methods= ['POST'])
def sys():
    sub = ''
    if request.method == 'POST':
        if(request.form.get("status") == "restart"):
            sub = signstatus("restart")
        elif (request.form.get("status") == "start"):
            sub = signstatus("start")
        elif (request.form.get("status") == "stop"):
            sub = signstatus("stop")
        else:
            sub = signstatus("restart")

    return({"status": "Ready"})
@app.route("/redemption", methods= ['POST'])
def redemption():
    text = request.form.get("redemption")
    thread = Thread(target = scroll_redemption.start, args = (text,) )
    thread.start()
    thread.join()
    # scroll_redemption.start(text)
    return ({"status":"done"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    con.close()
