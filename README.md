# BackendAI Project

This is a Django project that supports both HTTP and WebSocket protocols using Django Channels.

## Project Structure
backendai/
│
├── api/
│ ├── migrations/
│ │ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── consumers.py
│ ├── models.py
│ ├── routing.py
│ ├── tests.py
│ ├── urls.py
│ ├── views.py
│
├── backendai/
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│
├── manage.py


## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/backendai.git
    cd backendai
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**

    ```bash
    daphne -p 8000 backendai.asgi:application
    ```

## Features

- Supports HTTP and WebSocket protocols.
- Configured to use Django Channels for WebSocket support.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
