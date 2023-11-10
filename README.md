# Stock Startup

## Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/stockStartup.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd path/to/dir/stockStartup
    ```

3. **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run model migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run management commands to populate the database with dummy data:**
    ```bash
    python manage.py create_users
    python manage.py create_stocks
    python manage.py create_trades
    ```

7. **Start the cron job:**
    - On Windows, run `cron.bat`
    - On Linux, run `cron.sh`

Now, your Django project should be set up and ready to go. You can access the Django admin panel at `http://localhost:8000/admin/` and start working with your application.
