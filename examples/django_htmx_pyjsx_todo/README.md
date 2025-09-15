# Todo Webapp

A simple todo webapp built with Django, HTMX, and PyJSX.

## Features

- Create new todos
- Display todos dynamically using HTMX

## Installation
0. Install uv
  ```
  sudo snap install astro-uv
  ```
	
1. Install dependencies using uv:
   ```
   uv sync
   ```

2. Run migrations:
   ```
   uv run python manage.py migrate
   ```

3. Start the development server:
   ```
   uv run python manage.py runserver
   ```

## Usage

Visit `http://localhost:8000` to access the todo app.