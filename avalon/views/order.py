import colander
from cornice.resource import resource, view
from cornice.validators import colander_body_validator

from avalon.schemas import SchemaBuilder, Schematic
from avalon.models import Order


class OrderSchema(SchemaBuilder):
    class_ = Order

    class create(Schematic):
        includes = [
            'description', 'price', 'delivery_address', 'resources', 'seller', 'buyer']
        description = 'Create Order Schema'

    class view(Schematic):
        includes = ['id', 'status', 'description', 'price', 'delivery_address', 'resources', 'seller', 'buyer']
        description = 'View Order Schema'

    class update(Schematic):
        includes = ['description', 'status']
        description = 'Update Order Schema'

    class delete(Schematic):
        includes = ['id']
        description = 'Delete User Schema'

    class listing(Schematic):
        includes = ['description', 'status', 'price']
        description = 'Listing Order Schema'

        def resp_body_schema(cls, node, schema):
            return type(
                'OrdersListingSchema',
                (colander.SequenceSchema,),
                {'body': schema})(decription='OrdersListingSchema')

    class dashboard_listing(Schematic):
        includes = ['seller', 'status']
        description = 'Public List of User Schema'

    class dashboard_view(Schematic):
        includes = ['seller', 'buyer', 'status']
        description = 'Public User Profile Schema'

OrderSchema = OrderSchema()


@resource(
    name='orders',
    description='Orders management endpoint',
    tags=['Order'],
    collection_path='/orders',
    path='/orders/{id}',
    permission='manage'
)
class OrdersCRUD:

    def __init__(self, request):
        self.request = request

    @view(
        schema=OrderSchema.create,
        response_schemas=OrderSchema.create.responses,
        validators=(colander_body_validator,))
    def collection_post(self):
        """ Creates a Order """
        raise

    @view(response_schemas=OrderSchema.listing.responses)
    def collection_get(self):
        """ Returns list of Orders """
        raise

    @view(response_schemas=OrderSchema.view.responses)
    def get(self):
        """Shows all Order data"""
        Ordername = self.request.matchdict['Ordername']
        Order = self.request.dbsession.query(Order).filter(
            Order.Ordername == Ordername).first()

        if Order is None:
            self.request.response.status = 404
            return OrderSchema.view.responses['404']['body'].deserialize({'param': Ordername, 'status': 'Not Found'})
        return OrderSchema.view.responses['200']['body'].dictify(Order)

    @view(
        schema=OrderSchema.update,
        response_schemas=OrderSchema.update.responses,
        validators=(colander_body_validator,))
    def put(self):
        """ Updates Orders fields """
        raise

    @view(response_schemas=OrderSchema.delete.responses)
    def delete(self):
        """ Delete Order """
        raise


@resource(
    name='dasboard/orders',
    description='Orders Public Dashboard Endpoint',
    tags=['Order', 'Dashboard'],
    collection_path='/dasboard/orders',
    path='/dasboard/orders/{Ordername}',
    permission='view'
)
class OrdersCRUD:

    def __init__(self, request):
        self.request = request

    @view(response_schemas=OrderSchema.dashboard_listing.responses)
    def collection_get(self):
        """ Returns list of Orders """
        raise

    @view(response_schemas=OrderSchema.dashboard_view.responses)
    def get(self):
        """Shows all Order data"""
        Ordername = self.request.matchdict['Ordername']
        Order = self.request.dbsession.query(Order).filter(
            Order.Ordername == Ordername).first()

        if Order is None:
            self.request.response.status = 404
            return OrderSchema.dashboard_Order_view.responses['404']['body'].deserialize({'param': Ordername, 'status': 'Not Found'})
        return OrderSchema.dashboard_Order_view.responses['200']['body'].dictify(Order)
