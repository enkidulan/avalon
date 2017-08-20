# import colander
# from cornice import Service
# from pyramid.httpexceptions import HTTPForbidden
# from cornice.validators import colander_body_validator

# from avalon import schemas
# from avalon.models import User

# ORDERS = Service(
#     name='orders',
#     path='/users/{username}/orders/{orderId}',
#     description='Orders management endpoint')


# class OkResponseSchema(colander.MappingSchema):
#     body = schemas.OrderSchema()


# class NotFoundResponseSchema(colander.MappingSchema):
#     pass


# response_schemas = {
#     '200': OkResponseSchema(description="successful operation"),
#     '404': NotFoundResponseSchema(description="order not found"),
# }


# @ORDERS.get(tags=['Orders'], response_schemas=response_schemas)
# def get(request):
#     """Shows user data"""
#     username = request.matchdict['username']
#     user = request.dbsession.query(User).filter(User.username == username).one()
#     return schemas.OrderSchema.dictify(user)


# @ORDERS.post(tags=['Orders'], schema=schemas.OrderSchema, response_schemas=response_schemas, validators=(colander_body_validator,))
# def create(request):
#     """ Updates users fields """
#     username = request.authenticated_userid
#     if request.matchdict["username"] != username:
#         raise HTTPForbidden()
#     _USERS[username] = request.json_body
#     return {'success': True}
