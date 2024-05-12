import flask
import cv2
import sys

app = flask.Flask(__name__)
camera = cv2.VideoCapture(0)


def get_frames():
    while True:
        status, frame = camera.read()
        status, buffer = cv2.imencode('.jpg', frame)
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n'


@app.route('/stream')
def stream():
    return flask.Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/embed')
def embed():
    return flask.render_template('embed.html')


@app.route('/')
def home():
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.run(host=sys.argv[1], port=int(sys.argv[2]))
