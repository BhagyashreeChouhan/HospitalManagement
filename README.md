# Hospital Management Project

This is a hospital management web application built with Python, Django and Django REST Framework.

## Features

- User authentication (signup, login) with roles (Admin, Doctor)

- Manage patients: create, view, list patients (doctors see only their own)

- Manage medical records: add symptoms, diagnosis, and treatment linked to patients

- Role-based permissions: doctors can only access their own patients’ data, admins have full access
  
- Token-based authentication for secure API access

## API Endpoints

| Method | URL                            | Description                                      |
|--------|--------------------------------|--------------------------------------------------|
| POST   | /api/register/                 | Register a new user (doctor or admin)            |
| POST   | /api/login/                    | Obtain authentication token                     |
| GET    | /api/patients/                 | List patients (doctor sees own only; admin sees all) |
| POST   | /api/patients/                 | Create a new patient (assigned to logged-in doctor) |
| GET    | /api/patients/{id}/records/    | List medical records for a patient (only if owned) |
| POST   | /api/patients/records/add      | Add a medical record to a patient (if owned)     |

**Note:** All endpoints (except `/api/register/` and `/api/login/`) require an `Authorization` header:

## Technologies Used

- Python

- Django & Django REST Framework

- PostgreSQL (database)

## How to Run Locally

1. Clone the repository:
git clone https://github.com/BhagyashreeChouhan/HospitalManagement

2. Navigate to the project directory:
cd HospitalManagement

3. Create and activate a virtual environment:
python -m venv venv

 - On Windows: venv\Scripts\activate

 - On macOS/Linux: source venv/bin/activate

4. Install dependencies:
pip install -r requirements.txt

5. Apply migrations:
python manage.py migrate

6. Run the development server:
python manage.py runserver

7. Open your browser and go to http://127.0.0.1:8000/

## Live Demo

You can explore the live version of this hospital management application here:
https://hospitalmanagement-1rw4.onrender.com/

Please note the app is hosted on Render’s free tier, so it might take a few moments to load initially.
