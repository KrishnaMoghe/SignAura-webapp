from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Load models
static_model = tf.keras.models.load_model("./GestureModels/static_gesture_model.h5")
dynamic_model = tf.keras.models.load_model("./GestureModels/dynamic_gesture_model.h5")

last_gesture = "--"
last_update_time = 0
gesture_display_duration = 2.5  # seconds


# Gesture labels
static_gestures = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
dynamic_gestures = ['bzk', 'close', 'drink', 'goodbye', 'hello', 'rotate', 'walk']
desired_seq_length = 50

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Global state
cap = None
streaming = False
mode = "static"  # or "dynamic"
sequence = []
last_gesture = None
last_confidence = 0

last_update_time = time.time()
def gen_frames():
    global cap, streaming, mode, sequence, last_gesture, last_confidence, last_update_time

    cap = cv2.VideoCapture(1)  # Use 0 for default camera
    streaming = True

    while streaming:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark], dtype=np.float32)

            if mode == "static":
                input_data = np.expand_dims(landmarks.flatten(), axis=[0, -1])
                prediction = static_model.predict(input_data)
                gesture = static_gestures[np.argmax(prediction)]
                socketio.emit('gesture', {'gesture': gesture})
                print(f"[Static] Predicted: {gesture}")

            elif mode == "dynamic":
                sequence.append(landmarks)
                if len(sequence) == desired_seq_length:
                    input_sequence = np.array(sequence).reshape(1, desired_seq_length, -1)
                    prediction = dynamic_model.predict(input_sequence)
                    predicted_index = np.argmax(prediction)
                    predicted_gesture = dynamic_gestures[predicted_index]
                    confidence = np.max(prediction)

                    if confidence >= 0.7:
                        last_gesture = predicted_gesture
                        last_confidence = confidence
                        last_update_time = time.time()
                        print(f"[Dynamic] New Prediction: {last_gesture} ({confidence*100:.1f}%)")
                    else:
                        print(f"[Dynamic] Low confidence: {confidence*100:.1f}%")

                    sequence = []

                # Emit last valid gesture if still within display duration
                if time.time() - last_update_time < gesture_display_duration:
                    socketio.emit('gesture', {'gesture': last_gesture})
                else:
                    socketio.emit('gesture', {'gesture': '--'})


        # Display gesture overlay
        if mode == "dynamic" and last_gesture is not None:
            cv2.putText(frame, f"Gesture: {last_gesture} ({last_confidence*100:.1f}%)",
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('stop_camera')
def stop_camera():
    global streaming
    streaming = False

@socketio.on('set_mode')
def set_mode(data):
    global mode, sequence, last_gesture, last_confidence
    mode = data.get('mode', 'static')
    sequence = []
    last_gesture = None
    last_confidence = 0
    print(f"[Mode] Switched to {mode} mode")

if __name__ == '__main__':
    socketio.run(app, debug=True)
