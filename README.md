# Track It All

This is a simple bug tracker website built using Python Flask framework.

## Features

- User authentication (registration, login, logout)
- Create, view, update, and delete bug reports
- Assign bugs to specific users
- Filter and search functionality
- Admin panel for managing users and bugs

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/lordgrim18/Track-It-All.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Set up environment variables. Rename `.env.example` to `.env` and fill in the necessary configurations.

4. Run the application:

    ```bash
    python main.py
    ```

6. Visit `http://localhost:5000` in your web browser to access the bug tracker website.

## Usage

- Register a new account or log in if you already have an account.
- Once logged in, you can create new bug reports, view existing ones, update or delete them.
- Admin users have additional privileges to manage users and bugs.

## Future updates

- Feature for tracking tasks as well
- Creating and managing groups
