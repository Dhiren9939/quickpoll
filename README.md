# QuickPoll - Anonymous Voting App

## Introduction

QuickPoll is a simple web app for creating polls and voting anonymously. Built with Django, it lets users create polls, vote, and view results with minimal fuss.

## Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Dhiren9939/quickpoll.git
   cd quickpoll
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**

   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**

   ```bash
   python manage.py runserver
   ```

6. **Access the app**
   Open `http://localhost:8000` in your browser

The app should now be running locally. For production deployment, additional steps would be needed.
