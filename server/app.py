#!/usr/bin/env python3
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_jwt_extended import jwt_required, JWTManager
from auth import auth_bp, bcrypt
from models import db, Customer, Product as ProductModel, Order, OrderItem, Review

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '9d1608035e013ed57370aff38dee'
app.json.compact = False

db.init_app(app)

# Initialize Migrate, JWT, and Bcrypt
migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt.init_app(app)

# Register blueprint
app.register_blueprint(auth_bp)

# Instantiate REST API
api = Api(app)

with app.app_context():
    db.create_all()

@app.route('/')
@jwt_required()
def index():
    return '<h1>Project Server</h1>'
class Products(Resource):
    #@jwt_required
    def get(self):
        products = [product.to_dict() for product in ProductModel.query.all()]
        response = make_response(jsonify(products), 200)
        return response

class ProductByID(Resource):
    #@jwt_required
    def get(self, id):
        product = ProductModel.query.filter_by(id=id).first()
        if product is None:
            return make_response(jsonify({"message": "Product not found"}), 404)
        response_dict = product.to_dict()
        return make_response(jsonify(response_dict), 200)
    
    
    @jwt_required()
    def delete(self, id):
        product = ProductModel.query.filter_by(id=id).first()
        if product is None:
            return make_response(jsonify({"message": "Product not found"}), 404)

        db.session.delete(product)
        db.session.commit()

        return make_response(jsonify({"message": "Product deleted successfully"}), 202)

class Orders(Resource):
    @jwt_required()
    def delete(self, id):
        deleteorder = Order.query.filter_by(id=id).first()
        if deleteorder is None:
            return make_response(jsonify({"message": "Order not found"}), 404)
        db.session.delete(deleteorder)
        db.session.commit()
        return make_response(jsonify({"message": "Product deleted successfully"}), 204)

class Reviews(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        review = Review(
            comment=data.get("comment"),
            date_reviewed=data.get("date_reviewed")
        )
        db.session.add(review)
        db.session.commit()

        review_dict = review.to_dict()
        return make_response(jsonify(review_dict), 200)

api.add_resource(Products, '/products/')
api.add_resource(ProductByID, '/products/<int:id>')
api.add_resource(Orders, '/orders/<int:id>')
api.add_resource(Reviews, '/reviews/')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
