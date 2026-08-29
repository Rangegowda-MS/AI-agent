# ✈️ AI Travel Agent

An intelligent **AI-powered travel planning application** designed to generate personalized travel itineraries based on user preferences such as destination, budget, number of travelers, trip duration, interests, and hotel preferences.

The project combines **Python, Django, Artificial Intelligence, and modern web technologies** to provide users with a smart and interactive travel-planning experience.

---

## 🚀 Features

* 🤖 AI-powered trip planning
* 🗺️ Personalized travel itineraries
* 📅 Day-by-day travel plans
* 💰 Budget-based recommendations
* 🏨 Hotel preference selection
* 👥 Multi-traveler support
* 🎯 Interest-based recommendations
* 🍽️ Food and local experience suggestions
* 🏖️ Destination recommendations
* 💵 Estimated trip costs
* 📱 Responsive user interface
* ⚡ Django REST API integration
* 🗄️ Database storage for generated trips
* 🔐 Secure environment-variable configuration

---

## 🧠 How It Works

The user provides information such as:

* Destination
* Number of travel days
* Number of travelers
* Budget
* Hotel preference
* Travel interests

The application processes these preferences and sends them to the AI service.

The AI then generates a personalized itinerary containing recommended activities, attractions, experiences, and estimated travel costs.

---

## 🛠️ Technologies Used

### Backend

* Python
* Django
* Django REST Framework

### Artificial Intelligence

* OpenAI API
* Generative AI
* Prompt Engineering

### Frontend

* HTML5
* CSS3
* JavaScript
* Responsive Web Design

### Database

* SQLite

### Development Tools

* Git
* GitHub
* Visual Studio Code
* Python Virtual Environment
* REST APIs

---

## 📂 Project Structure

```text
AI_Travel_Agent_Full_Project/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── travel/
│   ├── migrations/
│   ├── services/
│   │   └── ai_service.py
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── api_urls.py
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Rangegowda-MS/AI-agent.git
```

### 2. Open the Project

```bash
cd AI-agent
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Do **not** upload your `.env` file or API keys to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
db.sqlite3
```

---

## 🗄️ Database Setup

Run Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Optionally create an administrator account:

```bash
python manage.py createsuperuser
```

---

## ▶️ Run the Application

Start the Django development server:

```bash
python manage.py runserver
```

Then open the local development address displayed by Django in your browser.

---

## 🤖 AI Travel Planning

The AI planner can use information such as:

```text
Destination: Goa
Duration: 5 Days
Travelers: 2
Budget: ₹30,000
Hotel Style: Comfort
Interests:
- Beaches
- Food
- Adventure
- Photography
```

The system uses these preferences to generate a personalized day-by-day travel plan.

---

## 🔮 Future Enhancements

Planned improvements include:

* Real-time flight search
* Real-time hotel availability
* Interactive maps
* Weather integration
* AI chatbot travel assistant
* Location-aware recommendations
* Automatic budget optimization
* Multi-city itinerary generation
* Travel history dashboard
* User authentication
* Saved and shareable itineraries
* PDF itinerary export
* Online booking integrations

---

## 🎯 Project Purpose

This project demonstrates practical experience with:

* Artificial Intelligence
* Generative AI
* Python
* Django
* REST APIs
* Prompt Engineering
* Database Management
* Frontend Development
* Full-Stack Web Development

It was developed as a portfolio project to demonstrate the integration of **AI with Python-based web application development**.

---

## 👨‍💻 Developer

**Rangegowda M S**

AI & Python Developer | Machine Learning Enthusiast | Django Developer

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
