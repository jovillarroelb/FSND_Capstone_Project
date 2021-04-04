import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

# Migrations
from flask_migrate import Migrate

# Import database and authentication files:
from database.models import setup_db, Manager, Project, Category
from auth.auth import AuthError, requires_auth

"""
PAGINATION:
Constant: Number of elements showed in the page.
This is intended for pagination.
"""
DATA_PER_PAGE = 10

"""
Pagination Function:

It determines how many items (managers/projects) will be shown per page, 
controlled by the 'DATA_PER_PAGE' variable (default = 10). It follows the 
guidelines from API course's example: "Bookshelf App".
"""


def paginate_data(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * DATA_PER_PAGE
    end = start + DATA_PER_PAGE

    items = [question.format() for question in selection]
    page_items = items[start:end]

    return page_items


"""
Main App:

Configuration and definition for the main App, API endpoints and Error
Handlers.

Task needed to be convered:

    1.  Set up CORS. Allow '*' for origins.
    2.  Use the after_request decorator to set Access-Control-Allow
    3.  Create an endpoint to handle GET requests for all available categories.
    4.  Create an endpoint to handle GET requests for questions, including
        pagination (every 10 questions).
    5.  Create an endpoint to DELETE question using a question ID.
    6.  Create an endpoint to POST a new question, which will require the
        question and answer text, category, and difficulty score.
    7.  Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term is a substring
        of the question.
    8.  Create a GET endpoint to get questions based on category.
    9.  Create a POST endpoint to get questions to play the quiz.
    10. Create error handlers for all expected errors including 404 and 422.
"""


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    get_app = setup_db(app)
    db = SQLAlchemy(get_app)

    '''
    Migration: This is intended to run the migrations the first time!
    '''
    migrate = Migrate(app, db)

    # 1.- Set up CORS allowing all the origins
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 2.- Access control
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type,Authorization,true",
        )
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET,POST,PATCH,DELETE",
        )
        return response

    """
    A.- ENDPOINTS:

    """
    # 3.- GET ALL CATEGORIES
    @app.route("/categories")
    def get_categories():
        """
        Description: Query all the categories existing in the DB and add it to
        a dictionary that will be presented in JSON format if success.
        Otherwise, throw an 404 error.
        """
        # Collect (query) all categories in DB and dictionary initialization.
        categories = Category.query.all()
        category_dictionary = {}

        # Make Key:Value using 'Id': 'Type'
        # (1:Science, 2:Art, 3:Geography, 4:History, 5:Entertainment, 6:Sports)
        for c in categories:
            category_dictionary[c.id] = c.type

        # When dictionary is empty >>>> Throws 404 error #
        # if 'category_dictionary' in not empty
        if len(category_dictionary) != 0:
            # Show the data from the dictionary in JSON format.
            return (
                jsonify(
                    {
                        "success": True,
                        "categories": category_dictionary,
                        "categories_total": len(category_dictionary),
                    }
                ),
                200,
            )
        # Dictionary is empty
        else:
            abort(404)

    # 4.- GET ALL MANAGERS
    @app.route("/managers")
    def get_managers():
        """
        Description: Query all the managers existing in the DB, add it to
        a dictionary and use pagination to present results in JSON format
        if success. Otherwise, throw an 404 error.
        """
        # Collect (query) all managers in DB and dictionary initialization.
        managers = Manager.query.all()
        page_managers = paginate_data(request, managers)

        try:
            if page_managers:
                return (
                    jsonify(
                        {
                            "success": True,
                            "managers": page_managers,
                            "total_managers": len(managers),
                        }
                    ),
                    200,
                )
            # DB is empty
            else:
                abort(404)

        # Another error > Unprocessable
        except BaseException:
            abort(422)

    # 5.- GET ALL PROJECTS
    @app.route("/projects")
    def get_projects():
        """
        Description: Query all the projects existing in the DB, add it to
        a dictionary and use pagination to present results in JSON format
        if success. Otherwise, throw an 404 error.
        """
        # Collect (query) all projects in DB and dictionary initialization.
        projects = Project.query.all()
        page_projects = paginate_data(request, projects)

        try:
            if page_projects:
                return (
                    jsonify(
                        {
                            "success": True,
                            "projects": page_projects,
                            "total_projects": len(projects),
                        }
                    ),
                    200,
                )
            # DB is empty
            else:
                abort(404)

        # Another error > Unprocessable
        except BaseException:
            abort(422)

    # 6.- DELETE PROJECT
    @app.route("/projects/<int:project_id>", methods=["DELETE"])
    @requires_auth("delete:project")
    def delete_project(project_id):
        """
        Description: If the user selects the trash can in the app, get the
        projects's ID and delete it from the DB, delivering a success message
        indicating which project ID was deleted.
        """
        try:
            # Select the project by ID
            project = Project.query.get_or_404(project_id)
            if project:
                project.delete()
                return (
                    jsonify(
                        {
                            "success": True,
                            "id": project_id,
                            "message": "Project deleted successfully!",
                        }
                    ),
                    200,
                )
            else:
                abort(404)
        except BaseException:
            abort(422)

    # 7.- PATCH PROJECT
    @app.route("/projects/<int:project_id>", methods=["PATCH"])
    @requires_auth("update:project_info")
    def patch_project(project_id):
        """
        Description: Modify the projects information according to the
        projects's ID, delivering a successful message indicating which
        project ID was modified.
        """
        # Get the data from the UI
        user_data = request.get_json()
        user_name = user_data.get("name")
        user_manager_id = user_data.get("manager_id")
        user_country = user_data.get("country")
        user_city = user_data.get("city")
        user_address = user_data.get("address")
        user_category = user_data.get("category")
        user_description = user_data.get("description")

        try:
            # Select the project by ID
            project = Project.query.get_or_404(project_id)
            if project:
                project.update()
                return (
                    jsonify(
                        {
                            "success": True,
                            "id": project_id,
                            "message": "Project deleted successfully!",
                        }
                    ),
                    200,
                )
            else:
                abort(404)
        except BaseException:
            abort(422)

    # 8.- ADD NEW PROJECT
    @app.route("/projects", methods=["POST"])
    @requires_auth("create:project")
    def create_project():
        """
        Description: Create a new project from the UI, indicating 'name',
        'manager_id', 'country', 'city', 'address', 'category' and
        'description'. All the data needs to be in filled in order to create
        a new question.
        """
        # Get the data from the UI
        user_data = request.get_json()
        user_name = user_data.get("name")
        user_manager_id = user_data.get("manager_id")
        user_country = user_data.get("country")
        user_city = user_data.get("city")
        user_address = user_data.get("address")
        user_category = user_data.get("category")
        user_description = user_data.get("description")

        # All the information needs to be provided
        if (
            user_name
            and user_manager_id
            and user_country
            and user_city
            and user_address
            and user_category
            and user_description
        ):

            try:
                new_project = Project(
                    name=user_name,
                    manager_id=user_manager_id,
                    country=user_country,
                    city=user_city,
                    address=user_address,
                    category=user_category,
                    description=user_description,
                )
                new_project.insert()

                # Return success in JSON format
                return (
                    jsonify(
                        {
                            "success": True,
                            "message": "Project successfully added to the database!",
                            "project": new_project.format(),
                        }
                    ),
                    200,
                )

            except BaseException:
                abort(400)
        # Some info is missing
        else:
            abort(400)

    """
    B.- ERROR HANDLERS:

    """
    # 8.- ERROR HANDLERS DEFINITION

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 400,
                    "message": "bad request",
                }
            ),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 404,
                    "message": "resource not found",
                }
            ),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "unprocessable",
                }
            ),
            422,
        )

    @app.errorhandler(AuthError)
    def auth_error(error):
        return (
            jsonify({"success": False, "error": error.status_code, "message": error.error["description"]}),
            error.status_code,
        )

    return app
