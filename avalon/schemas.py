from colanderalchemy import SQLAlchemySchemaNode
from avalon import models
import colander
import inspect


class Schematic:
    pass


class SchemaBuilder:

    @classmethod
    def _contruct_responses(cls, node, schema):

        if hasattr(node, 'resp_200_body_schema'):
            schema = node.resp_200_body_schema(cls, node, schema)

        ok = type(
            'OkResponseSchema',
            (colander.MappingSchema,),
            {'body': schema}
        )(description="Successful Operation")

        not_found = type(
            'NotFoundResponseSchema',
            (colander.MappingSchema,),
            {'body': cls.NotFoundBodySchema(
                description='Requested content cannot be found')}
        )(description="Not Found")
        return {
            '200': ok,
            '404': not_found,
        }

    @classmethod
    def _contruct(cls, node):
        params = {
            k: v
            for k, v in cls.__dict__.items()
            if not (
                (inspect.isclass(v) and issubclass(v, Schematic))
                or k.startswith('_'))
        }
        params.update(node.__dict__.items())
        params['includes'] = set(
            params.get('includes', [])) - set(params.get('excludes', []))
        schema = SQLAlchemySchemaNode(**params)
        schema.responses = cls._contruct_responses(node, schema)
        return schema

    class NotFoundBodySchema(colander.MappingSchema):
        param = colander.SchemaNode(
            colander.String(), description='param')
        status = colander.SchemaNode(
            colander.String(), description='status')

    def __new__(cls):
        schemas = {
            k: cls._contruct(v)
            for k, v in cls.__dict__.items()
            if inspect.isclass(v) and issubclass(v, Schematic)
        }
        return type(cls.__name__, (object, ), schemas)

        # params = dict(cls.__dict__.items())
        # params['includes'] = set(
        #     params.get('includes', [])) - set(params.get('excludes', []))
        # # swagger_schema = SQLAlchemySchemaNode(**params)
        # schema = SQLAlchemySchemaNode(**params)

        # # del swagger_schema.inspector
        # # del swagger_schema.class_
        # # schema.swagger = swagger_schema
        # return schema


AddressSchema = SQLAlchemySchemaNode(
    models.Address,
    includes=['name', 'biography'],
    excludes=['id'],
    title='Some class')


CommentSchema = SQLAlchemySchemaNode(
    models.Comment,
    includes=['name', 'biography'],
    excludes=['id'],
    title='Some class')


ResourceSchema = SQLAlchemySchemaNode(
    models.Resource,
    includes=['name', 'biography'],
    excludes=['id'],
    title='Some class')


# class OrderSchema(SchemaBuilder):
#     class_ = models.Order
#     # includes = ['description', 'status', 'price', 'feedback', 'delivery_address', 'resources', 'seller', 'buyer']
#     excludes = ['id', 'resources_id', 'seller_id', 'buyer_id', 'seller', 'buyer', 'delivery_address', 'resources']
#     title = 'Order class'
#     description = 'Users order schema'



