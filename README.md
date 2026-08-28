# Bus Entry & Exit Tracking System

A Python Flask project foundation for a real-time camera and cloud-based bus entry and exit tracking system.

This project currently has:

- Flask backend
- Clean project structure
- Environment-based configuration
- Logging
- Dashboard frontend
- Dashboard JSON API
- One camera slot in the dashboard
- Zero-state data because no camera is configured yet

Camera, detection, OCR, database, cloud storage, and real tracking logic are still pending.

## 1. Project Goal

The final system should:

1. Connect to one camera.
2. Capture frames from the camera.
3. Detect bus movement or bus presence.
4. Read bus number or plate text using OCR.
5. Decide whether the bus is entering or exiting.
6. Store each event in a database.
7. Show live counts on the dashboard.
8. Generate reports.
9. Optionally upload images or logs to cloud storage.

## 2. Current Folder Structure

```text
Bus_Entry_Exit_System/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── camera/
├── detection/
├── ocr/
├── database/
├── dashboard/
├── services/
├── models/
├── reports/
├── storage/
├── logs/
├── tests/
├── deployment/
├── docs/
├── templates/
└── static/
```

## 3. Architecture

The project follows Clean Architecture ideas:

- `app.py`: Flask application factory and app startup.
- `config.py`: Environment variable and app configuration management.
- `dashboard/`: Dashboard routes and dashboard API.
- `templates/`: HTML pages.
- `static/`: CSS and JavaScript assets.
- `models/`: Domain and response models.
- `services/`: Application services and business logic.
- `camera/`: Future camera connection logic.
- `detection/`: Future bus detection logic.
- `ocr/`: Future OCR logic.
- `database/`: Future database connection and repositories.
- `reports/`: Future report generation logic.
- `storage/`: Future local/cloud storage adapters.
- `logs/`: Runtime log files.
- `tests/`: Automated tests.
- `deployment/`: Production deployment files.
- `docs/`: Extra technical documentation.

## 4. Requirements

- Python 3.12 recommended
- Flask 3.x
- Windows PowerShell commands are used in this README

Note: the current local virtual environment may use Python 3.13 if that is the Python version installed on your machine.

## 5. Create Virtual Environment

Run this from the project root:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Check Python version:

```powershell
python --version
```

## 6. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 7. Create Environment File

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Open `.env` and update values if needed.

Important:

- Do not commit `.env`.
- Keep real secrets out of Git.
- Change `SECRET_KEY` before production deployment.

## 8. Run the Application

```powershell
python app.py
```

Open the dashboard:

```text
http://127.0.0.1:5000/
```

Alternative dashboard URL:

```text
http://127.0.0.1:5000/dashboard
```

Health check:

```text
http://127.0.0.1:5000/health
```

Dashboard API:

```text
http://127.0.0.1:5000/api/dashboard/summary
```

## 9. Current Dashboard Behavior

The dashboard is working, but it currently shows zero-state data.

That means:

- Active cameras: `0`
- Entries today: `0`
- Exits today: `0`
- Pending reviews: `0`
- Yard occupancy: `0`
- Average confidence: `0`
- Camera count: `1`
- Camera status: `not_configured`

This is correct because no real camera source is configured yet.

The dashboard data comes from:

```text
services/dashboard_service.py
```

The dashboard route is:

```text
dashboard/routes.py
```

The frontend files are:

```text
templates/dashboard.html
static/css/dashboard.css
static/js/dashboard.js
```

## 10. Test the Current App

Run a quick route test:

```powershell
python -c "from app import create_app; app = create_app(); client = app.test_client(); print(client.get('/').status_code); print(client.get('/health').get_json()); print(client.get('/api/dashboard/summary').get_json())"
```

Expected result:

- `/` returns `200`
- `/health` returns status `ok`
- `/api/dashboard/summary` returns dashboard JSON

## 11. Pending Work

The following features are still pending.

### Step 1: Camera Connection

Create logic to connect to one camera.

The camera source can be:

```text
0
```

for laptop webcam, or:

```text
rtsp://...
http://...
```

for IP camera or CCTV stream.

Recommended future files:

```text
camera/camera_config.py
camera/camera_service.py
camera/frame_reader.py
```

Expected output:

- Camera connected or not connected status
- Latest frame available for processing
- Camera FPS
- Camera error messages

### Step 2: Database Setup

Add a database to store tracking records.

Recommended fields:

- `id`
- `bus_number`
- `event_type`
- `camera_id`
- `confidence`
- `image_path`
- `occurred_at`
- `review_status`
- `created_at`

Recommended future files:

```text
database/connection.py
database/repositories.py
models/tracking_event.py
```

### Step 3: Detection Logic

Add bus detection logic.

This can later use:

- OpenCV
- YOLO
- A cloud vision API
- Any trained detection model

Recommended future files:

```text
detection/detector.py
detection/detection_result.py
```

Expected output:

- Bus detected: yes/no
- Bounding box
- Detection confidence

### Step 4: OCR Logic

Add OCR logic to read bus number or plate text.

Possible OCR options:

- EasyOCR
- Tesseract
- PaddleOCR
- Cloud OCR API

Recommended future files:

```text
ocr/ocr_engine.py
ocr/ocr_result.py
```

Expected output:

- Detected text
- OCR confidence
- Cropped plate/bus number image path

### Step 5: Entry/Exit Decision Logic

Because you have only one camera, the system needs a rule to decide entry vs exit.

Possible approaches:

- Camera placed only at entry point: every detected bus is an entry.
- Camera placed only at exit point: every detected bus is an exit.
- Camera sees both directions: use movement direction.
- Manual gate mode: configure camera as `entry`, `exit`, or `both`.

Recommended future config:

```text
CAMERA_MODE=entry
```

or:

```text
CAMERA_MODE=exit
```

or:

```text
CAMERA_MODE=both
```

### Step 6: Connect Real Data to Dashboard

After camera and database are ready, replace zero-state dashboard data with real records.

Update:

```text
services/dashboard_service.py
```

Dashboard should then show:

- Real active camera count
- Real entries today
- Real exits today
- Real pending reviews
- Real event list
- Real hourly chart
- Real camera status

### Step 7: Reports

Add reports for:

- Daily entries
- Daily exits
- Bus-wise history
- Camera-wise activity
- Manual review records

Recommended future files:

```text
reports/report_service.py
reports/export_service.py
```

Possible export formats:

- CSV
- Excel
- PDF

### Step 8: Cloud Storage

Use cloud storage only after local storage works.

Possible storage targets:

- Local filesystem
- AWS S3
- Google Cloud Storage
- Azure Blob Storage

Recommended future files:

```text
storage/local_storage.py
storage/cloud_storage.py
```

### Step 9: Tests

Add tests for:

- Config loading
- Health route
- Dashboard route
- Dashboard service
- Camera service
- Detection service
- OCR service
- Database repositories

Recommended command:

```powershell
pytest
```

### Step 10: Deployment

Production deployment should include:

- Secure `.env`
- Real database
- Production WSGI server
- Log rotation
- Reverse proxy
- Service manager
- Backup plan

For Linux production, use Gunicorn:

```bash
gunicorn "app:create_app()"
```

For Windows local development, keep using:

```powershell
python app.py
```

## 12. Recommended Build Order

Build the system in this order:

1. Finish dashboard zero-state view.
2. Add one-camera configuration.
3. Add camera connection check.
4. Add camera frame capture.
5. Add database models and tables.
6. Save raw tracking events.
7. Add bus detection.
8. Add OCR.
9. Add entry/exit decision logic.
10. Connect real data to dashboard.
11. Add reports.
12. Add tests.
13. Prepare deployment.

## 13. Important Notes

- Do not add fake dashboard counts.
- If no camera is configured, all tracking counts should stay `0`.
- If one camera is configured but not connected, active camera count should stay `0`.
- If one camera is connected, active camera count should become `1`.
- Entry and exit counts should increase only after real detection logic is added.
- OCR should not be implemented until camera frame capture is stable.

## 14. Useful Commands

Activate virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run app:

```powershell
python app.py
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Compile check:

```powershell
python -m compileall app.py dashboard models services
```

Open dashboard:

```text
http://127.0.0.1:5000/
```

## 15. Current Status

Completed:

- Flask app foundation
- Environment config
- Logging setup
- Dashboard page
- Dashboard API
- Colorful UI
- One-camera zero-state dashboard logic

Pending:

- Real camera connection
- Detection
- OCR
- Database
- Reports
- Cloud storage
- Automated tests
- Deployment setup
#   f i n a l _ y e a r _ p r o j e c t 
 
 
>>>>>>> f3d468e (first commit)
