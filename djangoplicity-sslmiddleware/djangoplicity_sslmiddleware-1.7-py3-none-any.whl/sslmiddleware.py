__license__ = "Python"
__copyright__ = "Copyright (C) 2007, Stephen Zabel"
__author__ = "Stephen Zabel - sjzabel@gmail.com"
__contributors__ = "Jay Parlar - parlar@gmail.com"

# With contributions from ESO.


from django.conf import settings
from django.http import HttpResponsePermanentRedirect

SSL = 'SSL'
SSLAllow = 'SSLAllow'


class SSLRedirect(object):
	def __init__(self, get_response):   
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		return response

	def process_view(self, request, view_func, view_args, view_kwargs):
		if SSL in view_kwargs:
			secure = view_kwargs[SSL]
			del view_kwargs[SSL]
		else:
			secure = False

		if hasattr(settings, 'ALLOW_SSL') and settings.ALLOW_SSL:
			allow_ssl = True
			if SSLAllow in view_kwargs:
				del view_kwargs[SSLAllow]
		else:
			if SSLAllow in view_kwargs:
				allow_ssl = view_kwargs[SSLAllow]
				del view_kwargs[SSLAllow]
			else:
				allow_ssl = False

		if settings.ENABLE_SSL:
			if allow_ssl:
				if secure and not self._is_secure(request):
					return self._redirect(request, secure)
			else:
				if not secure == self._is_secure(request):
					return self._redirect(request, secure)

	def _is_secure(self, request):
		if request.is_secure():
			return True

		#Handle the Webfaction case until this gets resolved in the request.is_secure()
		if 'HTTP_X_FORWARDED_SSL' in request.META:
			return request.META['HTTP_X_FORWARDED_SSL'] == 'on'

		return False

	def _redirect(self, request, secure):
		protocol = secure and "https" or "http"
		newurl = "%s://%s%s" % (protocol, request.get_host(), request.get_full_path())
		if settings.DEBUG and request.method == 'POST':
			raise RuntimeError(
		"""Django can't perform a SSL redirect while maintaining POST data.
		   Please structure your views so that redirects only occur during GETs.""")

		return HttpResponsePermanentRedirect(newurl)
