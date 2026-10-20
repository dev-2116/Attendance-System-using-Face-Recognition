# Smart Attendance System Using Face Recognition

An automated attendance management system built with **Python, OpenCV, and Machine Learning**. The system detects and recognizes registered faces through a live webcam feed and records attendance with the corresponding date and time, reducing the need for manual attendance tracking.

## ✨ Features

- **Face Detection:** Detects faces from a live webcam feed using OpenCV.
- **Face Recognition:** Identifies registered individuals using a K-Nearest Neighbors (KNN) classifier.
- **Automated Attendance:** Records attendance for recognized individuals.
- **Timestamp Recording:** Stores the name, date, and time of attendance.
- **CSV-Based Storage:** Saves attendance records in CSV format for easy access and analysis.
- **Live Camera Feed:** Displays the camera feed with face recognition results.
- **Text-to-Speech Feedback:** Provides voice feedback when supported by the system.
- **Simple Interface:** Offers a straightforward way to monitor attendance in real time.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| OpenCV | Webcam access and image processing |
| NumPy | Numerical operations |
| Scikit-learn | KNN-based face recognition |
| Pickle | Loading and storing trained model data |
| CSV | Attendance record storage |
| PyWin32 | Optional text-to-speech support on Windows |

## 📂 Project Structure

```text
Attendance-System-using-Face-Recognition/
│
├── data/                   # Face data or training data
├── attendance/             # Attendance records (if configured)
├── *.py                    # Python source files
├── *.pkl                   # Saved model or training data (if present)
├── Attendance.csv          # Generated attendance records
├── requirements.txt        # Project dependencies (if present)
└── README.md               # Project documentation
```

*Note: The structure above is illustrative. Filenames and folders may differ depending on the files included in the repository.*

## 🚀 Getting Started

### 1. Prerequisites

Make sure you have installed:

- Python 3.9 or later
- Git
- A working webcam
- pip, Python's package manager

### 2. Clone the Repository

```bash
git clone https://github.com/dev-2116/Attendance-System-using-Face-Recognition.git
```

Navigate to the project directory:

```bash
cd Attendance-System-using-Face-Recognition
```

### 3. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux or macOS:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

Install the required libraries:

```bash
pip install opencv-python numpy scikit-learn
```

For optional text-to-speech support on Windows:

```bash
pip install pywin32
```

### 5. Run the Application

Run the Python script responsible for starting the webcam and recognizing faces:

```bash
python test.py
```

Replace `test.py` with the actual filename of your application's main Python script.

If the project requires a separate face-data collection or model-training step, complete that step before starting the attendance application.

## ⚙️ How It Works

1. **Face Data Collection:** Collect face samples for the individuals who need to be recognized.
2. **Model Preparation:** Prepare the face data and train or load the KNN classifier.
3. **Live Face Detection:** Capture frames from the webcam using OpenCV.
4. **Face Recognition:** Extract face information and use the trained classifier to identify registered individuals.
5. **Attendance Logging:** Record the recognized person's name along with the current date and time.
6. **Data Storage:** Save attendance records in a CSV file for future reference.

## 📊 Attendance Records

Attendance records are stored in CSV format, which can be opened using Microsoft Excel, Google Sheets, or any text editor.

## 💻 System Requirements

- Operating System: Windows, Linux, or macOS
- Python: 3.9+
- Camera: Built-in or external webcam
- Memory: Sufficient to run Python, OpenCV, and the recognition model

Some features, particularly text-to-speech functionality, may be platform-specific.

## 🔒 Privacy and Responsible Use

- Obtain consent before collecting or processing anyone's facial data.
- Store face data and attendance records securely.
- Restrict access to personal information.
- Provide a manual attendance alternative when face recognition fails.
- Review attendance records for errors before using them for official purposes.

## 🔮 Future Improvements

- Web-based attendance dashboard
- Admin and student authentication
- Database integration using MySQL or MongoDB
- Daily and monthly attendance reports
- Duplicate attendance prevention
- Exportable reports and analytics
- Improved recognition accuracy and liveness detection

## 🎯 Project Objective

The objective of this project is to demonstrate how computer vision and machine learning can be applied to automate attendance management, improve convenience, and reduce the effort required for manual record keeping.

## 👨‍💻 Author

**Dev Patel**

- GitHub: [@dev-2116](https://github.com/dev-2116)
- Project Repository: [Attendance System using Face Recognition](https://github.com/dev-2116/Attendance-System-using-Face-Recognition)

---

⭐ If you find this project useful, consider giving the repository a star!

