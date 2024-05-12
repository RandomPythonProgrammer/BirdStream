import flask
import cv2

app = flask.Flask(__name__)
camera = cv2.VideoCapture(0)


def get_frames():
    while True:
        status, frame = camera.read()
        status, buffer = cv2.imencode('.jpg', frame)
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n'


@app.route('/stream')
def stream():
    return flask.Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def home():
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.run()
