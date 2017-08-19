import colander
from cornice.resource import resource, view
from pyramid.httpexceptions import HTTPForbidden
from cornice.validators import colander_body_validator

from avalon.schemas import SchemaBuilder
from avalon.models import User


# class UserSchema(SchemaBuilder):
#     class_ = User
#     schemas = {
#         'create': ['username', 'email', 'fullname', 'role'],
#         'update': ['username', 'email', 'fullname', 'role'],
#         'view': ['username', 'email', 'fullname', 'role'],
#         'list': ['username', 'email', 'fullname', 'role'],

#     }

class UserSchemaM(SchemaBuilder):
    class_ = User

    class create:
        includes = ['username', 'email', 'fullname', 'role']
        description = 'Create User Schema'

    class view:
        includes = ['email', 'fullname', 'addresses', 'sold', 'bought']
        description = 'Update User Schema'

    class update:
        includes = ['email', 'fullname', 'addresses']
        description = 'Update User Schema'

    class delete:
        includes = ['username']
        description = 'Delete User Schema'

    class list:
        includes = ['username', 'role']
        description = 'list Users Schema'




#     schemas = {
#         'create': ['username', 'email', 'fullname', 'role'],
#         'update': ['username', 'email', 'fullname', 'role'],
#         'view': ['username', 'email', 'fullname', 'role'],
#         'list': ['username', 'email', 'fullname', 'role'],

#     }

class UserSchema(SchemaBuilder):
    class_ = User
    includes = ['username', 'email', 'fullname', 'role']
    excludes = ['id']
    title = 'User class create'
    description = 'Create User Schema'


class ViewUserSchema(SchemaBuilder):
    class_ = User
    includes = ['username', 'email', 'fullname', 'role', 'addresses', 'resources', 'comments', 'sold', 'bought']
    excludes = ['id']
    title = 'User class'
    description = 'Create User Schema'


class ResponseViewUserSchema(colander.MappingSchema):
    body = ViewUserSchema()


class EditUserSchema(UserSchema):
    class_ = User
    includes = UserSchema.includes + ['addresses']
    excludes = UserSchema.excludes + ['username', 'role']
    description = 'Edit User Schema'


class OkResponseSchema(colander.MappingSchema):
    body = UserSchema()


class NotFoundBodySchema(colander.MappingSchema):
    username = colander.SchemaNode(
        colander.String(), description='user')
    status = colander.SchemaNode(
        colander.String(), description='status')


class NotFoundResponseSchema(colander.MappingSchema):
    body = NotFoundBodySchema(description='Not found body')


class UsersListingSchema(colander.SequenceSchema):
    body = UserSchema()


class ResponseUsersListingSchema(colander.MappingSchema):
    body = UsersListingSchema(description='UsersListingSchema')


response_schemas = {
    '200': OkResponseSchema(description="successful operation"),
    '404': NotFoundResponseSchema(description="user not found"),
}


@resource(
    name='users',
    description='Users management endpoint',
    tags=['Users'],
    collection_path='/users',
    path='/users/{username}',
    # collection_factory=BlogNetworkFactory,
    # collection_traverse='',
    # factory=BlogNetworkFactory,
)
class UsersCRUD:

    def __init__(self, request):
        self.request = request

    @view(
        schema=UserSchema,
        response_schemas=response_schemas,
        validators=(colander_body_validator,))
    def collection_post(self):
        """ Updates users fields """
        username = self.request.authenticated_userid
        if self.request.matchdict["username"] != username:
            raise HTTPForbidden()
        return {'success': True}

    @view(
        response_schemas={
            '200': ResponseUsersListingSchema(description="List of users")},
    )
    def collection_get(self):
        """ Returns list of users """
        username = self.request.authenticated_userid
        if self.request.matchdict["username"] != username:
            raise HTTPForbidden()
        return {'success': True}

    @view(
        response_schemas={
            '200': ResponseViewUserSchema(description='user details')}
    )
    def get(self):
        """Shows user data"""
        username = self.request.matchdict['username']
        user = self.request.dbsession.query(User).filter(
            User.username == username).first()
        if user is None:
            self.request.response.status = 404
            return response_schemas['404']['body'].deserialize(
                {'username': username, 'status': 'Not Found'})
        return UserSchema().dictify(user)

    @view(
        schema=EditUserSchema,
        response_schemas=response_schemas,
        validators=(colander_body_validator,))
    def put(self):
        """ Updates users fields """
        username = self.request.authenticated_userid
        if self.request.matchdict["username"] != username:
            raise HTTPForbidden()
        return {'success': True}

    @view(
        response_schemas=response_schemas,)
    def delete(self):
        """ Delete user """
        username = self.request.authenticated_userid
        if self.request.matchdict["username"] != username:
            raise HTTPForbidden()
        return {'success': True}
