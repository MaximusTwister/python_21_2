from hashlib import sha256
import io
from bson.json_util import dumps
from bson.objectid import ObjectId
from functools import wraps

from flask import Flask, request, Response, render_template

from constants import SECRET_KEY
from validators import validate_and_save
from forms import SignUpForm
from mongo_infra import users_coll
from utils import query_flights, encode_jwt, decode_jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {"error": "A valid token is missing"}
        _, jwt_token = token.split()
        user_id, error = decode_jwt(jwt_token=jwt_token, key=app.config.get('SECRET_KEY'))
        if not error and user_id:
            user = users_coll.find_one({'_id': ObjectId(user_id)})
            print(f"User: {user}")
        else:
            return {"error": error}
        return func(*args, **kwargs)
    return decorator


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if users_coll.find_one({'email': form.email.data}):
            form.email.errors.append('This email already exist')
        else:
            hashed_password = sha256(form.password.data.encode()).hexdigest()
            query = {'name': form.name.data, 'password': hashed_password}
            insert_res = users_coll.insert_one(query)
            user_id = str(insert_res.inserted_id)
            jwt_token = encode_jwt(user_id, key=app.config.get('SECRET_KEY'))
            virtual_file = io.StringIO(jwt_token)
            return Response(
                virtual_file,
                mimetype='text/plain',
                headers={"Content-Disposition": "attachment;filename=token"}
            )

    return render_template('signup.jinja', form=form)


@app.route("/add_flight", methods=["POST"])
def add_flight():
    status_code, errors = validate_and_save(json_object=request.json, object_type='flight')
    return Response(response=errors, status=status_code, mimetype='application/json')


@app.route('/get_flights', methods=["GET"])
@token_required
def get_flights():
    token = request.headers.get('Authorization')
    print(f"TOKEN: {token}")
    flights = query_flights()
    return Response(response=dumps(flights), mimetype='application/json')


@app.route("/add_ac", methods=['POST'])
def add_ac():
    status_code, errors = validate_and_save(json_object=request.json, object_type='ac')
    return Response(response=errors, status=status_code, mimetype='application/json')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
