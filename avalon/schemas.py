from colanderalchemy import SQLAlchemySchemaNode
from avalon import models



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


OrderSchema = SQLAlchemySchemaNode(
    models.Order,
    includes=['name', 'biography'],
    excludes=['id'],
    title='Some class')


ResourceSchema = SQLAlchemySchemaNode(
    models.Resource,
    includes=['name', 'biography'],
    excludes=['id'],
    title='Some class')


UserSchema = SQLAlchemySchemaNode(
    models.User,
    includes=['username', 'email', 'fullname', 'role'],
    excludes=['id'],
    title='User class')
