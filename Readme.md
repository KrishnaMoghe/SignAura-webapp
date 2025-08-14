# 🖐️ SignAura – Accessible Sign Language Learning & Communication Platform

SignAura is an **AI-powered web application** designed to bridge the communication gap for the deaf and mute community, with a focus on **Gujarati Sign Language (GSL)**.  
It integrates **real-time gesture recognition**, an **interactive sign language chatbot**, and **learning modules** into a unified platform.  

This repository contains the **web application** codebase, including:
- **Static & dynamic gesture recognition**
- **SignMate chatbot**
- **User authentication**
- **Web-based UI integration**

---

## 🌟 Features

### 🎯 Core Functionalities
- **Real-time Gesture Recognition**
  - **Static gestures** (0–9 digits)
  - **Dynamic gestures** (e.g., hello, goodbye, drink, rotate, walk)
  - Uses **MediaPipe** for landmark extraction and **deep learning models** for classification.

- **SignMate Chatbot**
  - Ask questions like _"What is the gesture for thank you?"_
  - Learns from user input for unknown gestures.
  - Stores custom gestures in a persistent CSV.

- **Two-way Communication**
  - Supports both **text-to-sign** and **sign-to-text** workflows.
  - Enables interactive learning and communication for students.

- **Authentication**
  - User login & signup (Node.js backend for authentication logic).
  - Secure access for personalized features.

---

## 🏗️ Technology Stack

| Component         | Technology |
|-------------------|------------|
| **Frontend**      | HTML, CSS, JavaScript, React (optional integration) |
| **Backend**       | Flask (Python), Flask-SocketIO, Node.js |
| **ML Models**     | TensorFlow/Keras, NumPy |
| **Gesture Tracking** | MediaPipe Hands |
| **Data Storage**  | CSV files for gesture dictionary |
| **Real-time Streaming** | OpenCV video feed over WebSocket |
| **Deployment**    | Render / Railway / Heroku / AWS |

---

## 📂 Repository Structure

```
SignAura - Webapp/
│
├── server/                    # Backend server directory
│   ├── app.py                # Main Flask app (gesture recognition + chatbot)
│   ├── signmate.py           # SignMate chatbot implementation
│   ├── index.js              # Node.js authentication server
│   ├── package.json          # Node.js dependencies
│   ├── package-lock.json     # Node.js lock file
│   ├── gestures.csv          # Base gesture dictionary
│   ├── templates/
│   │   └── index.html        # Web UI template
│   ├── GestureModels/        # Pre-trained ML models
│   │   ├── static_gesture_model.h5
│   │   └── dynamic_gesture_model.h5
│   ├── Middlewares/          # Custom middleware functions
│   ├── Routes/               # API route definitions
│   ├── Controllers/          # Business logic controllers
│   ├── Models/               # Data models
│   ├── util/                 # Utility functions
│   ├── venv/                 # Python virtual environment
│   └── node_modules/         # Node.js dependencies
│
├── client/                    # Frontend React application
│   ├── src/                  # React source code
│   ├── public/               # Static assets
│   ├── package.json          # React dependencies
│   ├── package-lock.json     # React lock file
│   └── node_modules/         # React dependencies
│
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation

````

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/Login-Signup-page.git
cd Login-Signup-page
````

### 2️⃣ Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Install Node.js dependencies (for authentication)

```bash
cd server
npm install
```

### 4️⃣ Place ML models

Make sure the following models are in `GestureModels/`:

* `static_gesture_model.h5`
* `dynamic_gesture_model.h5`

*(If you don’t have them, train using the SignAura training pipeline or request from the project maintainers.)*

### 5️⃣ Run the backend

```bash
python app.py
```

This starts the **Flask server** for gesture recognition & chatbot.

### 6️⃣ Run authentication server

```bash
node index.js
```

---

## 🎮 Usage

1. **Open the app** in your browser:

   ```
   http://localhost:5000
   ```

2. **Select Gesture Mode**

   * *Static* → for hand signs like numbers.
   * *Dynamic* → for motion-based gestures.

3. **Interact with SignMate Chatbot**

   * Type: `What is the gesture for hello?`
   * If unknown, teach new gestures via `/signmate/teach` endpoint.

4. **Authenticate (optional)**

   * Sign up or log in for personalized tracking.

---

## 🔍 API Endpoints

### Gesture Recognition

* **`GET /video`** – Live camera stream with gesture overlay.
* **WebSocket Events**

  * `set_mode` – Switch between `"static"` and `"dynamic"`.
  * `stop_camera` – Stop streaming.

### SignMate Chatbot

* **`POST /signmate/ask`**

  ```json
  { "message": "What is the gesture for hello?" }
  ```
* **`POST /signmate/teach`**

  ```json
  {
    "gesture": "thank you",
    "description": "Flat hand from chin moving outward",
    "confirm": true
  }
  ```

---

## 📊 Models & Accuracy

* **Static Gesture Model:** CNN, trained on custom dataset of 0–9 digits.
  *Accuracy:* \~97%
* **Dynamic Gesture Model:** LSTM, trained on sequence data of 50 frames per gesture.
  *Accuracy:* \~94%

---

## 🚀 Deployment

### Render / Railway

1. Push your repo to GitHub.
2. Connect to Render/Railway.
3. Set `python app.py` as start command.
4. Add environment variables if needed.

### Heroku

```bash
heroku create signaura-web
git push heroku main
```

---

## 🤝 Contributing

We welcome contributions to enhance SignAura:

1. Fork the repo
2. Create a new branch (`feature/new-gesture`)
3. Commit changes
4. Push and create a pull request

---

## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify.

---

## 📧 Contact

**Developed by:** SignAura Team
📩 Email: \[[krishnamoghe74@gmail.com](mailto:krishnamoghe74@gmail.com)]
🌐 Website: *coming soon*

