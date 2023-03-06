## Local config
The easiest way to start project locally is to run docker-compose.

1. Clone this repo.
2. Change directory to project folder.
3. Run `docker-compose up -d --build`
4. Create superuser:
   - `docker-compose exec web python3 manage.py createsuperuser`
5. Type admin username, email and password.
6. Now you can visit: `127.0.0.1:8000/admin` or `localhost:8000/admin` and log in to admin panel.


### Available paths:
- http://127.0.0.1:8000/admin/
- http://127.0.0.1:8000/api-auth/
- http://127.0.0.1:8000/api/v1/images
- http://127.0.0.1:8000/api/v1/expiring-links
- http://127.0.0.1:8000/api/v1/schema/
- http://127.0.0.1:8000/api/v1/schema/redoc/
- http://127.0.0.1:8000/api/v1/schema/swagger-ui/ 
