from .models import UserProxy


class GenerateUserProxy:
    def process_request(self, request):
        if request.user.is_authenticated() and not UserProxy.objects.filter(user_id=request.user).exists():
            UserProxy(
                user_id=request.user.uuid
            ).save(
            )


class AddUserProxyToRequest:
    def process_request(self, request):
        user_proxy = UserProxy.objects.filter(user_id=request.user.uuid)
        if request.user.is_authenticated() and user_proxy.exists():
            request.user_proxy = user_proxy.first()
