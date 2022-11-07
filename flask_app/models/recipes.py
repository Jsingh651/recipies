from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import users
class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cook_time = data['cook_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None


# query select * from recipies Left join users on recipee.user_id = user.id
# result return 
# eachrow.user.append
# getone, getall, create, update

    @classmethod
    def get_all_recipes(cls):
        query = 'SELECT * FROM recipes'
        results = connectToMySQL('recipesof_schema').query_db(query)
        recipes = []
        for i in results:
            recipes.append(cls(i))
        return recipes

    @classmethod
    def get_one_recipes(cls,data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s ;'
        results = connectToMySQL('recipesof_schema').query_db(query,data)
        return cls(results[0])

    @classmethod
    def create_recipes(cls,data):
        query = '''
            INSERT INTO recipes (name, description, instructions,cook_time, user_id) 
            VALUES (%(name)s,%(description)s,%(instructions)s,%(cook_time)s,%(user_id)s); 
                '''
        return connectToMySQL('recipesof_schema').query_db(query,data)

    @classmethod
    def update_recipes(cls,data):
        query = """
                UPDATE recipes SET name = %(name)s, description = %(description)s,
                instructions = %(instructions)s
                WHERE id = %(recipie_id)s;
                """

        print(query)
        return connectToMySQL('recipesof_schema').query_db(query,data)

    @classmethod
    def delete (cls,data):
        query = 'DELETE FROM recipes WHERE id = %(id)s'
        return connectToMySQL('recipesof_schema').query_db(query,data)

    @staticmethod
    def validate_recipes(recipe):
        is_valid = True # we assume this is true
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must have 3 chracters.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash('Instructions must be at least 3 characters')
            is_valid = False
        return is_valid


    @classmethod
    def get_user_with_recipe(cls):
        query = """
                SELECT * FROM recipes
                LEFT JOIN users on recipes.user_id = users.id;
                """
        results = connectToMySQL('recipesof_schema').query_db( query)
        # user = cls(results[0])
        recipes = []
        for data in results:
            single_recipe = cls(data)
            user_data = {
                'id': data['users.id'],
                'first_name':data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'password':data['password'],
                'created_at':data['users.created_at'],
                'updated_at': data['users.updated_at'],
            }
            single_recipe.user = users.User(user_data)
            recipes.append(single_recipe)
        return recipes