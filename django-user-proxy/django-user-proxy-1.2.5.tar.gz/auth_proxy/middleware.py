from .models import UserProxy


class GenerateUserProxy:
    def process_request(self, request):
        if request.user.is_authenticated() and not UserProxy.objects.filter(user_id=request.user.uuid).exists():
            UserProxy(
                user_id=request.user.uuid
            ).save(
            )


class GenerateUserProxyM:
    def __init__(self, response):
        self.response = response

    def __call__(self, request):
        if request.user.is_authenticated and not UserProxy.objects.filter(user_id=request.user.uuid).exists():
            UserProxy(
                user_id=request.user.uuid
            ).save(
            )

        return self.response(request)


class AddUserProxyToRequest:
    def process_request(self, request):
        user_proxy = UserProxy.objects.filter(user_id=request.user.uuid)
        if request.user.is_authenticated() and user_proxy.exists():
            request.user_proxy = user_proxy.first()
