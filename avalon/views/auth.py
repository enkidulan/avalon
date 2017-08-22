from collections import defaultdict

from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

import colander
from cornice.resource import resource, view
from cornice.validators import colander_body_validator

from avalon.schemas import SchemaBuilder, Schematic
from avalon.models import User
from colanderalchemy import SQLAlchemySchemaNode

from cornice import Service


class LoginUserSchema(SchemaBuilder):
    class_ = User

    class create(Schematic):
        includes = ['username', 'fullname']
        description = 'Login User Schema'

        resp_400_body_schema = True

        def resp_200_body_schema(cls, node, schema):
            return SQLAlchemySchemaNode(
                User, includes=['id', 'username'])

LoginUserSchema = LoginUserSchema()


login = Service(name='login', path='/login', description='User login')
logout = Service(name='logout', path='/logout', description='User logout')


@login.post(
    schema=LoginUserSchema.create,
    response_schemas=LoginUserSchema.create.responses,
    validators=(colander_body_validator,),
    tags=['Authorization'],
)
def login(request):
    raise


@logout.get(
    response_schemas=LoginUserSchema.create.responses,
    validators=(colander_body_validator,),
    tags=['Authorization'],
)
def logout(request):
    raise
