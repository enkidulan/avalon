from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
)
from pyramid.view import (
    view_config,
)


def includeme(config):
    authn_policy = AuthTktAuthenticationPolicy(secret='qwerty')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')


@view_config(route_name='login', renderer='json')
def login(request):
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        user = request.dbsession.query(User).filter_by(name=login).first()
        if user is not None and user.check_password(password):
            headers = remember(request, user.id)
            return HTTPFound(location=next_url, headers=headers)
        message = 'Failed login'

    return dict(
        message=message,
        url=request.route_url('login'),
        next_url=next_url,
        login=login,
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    next_url = request.route_url('view_wiki')
    return HTTPFound(location=next_url, headers=headers)
