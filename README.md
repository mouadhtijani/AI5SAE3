🎓 Student Project Management – Communication & Notifications








📘 Description

This project is a Student Project Management System designed to facilitate communication and automatic progress summarization between students and supervisors.

It provides real-time notifications, AI-based project progress summaries, and task tracking. The architecture integrates a FastAPI backend and a React frontend to ensure scalability and responsiveness.

This system is part of the “Gestion de la Communication et des Notifications” module within a final-year academic project.

🚀 Key Features

🧠 Automatic Project Summary Generation (AI-style template system)

🔔 Real-time Notifications via WebSockets

🧑‍💻 Project CRUD Operations

📈 Progress Tracking & Reporting

🌐 Modern React Frontend

⚡ FastAPI Backend with SQLAlchemy

🏗️ Project Structure
student-projects/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── crud.py
│   ├── database.py
│   ├── ws_manager.py
│   ├── tasks.py
│   └── ...
│
└── Frontend/
    ├── src/
    │   ├── components/
    │   ├── services/
    │   ├── pages/
    │   └── ...
    └── package.json

⚙️ Installation
1️⃣ Backend Setup (FastAPI)
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload


Backend runs on: http://127.0.0.1:8000

2️⃣ Frontend Setup (React)
cd Frontend
npm install
npm start


Frontend runs on: http://localhost:3000

🔌 API Endpoints
Method	Endpoint	Description
GET	/projects	Get all projects
GET	/projects/{id}	Get specific project details
POST	/projects/{id}/summaries/generate	Generate project summary
GET	/projects/{id}/summaries/latest	Retrieve latest summary
WS	/ws/projects/{id}	WebSocket notifications per project
🔔 Real-time Notification System

Each project has its own WebSocket channel for instant communication.
When a summary is generated or a task is updated, all connected clients receive an immediate notification.

Example message:

{
  "type": "summary_generated",
  "summary": "Le projet a été mis à jour avec un nouvel avancement..."
}

How it Works

The frontend opens a WebSocket connection to /ws/projects/{id}.

When a summary or update is triggered, the backend sends a JSON message.

The frontend displays it in real-time through a toast notification or a "Notifications" panel.

🧪 Testing the Notifications

Open two browser tabs on the same project page.

In tab A, click “Résumer l’avancement” to trigger summary generation.

Tab B will immediately display a notification via WebSocket.

You can also check your backend logs to confirm message delivery.

🧰 Technologies Used
Layer	Technology
Frontend	React.js, Axios, React-Toastify
Backend	FastAPI, SQLAlchemy, Pydantic
Database	SQLite (can be replaced with MySQL/PostgreSQL)
Real-time	WebSocket (FastAPI)
Language	Python 3.10+, JavaScript (ES6+)
🧑‍🏫 Author

Oussema Zarga
📍 Tunisia
🎓 Final Year Project – Gestion de la Communication et des Notifications
📧 Contact: [Your Email Here]

🖼️ Demo

(Add screenshots or short GIFs here to illustrate the interface and notifications.)

Example sections you can include:

Dashboard view

Summary generation panel

Notification toast example

📄 License

Distributed under the MIT License.
You are free to use, modify, and distribute this project for educational or professional purposes.

Would you like me to generate the badges with real GitHub links (repo stars, forks, last commit, etc.) for your exact repository name (e.g., OussemaZarga/student-projects)?

Vous avez dit :
Give me Full GITHUB readme ready to past in the github Yes
ChatGPT a dit :
Student Projects — Gestion de la Communication & Notifications

Projet de gestion des projets étudiants avec génération automatique de résumé d’avancement et notifications en temps réel.
Backend : FastAPI (Python) — Frontend : React (JS) — WebSockets pour notifications.

▲ Aperçu

Un petit système pour gérer des projets étudiants, suivre la progression, générer automatiquement des résumés d’avancement (logique IA / template) et envoyer des notifications en temps réel aux clients connectés. Idéal pour une démo, projet de fin d’études ou prototype.

🚀 Fonctionnalités principales

Création / lecture / mise à jour de projets (CRUD).

Suivi de la progression (progress).

Génération automatique de résumés d’avancement (backend).

Notifications en temps réel via WebSockets par projet.

Frontend React moderne avec toasts et panneau de notifications.

Mode dev simple (exécution synchrone) et option Celery pour production.

📁 Structure du dépôt (exemple)
student-projects/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── tasks.py
│   │   ├── ws_manager.py
│   │   └── ...
│   ├── requirements.txt
│   └── .env
└── Frontend/
    ├── src/
    │   ├── components/
    │   │   ├── App.js
    │   │   ├── ProjectList.js
    │   │   ├── SummaryCard.js
    │   │   ├── NotificationsButton.js
    │   │   └── NotificationCenter.js
    │   ├── services/api.js
    │   └── index.js
    ├── package.json
    └── .env

⚙️ Prérequis

Node.js (>= 16) et npm ou yarn

Python 3.10+

(Optionnel) Redis + Celery si tu veux exécuter les tâches en background en prod

PostgreSQL/MySQL ou SQLite pour dev

🧩 Installation & Lancement (copy–paste)
Backend (Windows)
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# Option dev : forcer génération synchrone (utile pour tester)
# set env and run:
$env:FORCE_SYNC_SUMMARY="1"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000

Backend (macOS / Linux)
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Option dev
export FORCE_SYNC_SUMMARY=1
python -m uvicorn app.main:app --reload --port 8000


Note: si tu veux Celery + Redis, installe Redis et démarre worker :

# installer redis & lancer redis-server
# lancer worker (depuis backend)
celery -A app.tasks.celery worker --loglevel=info

Frontend (Windows / macOS / Linux)
cd Frontend
npm install
npm start


Ouvre http://localhost:3000.

🔧 Configuration (.env)

Crée un fichier .env dans backend (exemple) :

POSTGRES_USER=pguser
POSTGRES_PASSWORD=pgpass
POSTGRES_DB=projectsdb
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DATABASE_URL=sqlite:///./dev.db
CELERY_BROKER=redis://localhost:6379/0
AI_API_KEY=        # si tu utilises une API externe
FORCE_SYNC_SUMMARY=1   # en dev pour ne pas utiliser Celery


Et dans Frontend/.env :

REACT_APP_API_URL=http://127.0.0.1:8000
REACT_APP_WS_URL=ws://127.0.0.1:8000    # ou wss:// si https

🧾 API & WebSocket (rapide)

GET /projects — lister projets

GET /projects/{id} — obtenir projet

POST /projects/{id}/summaries/generate — générer résumé

Dev : si FORCE_SYNC_SUMMARY=1, la route renvoie le résumé immédiatement.

Prod : si Celery configuré, la route peut renvoyer started_in_background et worker exécutera la génération.

GET /projects/{id}/summaries/latest — récupérer dernier résumé

WebSocket : ws://127.0.0.1:8000/ws/projects/{id} — recevoir notifications en temps réel

Message reçu côté front (exemple) :

{
  "type": "summary_generated",
  "project_id": 1,
  "summary": "Résumé généré...",
  "summary_id": 12
}

🧪 Tester les notifications (étapes)

Démarre backend (uvicorn) et frontend (npm start).

Ouvre deux onglets du navigateur sur http://localhost:3000 sur la même page projet.

Dans l’onglet A : clique Résumer l’avancement (ou appelle POST /projects/1/summaries/generate).

L’onglet B doit recevoir la notification via WebSocket et afficher le résumé / toast.

Si tu veux tester sans front : utilise l’endpoint de test (dev) POST /ws/test/{project_id} si présent, ou génère la summary via curl / Invoke-RestMethod.

PowerShell test example:

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/projects/1/summaries/generate
# ou pour /ws/test:
$body = @{ text = "Test notification" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/ws/test/1 -Body $body -ContentType "application/json"

✅ Dev tips & debugging rapide

Si POST renvoie started_in_background, la génération est gérée par Celery — vérifie que ton worker Celery tourne. Sinon active FORCE_SYNC_SUMMARY=1 pour dev.

Vérifie WebSocket dans DevTools → Network → WS (statut 101 = ok).

Si frontend servi en HTTPS, utilise wss:// pour WebSocket.

Ajoute print()/logging dans ws_manager.send_to_project pour tracer l’envoi.

🔒 Production notes

Ne laisse pas allow_origins=["*"] en production — configure les origines autorisées.

Sécurise la route d’API interne si tu utilises Celery pour appeler /internal/notify_ws.

Utilise PostgreSQL + Alembic pour migrations en prod.

Configure HTTPS + WSS et reverse proxy (nginx) devant uvicorn/gunicorn.

📸 Captures & Demo

Ajoute des captures d’écran ici :

Dashboard (liste projets)

Panel résumé + bouton Résumer

Panneau Notifications (historique)

📄 License

MIT License — voir le fichier LICENSE pour les détails.

✉️ Contact

Oussema Zarga — IA Project
Email : oussema.zarga@esprit.tn

GitHub : @Z4RGA 
