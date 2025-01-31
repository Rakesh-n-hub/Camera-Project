import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

# Initialize video capture variable
cap = None

def generate_frames():
    global cap
    while cap and cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        else:
            # Convert the frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield frame for video streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start_camera():
    """Start the camera."""
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)  # Open the camera
    return "Camera started"

@app.route('/stop')
def stop_camera():
    """Stop the camera."""
    global cap
    if cap:
        cap.release()
        cap = None
    return "Camera stopped"

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    global cap
    if cap:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Camera not started."

if __name__ == '__main__':
    app.run(debug=True)
