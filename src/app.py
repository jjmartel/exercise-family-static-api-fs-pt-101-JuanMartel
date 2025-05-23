"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"success": "true",
                     "family": members}
    return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def new_member():
    data = request.json
    new = jackson_family.add_member(data)
    response_body = {"success": "true",
                     "family": new}
    return jsonify(response_body)

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_a_member(id):
    deleted = jackson_family.delete_member(id)
    if deleted is None:
        return jsonify({"Error": "Not a Jackson Member"}), 404
    response_body = {"success": "true",
                     "delete_member": deleted}
    return jsonify(response_body), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Not a Jackson Member"}), 404


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
 