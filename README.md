# SmartExam Planner

SmartExam Planner is a web-based application that helps automate the **exam hall seating arrangement** process.  
It allows admins to upload student data, generate seating plans automatically, and export them for distribution.  
Students can log in with their details to check their allotted seat.

---

## 🚀 Features
- Admin login for secure access.
- Upload student details via CSV.
- Auto-generate seating arrangements based on available rooms.
- Store all data in **MongoDB** for persistence.
- Students can check their room and seat by entering their registration number.
- Download seating arrangement as a **PDF**.
- Responsive frontend (HTML, CSS, JavaScript).
- Backend powered by **Python Flask** + **MongoDB**.

---

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Python (Flask)  
- **Database**: MongoDB  

---

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/smartexam-planner.git
cd smartexam-planner
2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate   # for Linux/Mac
venv\Scripts\activate      # for Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup MongoDB

5️⃣ Run the Application
python app.py

6️⃣ Access in Browser
http://127.0.0.1:5000

📂 Project Flow

Admin logs in → Uploads student details (CSV).

System stores data → MongoDB.

Admin generates seating plan → Auto-allocation algorithm assigns seats.

Seating arrangement displayed → Admin can export PDF.

Students login → View their seat/room number.

📑 Usage

Admin Panel → Login → Upload student list → Generate seating → Download PDF.

Student Portal → Enter registration number → Check allotted seat.
