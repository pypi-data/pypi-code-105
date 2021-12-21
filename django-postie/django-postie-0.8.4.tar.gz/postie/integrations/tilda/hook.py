from django.http.response import HttpResponse

from .utils import get_tilda_credentials
from .tasks import handle_webhook_task
from .signals import tilda_webhook_received


def webhook_receiver(request):
    credentials = get_tilda_credentials()

    public_key = request.GET.get('publickey')
    project_id = int(request.GET.get('projectid') or 0)
    page_id = int(request.GET.get('pageid') or 0)

    tilda_webhook_received.send(None, request=request, credentials=credentials)

    if credentials.public_key == public_key and credentials.project_id == project_id:
        handle_webhook_task.delay(project_id, page_id)
        return HttpResponse('ok')

    return HttpResponse()
