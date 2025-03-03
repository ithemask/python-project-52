# Task Manager
[![Actions Status](https://github.com/ithemask/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ithemask/python-project-52/actions)
[![Lint with Ruff](https://github.com/ithemask/python-project-52/actions/workflows/lint-with-ruff.yml/badge.svg)](https://github.com/ithemask/python-project-52/actions/workflows/lint-with-ruff.yml)
[![Test with PostgreSQL](https://github.com/ithemask/python-project-52/actions/workflows/test-with-postgres.yml/badge.svg)](https://github.com/ithemask/python-project-52/actions/workflows/test-with-postgres.yml)
[![Test with SQLite](https://github.com/ithemask/python-project-52/actions/workflows/test-with-sqlite.yml/badge.svg)](https://github.com/ithemask/python-project-52/actions/workflows/test-with-sqlite.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/9c6edd5e45c5c1af9d4f/maintainability)](https://codeclimate.com/github/ithemask/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9c6edd5e45c5c1af9d4f/test_coverage)](https://codeclimate.com/github/ithemask/python-project-52/test_coverage)
## _Description_
___Task Manager___ _is a web application for task management built with Django. It allows users to register, create tasks, manage statuses and labels, and filter tasks by various criteria. The application provides a user-friendly interface for organizing and tracking tasks._
## _Key Features_
  + ___User Registration and Authentication:___ _users can register and log in to access their tasks._
  + ___Task Creation and Management:___ _users can create tasks by specifying a name, description, status, executor, and labels._
  + ___Status Management:___ _ability to create, edit, and delete task statuses (e.g., "In Progress", "Completed")._
  + ___Label Management:___ _users can add, edit, and delete labels for tasks (e.g., "Urgent", "Home Tasks")._
  + ___Task Filtering:___ _tasks can be filtered by:_
    + _Executor_
    + _Status_
    + _Label_
    + _Users can only view tasks that they have created._
  + ___Task Details:___ _each task has a dedicated page with detailed information._
  + ___Multilingual Support:___ _the application is available in English and Russian. The language is automatically selected based on the user's browser settings._
## _Online Access_
_The application is available online at: https://task-manager-kxvw.onrender.com_
## _Local installation and Setup_
### _Requirements:_
  + _OS Linux_
  + _Python >= 3.10_
  + _Pip >= 24.0_
  + _PostgreSQL >= 16.0 (optional)_
  1. _Clone the repository:_
      ```
      git clone git@github.com:ithemask/python-project-52.git
      cd python-project-52
      ```
  2. _Create a virtual environment and install dependencies:_
      ```
      python -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt
      ```
  3. _Configure the database and environment variables:_ 
      ```
      # Use SQLite as the database
      export DATABASE_URL=sqlite:///db.sqlite3

      # Use PostgreSQL as the database
      # Replace {username}, {password}, {host}, {port}, and {database_name} with your actual PostgreSQL credentials
      export DATABASE_URL=postgresql://{username}:{password}@{host}:{port}/{database_name}
  
      # Set the Django SECRET_KEY for cryptographic signing and security
      # Replace {secret_key} with a strong, randomly generated key
      export SECRET_KEY={secret_key}
      ```
  4. _Run migrations:_
      ```
      python manage.py migrate
      ```
  5. _Run the server:_
      ```
      python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker
      ```
  6. _Open the app in your browser: go to: http://127.0.0.1:8000_
## _Usage_
  1. ___Registration and Login:___ _register or log in to access the app's features._
  2. ___Creating Tasks:___ _go to the "Tasks" section and click "Create task". Fill in the required fields._
  3. ___Filtering Tasks:___ _use filters on the tasks page to search by executor, status, or label._
  4. ___Viewing Your Tasks:___ _the tasks page displays only tasks where the current user is the author._
  5. ___Viewing Task Details:___ _click on a task to open its detailed information page._
  6. ___Language Selection:___ _the application automatically detects the user's browser language and displays the interface in English or Russian. To switch languages, change your browser's language settings._
## _Acknowledgments_
_Thank you for using Task Manager! If you have suggestions or questions, please create an issue in the repository._
