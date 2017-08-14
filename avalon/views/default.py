from cornice import Service
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPForbidden
from ..models import User
from cornice.validators import colander_body_validator
from cornice_swagger.swagger import CorniceSwagger
from cornice.service import get_services
import colander
from avalon import schemas
import colander

user_schema = lambda: schemas.UserSchema

users = Service(
    name='users',
    path='/users/{username}',
    description='Users management endpoint')

import pdb; pdb.set_trace()

UserResponceSchema = type('UserResponceSchema', (schemas.UserSchema.typ.__class__,), {f.name: f.typ for f in schemas.UserSchema.children})

# {'children': schemas.UserSchema.children})

# Create a response schema for our 200 responses
class OkResponseSchema(colander.MappingSchema):
    body = UserResponceSchema(description="User schema response")


# Create a body schema for our requests
class BodySchema(colander.MappingSchema):
    value = colander.SchemaNode(colander.String(),
                                description='My precious value')
    name = colander.SchemaNode(colander.String(),
                                description='My precious name')

# Create a response schema for our 200 responses
class notResponseSchema(colander.MappingSchema):
    body = BodySchema()


# import pdb; pdb.set_trace()

response_schemas = {
    '200': OkResponseSchema(description="Return Value"),
    '400': notResponseSchema(description="not foues Value"),
    '500': UserResponceSchema(),
}


@users.get(response_schemas=response_schemas)
def get(request):
    """Shows user data"""
    username = request.matchdict['username']
    user = request.dbsession.query(User).filter(User.username == username).one()
    return user_schema().dictify(user)


@users.post(schema=user_schema, response_schemas=response_schemas, validators=(colander_body_validator,))
def create(request):
    """ Updates users fields """
    username = request.authenticated_userid
    if request.matchdict["username"] != username:
        raise HTTPForbidden()
    _USERS[username] = request.json_body
    return {'success': True}


# Create a service to serve our OpenAPI spec
swagger = Service(name='Avalon API',
                  path='/__api__',
                  description="Avalon API documentation")


@swagger.get()
def openAPI_spec(request):
    my_generator = CorniceSwagger(get_services())
    my_spec = my_generator('AvalonAPI', '1.0.0')
    return my_spec

# @view_config(route_name="whoami", permission="authenticated", renderer="json")
# def whoami(request):
#     """View returning the authenticated user's credentials."""
#     username = request.authenticated_userid
#     principals = request.effective_principals
#     return {"username": username, "principals": principals}
