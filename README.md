BArtO - A Platform Connecting Artists
BArtO is a Django-based project aimed at connecting artists across various disciplines (music, writing, acting, etc.). The platform allows users to upload their work, interact with other artists, and engage in events and collaborations. Artists can share their creations, get feedback, and invite others to events.

Features
Artist Profiles: Artists can create profiles and upload works in different categories such as music, writing, and acting.
Event Management: Organizers can create events, invite artists, and manage participants. Artists can RSVP for events and participate in discussions.
Followers & Connections: Artists can follow each other, form connections, and get notifications about activities and invitations.
Comments & Feedback: Users can comment on works and events, with voting and moderation features.
Notifications: The platform supports notifications for new followers, event invitations, and other important actions.
Calendar View: Upcoming events are displayed in a calendar format for easy access and planning.
Installation
To run BArtO locally, you need to have Python, Django, and a few other dependencies installed.

Prerequisites
Python 3.x
pip (Python package installer)
Setting Up the Environment
Clone the repository:

bash
Копиране на код
git clone https://github.com/your-username/barto.git
cd barto
Install dependencies:

Create a virtual environment and install the necessary packages.

bash
Копиране на код
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
Set up the database:

BArtO uses SQLite by default. Run migrations to set up the database schema.

bash
Копиране на код
python manage.py migrate
Create a superuser (optional for admin access):

bash
Копиране на код
python manage.py createsuperuser
Run the development server:

bash
Копиране на код
python manage.py runserver
The application should now be available at http://127.0.0.1:8000.

Usage
Create an Account
You can register as an artist and set up your profile.
Upload works (e.g., music, text, or videos) and categorize them.
Create and Join Events
Organizers can create events and invite other artists.
You can RSVP for events and participate in event discussions.
Users can follow others, receive notifications, and interact with content.
Notifications
Get notified when you have new followers, event invitations, or comments on your work.
Structure
The project is organized into different apps:

Accounts: Manages user registration, profiles, and authentication.
Works: Handles the creation and display of works (e.g., music, text, videos).
Events: Manages event creation, participant invitations, and RSVPs.
Connections: Handles the following system, allowing users to connect with each other.
Notifications: Sends notifications to users about relevant activities.
Technologies Used
Django: A powerful web framework for Python.
SQLite: A lightweight database used for development.
HTML/CSS: Basic frontend for displaying content and forms.
Bootstrap: For responsive design and styling.
Contributing
Contributions to BArtO are welcome! If you have ideas, fixes, or improvements, feel free to fork the repository and submit a pull request. Please follow the code style and ensure tests are included for new features.

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new pull request.
License
This project is licensed under the MIT License - see the LICENSE file for details.
