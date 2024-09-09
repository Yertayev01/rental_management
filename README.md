# Rental Management System

A Django-based REST API for managing a rental business, allowing users to manage rental orders, products, and obtain useful statistics.

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd rental_management

2. **Build and start the Docker containers**
    docker-compose up --build

3. **Run database migrations and create a superuser**
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate
    docker-compose run web python manage.py createsuperuser

4. **Access the application**
    http://localhost:8000 - app
    http://localhost:8000/admin - admin panel

5. **Swagger Documentation. To view the interactive API documentation, navigate to**
    http://localhost:8000/swagger/

docker-compose exec web python manage.py makemigrations rentals
docker-compose exec web python manage.py migrate
docker-compose down
docker-compose up --build