import colander
from cornice.resource import resource, view
from cornice.validators import colander_body_validator

from avalon.schemas import SchemaBuilder, Schematic
from avalon.models import User


class UserSchema(SchemaBuilder):
    class_ = User

    class create(Schematic):
        includes = ['username', 'email', 'fullname', 'role']
        description = 'Create User Schema'

    class view(Schematic):
        includes = ['email', 'fullname', 'addresses', 'sold', 'bought']
        description = 'View User Schema'

    class update(Schematic):
        includes = ['email', 'fullname', 'addresses']
        description = 'Update User Schema'

    class delete(Schematic):
        includes = ['username']
        description = 'Delete User Schema'

    class listing(Schematic):
        includes = ['username', 'role']
        description = 'Listing Users Schema'

        def resp_body_schema(cls, node, schema):
            return type(
                'UsersListingSchema',
                (colander.SequenceSchema,),
                {'body': schema})(decription='UsersListingSchema')

    class dashboard_listing(Schematic):
        includes = ['username']
        description = 'Public List of User Schema'

    class dashboard_user_view(Schematic):
        includes = ['username', 'sold_count', 'bought_count']
        description = 'Public User Profile Schema'

UserSchema = UserSchema()


@resource(
    name='users',
    description='Users management endpoint',
    tags=['Users'],
    collection_path='/users',
    path='/users/{username}',
    permission='manage'
)
class UsersCRUD:

    def __init__(self, request):
        self.request = request

    @view(
        schema=UserSchema.create,
        response_schemas=UserSchema.create.responses,
        validators=(colander_body_validator,))
    def collection_post(self):
        """ Creates a user """
        raise

    @view(response_schemas=UserSchema.listing.responses)
    def collection_get(self):
        """ Returns list of users """
        raise

    @view(response_schemas=UserSchema.view.responses)
    def get(self):
        """Shows all user data"""
        username = self.request.matchdict['username']
        user = self.request.dbsession.query(User).filter(
            User.username == username).first()

        if user is None:
            self.request.response.status = 404
            return UserSchema.view.responses['404']['body'].deserialize({'param': username, 'status': 'Not Found'})
        return UserSchema.view.responses['200']['body'].dictify(user)

    @view(
        schema=UserSchema.update,
        response_schemas=UserSchema.update.responses,
        validators=(colander_body_validator,))
    def put(self):
        """ Updates users fields """
        raise

    @view(response_schemas=UserSchema.delete.responses)
    def delete(self):
        """ Delete user """
        raise


@resource(
    name='dasboard_users',
    description='Users Public Dashboard Endpoint',
    tags=['Users'],
    collection_path='/dasboard_users',
    path='/dasboard_users/{username}',
    permission='view'
)
class UsersCRUD:

    def __init__(self, request):
        self.request = request

    @view(response_schemas=UserSchema.dashboard_listing.responses)
    def collection_get(self):
        """ Returns list of users """
        raise

    @view(response_schemas=UserSchema.dashboard_user_view.responses)
    def get(self):
        """Shows all user data"""
        username = self.request.matchdict['username']
        user = self.request.dbsession.query(User).filter(
            User.username == username).first()

        if user is None:
            self.request.response.status = 404
            return UserSchema.dashboard_user_view.responses['404']['body'].deserialize({'param': username, 'status': 'Not Found'})
        return UserSchema.dashboard_user_view.responses['200']['body'].dictify(user)
