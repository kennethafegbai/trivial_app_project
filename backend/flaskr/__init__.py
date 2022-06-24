import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def pagination(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

   
    CORS(app, resources={r"*": {"origins": "*"}})


    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,PATCH,POST,DELETE,OPTIONS"
        )
        return response

   
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        if categories is None:
            abort(404)
        else:
            #formatted_categories = [category.format() for category in categories]
            formatted_categories = {category.id:category.type for category in categories}

            return jsonify(
                {
                'categories':formatted_categories
                }
            )


    @app.route('/questions', methods=['GET'])
    def get_questions():

        questions = Question.query.order_by(Question.id).all()

        current_questions = pagination(request, questions) #pagination funtion to return 10 books

        if len(current_questions) < 1:
            abort(404)
        else:
            categories = Category.query.all()

            #formatted_categories = [category.format() for category in categories]
            formatted_categories = {category.id:category.type for category in categories}


            return jsonify(
                {
                    'success':True,
                    'questions':current_questions,
                    'total_questions':len(questions),
                    'current_category':None,
                    'categories': formatted_categories
                }
            )


    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        delete_question = Question.query.get(question_id)

        if delete_question is None:    
            abort(404)
        else:    
            try:
                delete_question.delete()
                return jsonify(
                    {
                        'success':True,
                        'deleted': delete_question.id,
                        'message': 'delete successful'
                    }
                )

            except Exception:
                abort(500)


    @app.route('/questions', methods=['POST'])
    def submit_question():
        searchTerm = request.get_json().get('searchTerm', None)
        if searchTerm is not None:
            searched_questions = Question.query.filter(Question.question.ilike(f"%{searchTerm}%"))
            formatted_questions = [question.format() for question in searched_questions]

            if len(formatted_questions) < 1:
                abort(404)

            return jsonify(
                {
                    'questions':formatted_questions,
                    'totalQuestions':len(Question.query.all()),
                    'currentCategory':None
                    }
            )
        else:
            try:
                question = request.get_json().get('question')
                answer = request.get_json().get('answer')
                category = request.get_json().get('category')
                difficulty = request.get_json().get('difficulty')
                new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
                new_question.insert()
                questions = Question.query.all()

                formatted_questions = [question.format() for question in questions]
                return jsonify(
                        {
                            'success':True,
                            'added':new_question.id
                        }
                )
            except Exception:
                abort(400)


   
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def questions_by_category(category_id):
        try:
            questions_by_category = Question.query.filter_by(category=category_id).all()
            formatted_questions = [question.format() for question in questions_by_category]
            return jsonify(
                {
                    'success':True,
                    'questions':formatted_questions,
                    'totalQuestions':len(Question.query.all()),
                    'currentCategory':None
                }
            )
        except Exception:
            abort(404)

   
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        #pass
        data_from_frontend = request.get_json()
        try:
            previous_questions = data_from_frontend['previous_questions']
            quiz_category = data_from_frontend['quiz_category']
        except Exception:
            abort(400)
        if quiz_category:
            random_questions = Question.query.filter(Question.category == quiz_category, Question.id.not_in(previous_questions)).all()
        else:
            random_questions = Question.query.filter(Question.id.not_in(previous_questions)).all()

        if random_questions:
            random_question = random.choice(random_questions).format()
        else:
            random_question = None
        
        return jsonify(
            {
                "question":random_question
            }
        )



   
    @app.errorhandler(404)
    def not_found(error):
        return (jsonify(
            {
                "success":False,
                "message":"Resource not found",
                "error":404,
            }
        ), 404)

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify(
            {
                "success":False,
                "message":"Bad request",
                "error":400,
            }
        ), 400)

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify(
            {
                "success":False,
                "message":"Not processable",
                "error":422,
            }
        ), 422)


    @app.errorhandler(405)
    def method_not_allowed(error):
        return (jsonify(
            {
                "success":False,
                "message":"Method not allowed",
                "error":405,
            }
        ), 405)

    @app.errorhandler(500)
    def server_error(error):
        return (jsonify(
            {
                "success":False,
                "message":"Server error",
                "error":500,
            }
        ), 500)




    return app

