# 🎬 Movie Database Project

A Python-based movie database application that allows users to manage a personal movie collection using a command-line interface.  
Movie data is fetched automatically from the **OMDb API**, stored in a **SQLite database**, and can be exported as a simple **HTML website**.

---

## ✨ Features

- Add movies by title (movie data is fetched from the OMDb API)
- Store movies persistently using SQLite
- List all movies with year and IMDb rating
- Update movie ratings
- Delete movies
- Search movies by name
- Display statistics (average, median, best & worst rated movies)
- Pick a random movie
- Generate an HTML website displaying all movies with posters

---

## 🛠️ Technologies Used

- **Python 3**
- **SQLite** (via SQLAlchemy)
- **OMDb API** (movie data & posters)
- **HTML/CSS** (for generated website)
- `requests` (API communication)

---

## 🚀 Setup & Installation

Follow these steps to run the project locally:

### 1. Clone the repository

bash
git clone https://github.com/your-username/movie-database-project.git
cd movie-database-project

### 2. Install dependencies

pip install -r requirements.txt

### 3. 🔑 API Key Setup

This project uses the OMDb API.

You need to create a free API key at:
https://www.omdbapi.com/

Then add your API key in the source code of "movie_storage_sql.py:
```python
API_KEY = "your_api_key_here"
