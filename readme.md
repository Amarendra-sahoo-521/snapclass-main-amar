# Snap Class

Snap Class is a Streamlit-based classroom management and attendance application that uses AI-assisted face and voice recognition to help students and teachers manage classes more efficiently.

The app supports two user flows:
- Student portal for login, registration, subject enrollment, and attendance tracking
- Teacher portal for authentication, subject creation, class management, and attendance review

## Features

- Student login with face recognition
- Student registration with facial embedding and optional voice enrollment
- Teacher login and registration with password hashing
- Subject creation for teachers
- Student enrollment in courses by subject code / classroom flow
- Attendance logging and class sessions
- Attendance summary reporting for teachers
- Supabase-backed storage for app data

## Tech Stack

- Python
- Streamlit
- Supabase
- NumPy
- Pillow
- OpenCV / image processing workflow (used in the face pipeline)
- Face recognition and voice embedding model pipeline
- bcrypt for password hashing

## Project Structure

```text
.
├── app.py                   # App entry point
├── requirements.txt         # Python dependencies
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml         # Supabase secrets for local development
├── src/
│   ├── components/          # UI dialogs, header/footer, cards, forms
│   ├── database/            # Supabase configuration and data access helpers
│   ├── pipelines/           # Face and voice recognition logic
│   ├── screens/             # Teacher/student/home UI screens
│   └── utils/               # Supporting helpers (if added later)
├── ui/
│   └── base_layout.py       # Shared styling and layout logic
└── README.md                # Project documentation
```

## Prerequisites

- Python 3.10+ recommended
- A Supabase project with a configured database and auth setup
- Camera access for face recognition
- Microphone access for voice enrollment (optional)

## Setup

1. Clone the repository
2. Create a virtual environment if needed:

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your Supabase credentials in `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://your-project-url.supabase.co"
SUPABASE_PUBLISHABLE_KEY = "your-publishable-key"
SUPABASE_SECRET_KEY = "your-secret-key"
SUPABASE_JWKS_URL = "https://your-project-url.supabase.co/auth/v1/.well-known/jwks.json"
```

This app reads the keys from `st.secrets` in `src/database/config.py`.

## Run the App

From the project root:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, typically:

```text
http://localhost:8501
```

## How It Works

### Teacher Flow
- Log in or register a teacher account
- Create one or more subjects
- Start a class session for a subject
- Capture attendance using the face-recognition pipeline
- View attendance records and class summaries

### Student Flow
- Open the student portal
- Log in using face recognition
- If not recognized
- Enroll in courses
- View attendance statistics for each enrolled subject

## Notes

- The app is directly tied to a Supabase-backed database.
- Face recognition and voice processing depend on the model pipeline files and embeddings stored in the project environment.
- Some features require the browser to allow camera access.

## Future Improvements

- Better multi-class attendance analytics
- Role-based permission enhancements
- Cleaner deployment configuration for production
- More robust error handling and onboarding flows

## Contributing

Pull requests and improvements are welcome. For local development, keep the Supabase configuration consistent and test all recognition flows in a real classroom environment before using it in production.
