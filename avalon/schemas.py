from colanderalchemy import SQLAlchemySchemaNode
from avalon import models


class SchemaBuilder:

    def __new__(cls):
        params = dict(cls.__dict__.items())
        swagger_schema = SQLAlchemySchemaNode(**params)
        schema = SQLAlchemySchemaNode(**params)
        del swagger_schema.inspector
        del swagger_schema.class_
        schema.swagger = swagger_schema
        return schema


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


class OrderSchema(SchemaBuilder):
    class_ = models.Order
    # includes = ['description', 'status', 'price', 'feedback', 'delivery_address', 'resources', 'seller', 'buyer']
    excludes = ['id', 'resources_id', 'seller_id', 'buyer_id', 'seller', 'buyer', 'delivery_address', 'resources']
    title = 'Order class'
    description = 'Users order schema'


class UserSchema(SchemaBuilder):
    class_ = models.User
    includes = ['username', 'email', 'fullname', 'role']
    excludes = ['id']
    title = 'User class'
    description = 'User schema'
