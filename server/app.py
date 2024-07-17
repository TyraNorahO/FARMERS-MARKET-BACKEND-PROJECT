from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity
from auth import auth_bp, bcrypt
from models import db, Customer, Product as ProductModel, Order, OrderItem, Review
from datetime import datetime

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

class ProductList(Resource):
    def get(self):
        type_filter = request.args.get('type')
        price_range = request.args.get('priceRange')
        
        query = ProductModel.query
        
        if type_filter:
            query = query.filter_by(type=type_filter)
        
        if price_range:
            min_price, max_price = map(float, price_range.split('-'))
            query = query.filter(ProductModel.price >= min_price, ProductModel.price <= max_price)
        
        products = query.all()
        
        product_list = []
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'type': product.type,
                'image': product.image  # Assuming you have this attribute
            }
            product_list.append(product_data)
        return product_list, 200

class ProductByID(Resource):
    @jwt_required()
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
        return make_response(jsonify({"message": "Order deleted successfully"}), 204)

class Reviews(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()

        data = request.get_json()
        comment = data.get("comment")

        if not comment:
            return make_response(jsonify({"message": "Comment is required"}), 400)

        review = Review(
            comment=comment,
            date_reviewed=datetime.utcnow(),
            customer_id=current_user_id,
            product_id=data.get("product_id")  # Assuming product_id is provided in request
        )

        db.session.add(review)
        db.session.commit()

        review_dict = review.to_dict()  # Assuming you have a method to_dict() in your Review model
        return make_response(jsonify(review_dict), 200)

    @jwt_required()
    def delete(self, id):
        delete_review = Review.query.filter_by(id=id).first()

        if not delete_review:
            return make_response(jsonify({"message": "Review not found"}), 404)

        # Check if current user is authorized to delete the review
        current_user_id = get_jwt_identity()
        if delete_review.customer_id != current_user_id:
            return make_response(jsonify({"message": "Unauthorized to delete this review"}), 403)

        db.session.delete(delete_review)
        db.session.commit()

        return make_response(jsonify({"message": "Review deleted successfully"}), 204)

api.add_resource(ProductList, '/products/')
api.add_resource(ProductByID, '/products/<int:id>')
api.add_resource(Orders, '/orders/<int:id>')
api.add_resource(Reviews, '/reviews/')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
