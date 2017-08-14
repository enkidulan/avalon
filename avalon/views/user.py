import colander
from cornice import Service
from pyramid.httpexceptions import HTTPForbidden
from cornice.validators import colander_body_validator

from avalon import schemas
from avalon.models import User

USERS = Service(
    name='users',
    path='/users/{username}',
    description='Users management endpoint')


class OkResponseSchema(colander.MappingSchema):
    body = schemas.UserSchema().swagger


class NotFoundResponseSchema(colander.MappingSchema):
    pass


response_schemas = {
    '200': OkResponseSchema(description="successful operation"),
    '404': NotFoundResponseSchema(description="user not found"),
}


@USERS.get(tags=['Users'], response_schemas=response_schemas)
def get(request):
    """Shows user data"""
    username = request.matchdict['username']
    user = request.dbsession.query(User).filter(User.username == username).one()
    return schemas.UserSchema.dictify(user)


@USERS.post(tags=['Users'], schema=schemas.UserSchema, response_schemas=response_schemas, validators=(colander_body_validator,))
def create(request):
    """ Updates users fields """
    username = request.authenticated_userid
    if request.matchdict["username"] != username:
        raise HTTPForbidden()
    _USERS[username] = request.json_body
    return {'success': True}
