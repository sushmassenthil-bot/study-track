StudyTrack

Unified Full-Stack Study Management Platform

StudyTrack is a full-stack student management system built with FastAPI, SQLAlchemy, SQLite, HTML, CSS and JavaScript.

The application allows users to manage students and courses through a web dashboard, perform student sorting and searching using manually implemented algorithms, generate student reports, and use an AI-assisted study helper.

The entire application is integrated into one project and communicates through the FastAPI backend.


Features

1. Student Management

StudyTrack provides complete CRUD operations for student records.

Users can:

- View all students
- Add a new student
- View an individual student
- Update student information
- Delete a student
- Filter students by minimum age

Each student contains:

- ID
- Name
- Email
- Age

2. Course Management

Users can manage course enrollments through the dashboard.

Users can:

- View all courses
- Add a course
- View an individual course
- Update course information
- Delete a course

Each course contains:

- ID
- Course name
- Credits
- Student ID

Course records are connected to students through a foreign-key relationship.

3. Search and Algorithms

StudyTrack includes a dedicated Search & Algorithms section.

It contains:

- Insertion Sort
- Binary Search
- Student roster reporting

The sorting algorithm is implemented manually instead of using Python's built-in sorting function.

Binary Search is performed on a name-sorted student list.

4. AI Study Advisor

The AI Study Advisor provides study assistance through the integrated AI assistant module.

It can:

- Summarize study notes
- Identify important points
- Estimate difficulty
- Search study notes using semantic similarity

The application includes an offline mock mode so the AI features can work without requiring an external API key or network connection.

Technology Stack

Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

Frontend

- HTML5
- CSS3
- JavaScript

Algorithms

- Insertion Sort
- Binary Search
- Cosine Similarity

Project Structure

text
StudyTrack/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── algorithms.py
│   ├── ai_service.py
│   ├── seed_data.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── .env.example
├── .gitignore
└── README.md

Quick Feature Verification

Backend:
uvicorn backend.main:app --reload

Frontend:
serve frontend on port 5500

After starting the application:

1. Open http://localhost:8000/.
2. Confirm the seeded roster displays 8 students.
3. Edit a student's age and click Save Age.
4. Add a new student using the student form.
5. Delete a student using the Delete button.
6. Open Search & Algorithms to test sorting, searching, and the student report.
7. Open AI Study Advisor to test note summarization and semantic note search.
8. Confirm the dashboard shows API Connected.