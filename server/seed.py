#!/usr/bin/env python3

# Standard library imports
# from random import randint, choice as rc

# Remote library imports
# from faker import Faker

# Local imports
from app import app
from models import db,Product,Order
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    sukumawiki = Product(
        name="Sukumawiki",
        image="https://images.pexels.com/photos/9465761/pexels-photo-9465761.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=11.50,
        type='Vegetable'
    )

    cabbage = Product(
        name="Cabbage",
        image="https://images.pexels.com/photos/134877/pexels-photo-134877.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=14.50,
        type='Vegetable'
    )
    
    tomato = Product(
        name="Tomato",
        image="https://images.pexels.com/photos/3943197/pexels-photo-3943197.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=7.00,
        type='Vegetable'
    )
    
    cucumber = Product(
        name="Cucumber",
        image="https://images.pexels.com/photos/4203056/pexels-photo-4203056.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=5.50,
        type='Vegetable'
    )
    
    broccoli = Product(
        name="Broccoli",
        image="https://images.pexels.com/photos/47347/broccoli-vegetable-food-healthy-47347.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=9.50,
        type='Vegetable'
    )
    apple = Product(
        name="apple",
        image="https://images.pexels.com/photos/206959/pexels-photo-206959.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=12.50,
        type = 'Fruit'
    )
    banana = Product(
        name="Banana",
        image="https://images.pexels.com/photos/1093038/pexels-photo-1093038.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=3.50,
        type = 'Fruit'
    )
    grapes = Product(
        name="Grapes",
        image="https://images.pexels.com/photos/708777/pexels-photo-708777.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=20.00,
        type = 'Fruit'
        
    )
    orange = Product(
        name="Orange",
        image="https://images.pexels.com/photos/2294477/pexels-photo-2294477.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=14.00,
        type = 'Fruit'
    )
    pears = Product(
        name="Pears",
        image="https://images.pexels.com/photos/2987077/pexels-photo-2987077.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=3.00,
        type = 'Fruit'
    )
    milk = Product(
        name="Milk",
        image="https://images.pexels.com/photos/248412/pexels-photo-248412.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=24.00,
        type = 'Dairy',
    )
    cream = Product(
        name="Cream",
        image="data:image/jpeg;base64,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",
        price=25.00,
        type = 'Dairy',
    )
    yoghurt = Product(
        name="Yoghurt",
        image="https://images.pexels.com/photos/373882/pexels-photo-373882.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=26.50,
        type = 'Dairy',
    )
    butter = Product(
        name="Butter",
        image="https://images.pexels.com/photos/3821250/pexels-photo-3821250.jpeg?auto=compress&cs=tinysrgb&w=600",
        price=29.00,
        type = 'Dairy',
    )
    cheese = Product(
        name="Cheese",
        image="https://media.istockphoto.com/id/1127471287/photo/cheese-on-white.jpg?b=1&s=612x612&w=0&k=20&c=hGLwrwCq5501O2QtXyYOU4q9oqpvfR_IegBdXITFzYs=",
        price=30.00,
        type = 'Dairy',
    )
     

    db.session.add_all([sukumawiki,broccoli,cabbage,tomato,cucumber,apple,banana,grapes,orange,pears,milk,cream,yoghurt,butter,cheese])
    db.session.commit()


if __name__ == '__main__':
    
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!
