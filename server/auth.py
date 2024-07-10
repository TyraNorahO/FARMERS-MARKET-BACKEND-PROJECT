from flask_jwt_extended import JWTManager,jwt_required
from flask import Blueprint
from flask_restful import API,Resource,reqparse
from models import RegisterUser,db
from flask_bcrypt import Bcrypt


auth_bp = Blueprint('auth_bp',__name__,url_prefix='/auth')
auth_api = API(auth_bp)
jwt = JWTManager()

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return RegisterUser.query.filter_by(id=identity).first()



bcrypt = Bcrypt()

register_agrs = reqparse.Request.Parser()
register_agrs.add_argument('email')
register_agrs.add_argument('password1')
register_agrs.add_argument('password2')

#registering
class Signup(Resource):
    def post(self):
        data = register_agrs.parse_args()
        #hash password
        if data.get("password1") != data.get("password2"):
            return {"msg":"Password dont match"}
        hash_password = Bcrypt.generate_password_hash(data.get('password'))
        new_user = RegisterUser(email=data.get('email'),password = hash_password)
        db.session.add(new_user)
        db.commit()

        return {"msg":"You have signed up successfully"}
    


#login

login_agrs = reqparse.Request.Parser()
login_agrs.add_argument('email')
login_agrs.add_argument('password1')

class Login(Resource):
    def post(self):
        data = login_agrs.parse_agrs()

        user = RegisterUser.query.filter_by(email = data.get('email')).first()

        if not user :
            return {"msg":"The email doesnot exist"}
        if not bcrypt.check_password_hash(user.password,data.get('password')):
            return {"msg":"Incorrect password"}
        
        token = create_access_token(identity=user.id)
        refresh_token = create_refreshed_token(identity=user.id)
        return {"token" :token,'refresh_token':refresh_token}
    
    @jwt_required()
    def get(self):
        user = current_user
        return {'email': user.email}

#access to certain resource
auth_api.add_resource(Signup,'/signup')
auth_api.add_resource(Login,'/login')