A simple **Django & Django REST Framework (DRF)** based web application that allows users to shorten long URLs and retrieve the original URLs using a generated short code.

## **Features**
- **Shorten a long URL**: Generate a short, unique URL for any given long URL.
- **Expand a shortened URL**: Retrieve the original URL using its short code.
- **Redirect to the original URL**: Visit the shortened URL and get redirected to the original destination.

## Local Setup Guide
Follow these steps to set up the URL Shortener project locally using Poetry.

### Create a `.env` File

In the project root, create a file named `.env` with the following content:

```
BASE_URL=http://localhost:8000
SECRET_KEY=your_production_secret_key
```

Now, choose either of the following options:

### Docker Setup (Recommended)

#### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your system.

#### Build the docker image

`docker build -t url-shortener .`

#### Run the docker container

`docker run --rm --env-file .env -p 8000:8000 --name url_shortener_dev url-shortener`


### Baremetal Setup

#### Prerequisites
Ensure you have the following installed on your system:

- Python 3.10+ (Check with python --version)
- Poetry (Check with poetry --version, install via official guide)

#### Clone the Repository and Install Dependencies
After cloning the repository, do:

`poetry install`

Poetry manages dependencies and virtual environments automatically.

This will:

- Create a virtual environment if needed.
- Install all dependencies defined in pyproject.toml.

#### Apply Migrations (Initialize the Database)
Run Django migrations to set up the database schema:

`poetry run python manage.py migrate`


#### Run the Development Server
Start the Django development server:

`poetry run python manage.py runserver`

By default, the app will be available at http://127.0.0.1:8000/.

## Access the application

Once the container or Django local dev server is running, you can now interact with your API endpoints (see API Endpoints section).

## Running Tests
To ensure everything works correctly, run the test suite:

With Docker:

`docker exec -it url_shortener_dev poetry run python manage.py test`

With Baremetal:

`poetry run python manage.py test`

You can also run specific tests:

`python manage.py test tests.shortener.test_views`

## API Endpoints
Once running, you can interact with the API using tools like Postman or cURL.

Shorten a URL

```
curl -X POST "http://127.0.0.1:8000/api/shorten/" \
     -H "Content-Type: application/json" \
     -d '{"url": "http://example.com/very-very/long/url"}'

# Response:
{"short_url":"http://localhost:8000/shrt/6f3gbd"}
```

Expand a Shortened URL
```
curl -X GET "http://127.0.0.1:8000/api/expand/6f3gbd/" \
     -H "Content-Type: application/json"

# Response:
{"original_url":"http://example.com/very-very/long/url"}
```

Redirect to Original URL
```
curl -X GET -i "http://127.0.0.1:8000/api/shrt/6f3gbd/"

# Response (as redirect to the original URL):
HTTP/1.1 302 Found
Date: Thu, 20 Feb 2025 10:18:06 GMT
Server: WSGIServer/0.2 CPython/3.10.7
Content-Type: text/html; charset=utf-8
Location: http://example.com/very-very/long/url
Allow: GET, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 0
Vary: Cookie
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
```

## Additional Notes

The app uses SQLite by default (stored in db.sqlite3).

If needed, create a superuser for the Django admin:

`poetry run python manage.py createsuperuser`

To stop running container, do `docker ps` and  then `docker stop url_shortener_dev`

To stop the development server, press CTRL + C.

You're all set! 🚀