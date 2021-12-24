"""
See https://gist.github.com/dkarchmer/d85e55f9ed5450ba58cb
This API generically supports DjangoRestFramework based APIs
It is based on https://github.com/samgiles/slumber, but customized for
Django Rest Frameworks, and the use of TokenAuthentication.
Usage:
    # Assuming
    # v1_api_router.register(r'some_model', SomeModelViewSet)
    api = Api('http://127.0.0.1:8000')
    api.login(email='user1@test.com', password='user1')
    obj_list = api.some_model.get()
    logger.debug('Found {0} groups'.format(obj_list['count']))
    obj_one = api.some_model(1).get()
    api.logout()
"""
import logging
import requests
import warnings
from odecloud.api.exceptions import (
    ImproperlyConfigured,
    HttpClientError,
    HttpCouldNotVerifyServerError,
    HttpNotFoundError,
    HttpServerError,
    RestBaseException,
)

logger = logging.getLogger(__name__)


class RestResource:
    """
    Resource provides the main functionality behind a Django Rest Framework based API. It handles the
    attribute -> url, kwarg -> query param, and other related behind the scenes
    python to HTTP transformations. It's goal is to represent a single resource
    which may or may not have children.
    """

    def __init__(self, session, base_url, *args, **kwargs):
        self._session = session
        self._base_url = base_url
        self._store = kwargs

    def __call__(self, id=None):
        """
        Returns a new instance of self modified by one or more of the available
        parameters. These allows us to do things like override format for a
        specific request, and enables the api.resource(ID).get() syntax to get
        a specific resource by it's ID.
        """

        new_url = self._base_url

        if not new_url.endswith('/'):
            new_url += '/'

        if id:
            new_url += f'{id}/'

        return self._get_resource(session=self._session, base_url=new_url)

    def __getattr__(self, item):
        # Don't allow access to 'private' by convention attributes.
        if item.startswith("_"):
            raise AttributeError(item)

        kwargs = self._store.copy()
        return self._get_resource(self._session, f"{self._base_url}{item}/", **kwargs)

    def _get_resource(self, session, base_url, **kwargs):
        return self.__class__(session, base_url, **kwargs)

    def _check_for_errors(self, resp, url):
        if 400 <= resp.status_code <= 499:
            exception_class = HttpNotFoundError if resp.status_code == 404 else HttpClientError
            error_msg = f'{resp.status_code} CLIENT ERROR: {url}'
            
            if resp.status_code == 400 and resp.content:
                error_msg += f'({resp.content})'
                
            raise exception_class(error_msg, response=resp, content=resp.content)
        
        elif 500 <= resp.status_code <= 599:
            raise HttpServerError(f"{resp.status_code} SERVER ERROR: {url}", response=resp, content=resp.content)

    def _try_to_serialize_response(self, resp):
        try:
            return resp.json()
        except Exception:
            return resp.content

    def _process_response(self, resp):
        self._check_for_errors(resp, self._base_url)

        if 200 <= resp.status_code <= 299:
            return self._try_to_serialize_response(resp)

    def url(self):
        return self._base_url

    def _convert_ssl_exception(self, requester, **kwargs):
        try:
            return requester(self._base_url, **kwargs)
        except requests.exceptions.SSLError as err:
            raise HttpCouldNotVerifyServerError("Could not verify the server's SSL certificate", err) from err

    def get(self, **kwargs):
        resp = self._convert_ssl_exception(self._session.get, params=kwargs)
        return self._process_response(resp)

    def post(self, data=None, **kwargs):
        resp = self._convert_ssl_exception(self._session.post, json=data, params=kwargs)
        return self._process_response(resp)

    def patch(self, data=None, **kwargs):
        resp = self._convert_ssl_exception(self._session.patch, json=data, params=kwargs)
        return self._process_response(resp)

    def delete(self, data=None, **kwargs):
        resp = self._convert_ssl_exception(self._session.delete, json=data, params=kwargs)
        return resp.status_code == 204
    
    
class _TimeoutHTTPAdapter(requests.adapters.HTTPAdapter):
    """Custom http adapter to allow setting timeouts on http verbs.
    See https://github.com/psf/requests/issues/2011#issuecomment-64440818
    and surrounding discussion in that thread for why this is necessary.
    Short answer is that Session() objects don't support timeouts.
    """

    def __init__(self, timeout=None, *args, **kwargs):
        self.timeout = timeout
        super(_TimeoutHTTPAdapter, self).__init__(*args, **kwargs)

    def send(self, *args, **kwargs):
        kwargs['timeout'] = self.timeout
        return super(_TimeoutHTTPAdapter, self).send(*args, **kwargs)


class Api(object):
    resource_class = RestResource
    _client_key = None
    _client_secret = None
    _user_id = None
    
    def __init__(self, base_url, client_key=None, client_secret=None, user_id=None, verify=True, timeout=None, retries=None):
        self.base_url = f'{base_url}'
        
        self.session = requests.Session()
        self.session.verify = verify
        
        if client_key and client_secret and user_id:
            self._user_id = user_id
            self.session.headers.update({
                'x-client-key': client_key,
                'x-client-secret': client_secret
            })
        elif client_key or client_secret or user_id:
            raise HttpClientError('Not all credentials were provided. Please try again.')
        warnings.warn("Please login, via login(), to access OdeCloud's API.")
        
        if retries is not None or timeout is not None:
            adapter = _TimeoutHTTPAdapter(max_retries=retries, timeout=timeout)
            self.session.mount('https://', adapter)
            self.session.mount('http://', adapter)

    def url(self, section):
        return f'{self.base_url}/{section}/'
    
    def user_id(self):
        return self._user_id
    
    def _request_secret(self, email, password):
        try:
            r = self.session.post(self.url('oauth/request'), json={'email': email, 'password': password})
        except requests.exceptions.SSLError as err:
            raise HttpCouldNotVerifyServerError("Could not verify the server's SSL certificate", err) from err

        if r.status_code == 201:
            secret_data = r.json()
                   
            if 'secret' not in secret_data:
                raise HttpServerError("Invalid response from OdeCloud's servers: no secret code was given")
            
            secret_code = secret_data['secret']
            return secret_code
        
        raise HttpServerError(f'ERROR {r.status_code}: {r.content.decode()["detail"]}')
        
    def login(self, email, password):
        try:
            secret_code = self._request_secret(email, password)
            r = self.session.post(self.url('oauth/login'), json={'secret': secret_code})
            
        except requests.exceptions.SSLError as err:
            raise HttpCouldNotVerifyServerError("Could not verify the server's SSL certificate", err) from err        
        except HttpServerError as err:
            raise HttpServerError("Invalid response from OdeCloud's servers: no secret code was given")
        
        if r.status_code == 403:
            raise HttpServerError('Credentials expired. Re-authenticate with /oauth/request/')
        
        if r.status_code == 201:
            client_credentials = r.json()
            
            if 'clientKey' not in client_credentials:
                raise HttpServerError("Invalid response from OdeCloud's server: no client key was given")
            
            if 'clientSecret' not in client_credentials:
                raise HttpServerError("Invalid response from OdeCloud's server: no client secret was given")
        
            if 'userId' not in client_credentials:
                raise HttpServerError("Invalid response from OdeCloud's server: no user ID was given")
            
            self._user_id = client_credentials['userId']
            
            self.session.headers.update({
                'x-client-key': client_credentials['clientKey'],
                'x-client-secret': client_credentials['clientSecret']
            })
            return
        
        raise HttpServerError(f'ERROR {r.status_code}: {r.content.decode()}')

    def logout(self) -> None:
        self._user_id = None
        self._client_key = None
        self._client_secret =  None
    
    def __call__(self, id):
        return self.resource_class(session=self.session, base_url=self.url(id))

    def __getattr__(self, item):
        """
        Instead of raising an attribute error, the undefined attribute will
        return a Resource Instance which can be used to make calls to the
        resource identified by the attribute.
        """

        # Don't allow access to 'private' by convention attributes.
        if item.startswith("_"):
            raise AttributeError(item)

        return self.resource_class(session=self.session, base_url=self.url(item))