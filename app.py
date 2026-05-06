from flask import Flask, render_template, Response, request
import cv2
import random

app = Flask(__name__)

# Global camera
camera = None

# 9 Emotions
emotions = [
    "Happy", "Sad", "Angry", "Neutral",
    "Excited", "Relaxed", "Bored", "Fear", "Surprised"
]

# YouTube SEARCH LINKS (always working)
music = {
    "Happy": [
        "https://www.youtube.com/results?search_query=telugu+happy+songs",
        "https://www.youtube.com/results?search_query=telugu+party+songs",
        "https://www.youtube.com/results?search_query=telugu+dance+hits"
    ],
    "Sad": [
        "https://www.youtube.com/results?search_query=telugu+sad+songs",
        "https://www.youtube.com/results?search_query=telugu+melody+songs",
        "https://www.youtube.com/results?search_query=telugu+love+failure+songs"
    ],
    "Angry": [
        "https://www.youtube.com/results?search_query=telugu+mass+bgm",
        "https://www.youtube.com/results?search_query=telugu+powerful+songs",
        "https://www.youtube.com/results?search_query=telugu+fight+bgm"
    ],
    "Neutral": [
        "https://www.youtube.com/results?search_query=telugu+lofi",
        "https://www.youtube.com/results?search_query=telugu+instrumental",
        "https://www.youtube.com/results?search_query=telugu+background+music"
    ],
    "Excited": [
        "https://www.youtube.com/results?search_query=telugu+energetic+songs",
        "https://www.youtube.com/results?search_query=telugu+festival+songs",
        "https://www.youtube.com/results?search_query=telugu+fast+beats"
    ],
    "Relaxed": [
        "https://www.youtube.com/results?search_query=telugu+relaxing+songs",
        "https://www.youtube.com/results?search_query=telugu+soft+melodies",
        "https://www.youtube.com/results?search_query=telugu+peaceful+music"
    ],
    "Bored": [
        "https://www.youtube.com/results?search_query=telugu+trending+songs",
        "https://www.youtube.com/results?search_query=telugu+viral+songs",
        "https://www.youtube.com/results?search_query=telugu+top+hits"
    ],
    "Fear": [
        "https://www.youtube.com/results?search_query=telugu+horror+bgm",
        "https://www.youtube.com/results?search_query=telugu+thriller+music",
        "https://www.youtube.com/results?search_query=telugu+suspense+bgm"
    ],
    "Surprised": [
        "https://www.youtube.com/results?search_query=telugu+trending+hits",
        "https://www.youtube.com/results?search_query=telugu+new+songs",
        "https://www.youtube.com/results?search_query=telugu+chartbusters"
    ]
}

# Emoji map
emoji_map = {
    "Happy": "😄", "Sad": "😢", "Angry": "😡", "Neutral": "😐",
    "Excited": "🤩", "Relaxed": "😌", "Bored": "😴",
    "Fear": "😨", "Surprised": "😲"
}

# 🎥 Generate camera frames
def generate_frames():
    global camera
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()


# ================= ROUTES ================= #

# Home
@app.route('/')
def home():
    return render_template("index.html")


# Mode selection
@app.route('/mode')
def mode():
    return render_template("mode.html")


# Manual emotion selection
@app.route('/manual', methods=['POST'])
def manual():
    emotion = request.form.get('emotion')

    if emotion not in emotions:
        emotion = "Neutral"

    emoji = emoji_map.get(emotion, "🙂")

    # Pick random 3 links
    songs = random.sample(music[emotion], 3)

    return render_template(
        "result.html",
        emotion=emotion,
        emoji=emoji,
        songs=songs
    )


# Webcam page
@app.route('/detecting')
def detecting():
    return render_template("detecting.html")


# Video streaming
@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Result from webcam (currently random emotion)
@app.route('/result')
def result():
    global camera

    # Stop camera
    if camera is not None and camera.isOpened():
        camera.release()

    # Random emotion (placeholder for AI)
    emotion = random.choice(emotions)

    emoji = emoji_map.get(emotion, "🙂")

    # Random 3 songs
    songs = random.sample(music[emotion], 3)

    return render_template(
        "result.html",
        emotion=emotion,
        emoji=emoji,
        songs=songs
    )


# Run app
if __name__ == "__main__":
    app.run(debug=True)