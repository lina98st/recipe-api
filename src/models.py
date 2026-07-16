import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    created_at = db.Column(db.Date)
    password_hash = db.Column(db.Text)

    profile = db.relationship(
        "UserProfile",
        backref="user",
        uselist=False
    )

    def __init__(self, email: str, created_at: datetime.date, password_hash: str):
        self.email = email
        self.created_at = created_at
        self.password_hash = password_hash

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at
        }




class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    display_name = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True
    )
    avatar_url = db.Column(db.Text, nullable=False)

    def __init__(self, display_name: str, bio, user_id: int, avatar_url: str):
        self.display_name = display_name
        self.bio = bio
        self.user_id = user_id
        self.avatar_url = avatar_url

    def serialize(self):
        return {
            'id': self.id,
            'display_name': self.display_name,
            'bio': self.bio,
            'user_id': self.user_id,
            'avatar_url': self.avatar_url
        }


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

recipes_ingredients_table = db.Table(
    "recipes_ingredients",
    db.Column(
        "recipe_id",
        db.Integer,
        db.ForeignKey("recipes.id"),
        primary_key=True
    ),
    db.Column(
        "ingredient_id",
        db.Integer,
        db.ForeignKey("ingredients.id"),
        primary_key=True
    )
)

class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    instructions = db.Column(db.Text)
    cooking_time = db.Column(db.Integer)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id")
    )
    category = db.relationship(
        "Category",
        backref="recipes",
    )
    ingredients = db.relationship(
        "Ingredient",
        secondary=recipes_ingredients_table,
        backref="recipes"
    )
    def __init__(self, title: str, instructions: str, cooking_time: int, category_id: int):
        self.title = title
        self.instructions = instructions
        self.cooking_time = cooking_time
        self.category_id = category_id

    def serialize(self):
        return {
            'id': self.id,
            'instructions': self.instructions,
            'cooking_time': self.cooking_time,
            'title': self.title,
            'category_id': self.category_id
        }



class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Rating(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer)
    created_at = db.Column(db.Date)
    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.id")
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )
    user = db.relationship(
        "User",
        backref="ratings"
    )
    recipe = db.relationship(
        "Recipe",
        backref="ratings"
    )

    def __init__(self, score: int, created_at: datetime.date, recipe_id: int, user_id: int):
        self.score = score
        self.created_at = created_at
        self.recipe_id = recipe_id
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'score': self.score,
            'created_at': self.created_at,
            'recipe_id': self.recipe_id,
            'user_id': self.user_id
        }


