from cornice_swagger.swagger import CorniceSwagger
from pyramid.view import view_config
from cornice.service import get_services
from cornice import Service


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
