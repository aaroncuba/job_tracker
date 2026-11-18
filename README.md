# Job Application Tracker

A web application built with Python (Flask), MySQL, and HTML/CSS to keep track of companies, job postings, applications, and contacts. It also includes a Job Match page that compares your skills against job requirements and ranks jobs by match percentage.

## Features
- Dashboard with live counts for companies, jobs, applications, and contacts
- Full CRUD (create, read, update, delete) for all four tables with form validation and delete confirmations
- Job Match tool that takes comma-separated skills and shows match percentages along with matched and missing skills
- MySQL JSON columns for storing job skill requirements and application interview notes

## Tech Stack
- Python 3 / Flask
- MySQL 8.0 (`mysql-connector-python`)
- HTML / CSS (Jinja2 templates)

## Project Files
- `app.py` - Flask routes and Job Match logic
- `database.py` - MySQL connection helper
- `schema.sql` - Creates the `job_tracker` database and tables
- `requirements.txt` - Python dependencies
- `AI_USAGE.md` - AI usage documentation
- `static/style.css` - Page styling
- `templates/` - HTML templates (`base.html`, `dashboard.html`, `companies.html`, `jobs.html`, `applications.html`, `contacts.html`, `job_match.html`)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone [https://github.com/aaroncuba/job_tracker.git](https://github.com/aaroncuba/job_tracker.git)
cd job_tracker
```

### 2. Create a Virtual Environment and Install Dependencies
Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set Up the MySQL Database
Run `schema.sql` in MySQL Workbench or from the command line:
```bash
mysql -u root -p < schema.sql
```

### 4. Configure Environment Variables
Create a `.env` file in the root folder with your local MySQL credentials:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=job_tracker
```

### 5. Run the Application
```bash
python app.py
```
Open your browser and go to `http://127.0.0.1:5000`.

## Demo Videos
- `demo_app.mkv` - Walkthrough of the Flask server, dashboard, CRUD operations, and Job Match feature
- `demo_database.mkv` - MySQL Workbench verification showing the database tables and saved records
