from cornice_swagger.swagger import CorniceSwagger
from pyramid.view import view_config
from cornice.service import get_services


@view_config(route_name="__api__", renderer='json')
def openAPI_spec(request):
    my_generator = CorniceSwagger(get_services())
    my_spec = my_generator('AvalonAPI', '1.0.0')
    return my_spec


@view_config(route_name="api", renderer='templates/api.jinja2')
def whoami(request):
    api_url = request.route_url('__api__')
    return {'api_url': api_url}
