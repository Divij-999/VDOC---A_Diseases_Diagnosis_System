
# 🩺 VDOC : A Diseases Diagnosis System

---

## 🛠️ Technology Used :
- **Frontend** : React
- **Backend** : Django
- **Chatbot** : Rasa
- **Database** : PostgreSQL

---

## ⚙️ Solutions for Common Errors in Frontend and Backend

### 🔧 Frontend
- If `module not found` error occurs, run:
```bash
npm install
```

### 🔧 Backend - Chatbot
- If Rasa is not installed, install it using Conda / Anaconda:
```bash
conda create -n rasa_bot python=3.9
conda activate rasa_bot
pip install rasa
```

### 🔧 Backend
- Install required packages:
```bash
pip install -r requirements.txt
```

---

## 🗄️ Run Migrations Before Starting Website
```bash
conda activate rasa_bot
cd ./backend/vdocBackend/
python manage.py makemigrations
python manage.py migrate
```

---

## 🔑 Update Database Credentials
- Go to:
```bash
cd ./backend/
```
- Update `.env` file:
```plaintext
DATABASE_PASSWORD = your_password
```

---

## 📥 Insert Dataset
- Insert the CSV file provided in the `dataset` folder into your PostgreSQL database.

---

## 🚀 Steps to Run Website

### 1️⃣ Frontend (Terminal 1)
```bash
conda activate rasa_bot
cd ./frontend/
npm start
```

### 2️⃣ Backend

#### 2.1 Terminal 2 - Django Backend
```bash
conda activate rasa_bot
cd ./backend/vdocBackend/
python manage.py runserver
```

#### 2.2 Terminal 3 - Rasa Chatbot API
```bash
conda activate rasa_bot
cd ./backend/vdocBackend/rasa/
rasa run --enable-api --cors "*"
```

#### 2.3 Terminal 4 - Rasa Actions
```bash
conda activate rasa_bot
cd ./backend/vdocBackend/rasa/
rasa run actions
```

---

## ©️ Copyright
Divij Modi  
📧 Contact: dmodi2806@gmail.com
