**Full Stack Hospital Management System:**
Set Up Flask as the Back-End: Flask will handle requests, interact with the database, and serve HTML pages.
Create Front-End HTML Forms: Users will input data via HTML forms for adding patients, generating bills, and viewing patient details.
CSS Styling: Use basic CSS for better styling to make the interface attractive.
Connect Flask with SQLite: Use SQLite to store patient and billing data, which is accessible via Flask routes.

hospital_management/
│
├── app.py                # Flask back-end logic
├── templates/            # HTML files (front-end)
│   ├── index.html        # Home page
│   ├── add_patient.html  # Form to add patient
│   ├── generate_bill.html# Form to generate a bill
│   └── show_patient.html # Show patient details
└── static/               # CSS and images (front-end)
    └── style.css

