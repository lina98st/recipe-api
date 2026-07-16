# Recipe API

A RESTful Recipe API built with Python, Flask, SQLAlchemy, and PostgreSQL.

## Description

This project provides a REST API for managing recipes, categories, ingredients, users, user profiles, and ratings.

The application uses SQLAlchemy ORM for database access and PostgreSQL as the database backend. Docker is used to provide a consistent local development environment.

## Technologies

- Python
- Flask
- SQLAlchemy
- Flask Migrate
- PostgreSQL
- Docker
- pgAdmin
- Insomnia

## API Endpoints

| Endpoint            | Method             | Description                               |
| ------------------- | ------------------ | ----------------------------------------- |
| /users              | GET, POST          | List or create users                      |
| /users/<id>         | GET, PATCH, DELETE | Retrieve, update or delete a user         |
| /user_profiles      | GET, POST          | List or create user profiles              |
| /user_profiles/<id> | GET, PATCH, DELETE | Retrieve, update or delete a user profile |
| /recipes            | GET, POST          | List or create recipes                    |
| /recipes/<id>       | GET, PATCH, DELETE | Retrieve, update or delete a recipe       |
| /categories         | GET, POST          | List or create categories                 |
| /categories/<id>    | GET, PATCH, DELETE | Retrieve, update or delete a category     |
| /ingredients        | GET, POST          | List or create ingredients                |
| /ingredients/<id>   | GET, PATCH, DELETE | Retrieve, update or delete an ingredient  |
| /ratings            | GET, POST          | List or create ratings                    |
| /ratings/<id>       | GET, PATCH, DELETE | Retrieve, update or delete a rating       |

## Database

The project contains the following relationships:

- One to One: User → UserProfile
- One to Many: Category → Recipes
- One to Many: User → Ratings
- One to Many: Recipe → Ratings
- Many to Many: Recipes ↔ Ingredients

## Performance

A database index was added to the `category_id` column of the `recipes` table to improve lookup performance when filtering recipes by category.

## Running the Project

```bash
docker compose up --build
docker compose exec flask flask db upgrade
```

The API is available at:

```
http://localhost:3000
```

## Testing

The REST API was tested using Insomnia to verify CRUD operations and API responses.

## Retrospective

### How did the project's design evolve?

The project started as a simple database design. During development, additional entities, relationships, and REST endpoints were added. Finally, the application was containerized with Docker to create a portable development environment.

### ORM or raw SQL?

I chose SQLAlchemy ORM because it provides a cleaner and more maintainable way to interact with the database while reducing the amount of SQL code.

### Future Improvements

- User authentication
- Recipe search and filtering
- Pagination
- Average recipe ratings
- Image uploads
- Cloud deployment (Render or Railway)
