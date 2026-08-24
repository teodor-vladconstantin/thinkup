from api.api_crud_awards import API_CRUD_AWARDS
from dynamoDB import setup
from flask import Blueprint, request
from model.entity.awards.award import Award
from utils.jwt_server import require_auth

urlAwards = Blueprint('views', __name__)
dbCrudAwards = setup.startSetup('Awards')
apiAwards = API_CRUD_AWARDS(dbCrudAwards)


@urlAwards.route('/awards/<string:id>', methods=['GET'])
@require_auth()
def get_award(id):
    return apiAwards.get_award(id)


@urlAwards.route('/awards/<string:id>', methods=['POST'])
@require_auth()
def add_award(id):
    awardJSON = request.json
    awardOBJ = Award(id, awardJSON['name'], awardJSON['userId'], awardJSON['description'], awardJSON['imageId'])

    return apiAwards.add_award(awardOBJ)


@urlAwards.route('/awards/<string:id>', methods=['DELETE'])
@require_auth()
def delete_award(id):
    return apiAwards.delete_award(id)


@urlAwards.route('/goals/<string:id>', methods=['PUT'])
@require_auth()
def update_award(id):
    awardJson = request.json
    apiAwards.update_award(awardJson)
