from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Resource
from datetime import datetime
import hashlib

def register_routes(app):

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
        new_user = User(username=data['username'],
                        password=hashed_password,
                        subscription_level=data['subscription_level'],
                        account_status=data['account_status'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and user.password == hashlib.sha256(data['password'].encode()).hexdigest():
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token)
        return jsonify({"message": "Invalid credentials"}), 401

    @app.route('/resources', methods=['POST'])
    @jwt_required()
    def add_resource():
        data = request.json
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if user.subscription_level != 'premium':
            return jsonify({"message": "Unauthorized"}), 403
        new_resource = Resource(name=data['name'],
                                access_level=data['access_level'],
                                available_hours=data['available_hours'])
        db.session.add(new_resource)
        db.session.commit()
        return jsonify({"message": "Resource added successfully!"}), 201

    @app.route('/resources', methods=['GET'])
    @jwt_required()
    def get_resources():
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        resources = Resource.query.all()
        result = []
        current_time = datetime.now().strftime("%H:%M")
        for resource in resources:
            if resource.access_level == 'basic' or user.subscription_level == 'premium':
                if resource.available_hours.split('-')[0] <= current_time <= resource.available_hours.split('-')[1]:
                    result.append({"id": resource.id, "name": resource.name})
        return jsonify(result)
