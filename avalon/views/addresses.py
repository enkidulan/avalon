import colander
from cornice.resource import resource, view
from cornice.validators import colander_body_validator

from avalon.schemas import SchemaBuilder, Schematic
from avalon.models import Address
from colanderalchemy import SQLAlchemySchemaNode


class AddressSchema(SchemaBuilder):
    class_ = Address

    class create(Schematic):
        includes = ['address', 'phone', 'note']
        description = 'Create Address Schema'

        resp_400_body_schema = True

        def resp_200_body_schema(cls, node, schema):
            return SQLAlchemySchemaNode(
                Address, includes=['id', 'address', 'phone', 'note'])

    # class view(Schematic):
    #     includes = ['id', 'address', 'phone', 'note']
    #     description = 'View Address Schema'

    # class update(Schematic):
    #     includes = ['address', 'phone', 'note']
    #     description = 'Update Address Schema'

    class delete(Schematic):
        includes = ['id']
        description = 'Delete Address Schema'

    # class listing(Schematic):
    #     includes = ['description', 'status', 'price']
    #     description = 'Listing Address Schema'

        def resp_body_schema(cls, node, schema):
            return type(
                'AddressListingSchema',
                (colander.SequenceSchema,),
                {'body': schema})(decription='Address Listing Schema')

AddressSchema = AddressSchema()


@resource(
    name='addresses',
    description='AddressSchema management endpoint',
    tags=['UserAddresses'],
    collection_path='/user/{username}/address',
    path='/user/{username}/address/{id}',
    permission='edit'
)
class UserAddressCRUD:

    def __init__(self, request):
        self.request = request

    @view(
        schema=AddressSchema.create,
        response_schemas=AddressSchema.create.responses,
        validators=(colander_body_validator,))
    def collection_post(self):
        """ Creates a Address """
        raise

    # @view(response_schemas=AddressSchema.listing.responses)
    # def collection_get(self):
    #     """ Returns list of Orders """
    #     raise

    # @view(response_schemas=AddressSchema.view.responses)
    # def get(self):
    #     """Shows all Address data"""
    #     raise

    # @view(
    #     schema=AddressSchema.update,
    #     response_schemas=AddressSchema.update.responses,
    #     validators=(colander_body_validator,))
    # def put(self):
    #     """ Updates Orders fields """
    #     raise

    @view(response_schemas=AddressSchema.delete.responses)
    def delete(self):
        """ Delete Address """
        raise
