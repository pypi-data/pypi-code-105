from collections import OrderedDict

from django.core.paginator import InvalidPage, Paginator as DjangoPaginator
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound
from rest_framework.pagination import BasePagination, _positive_int

from uboxadmin.settings import admin_settings
from uboxadmin.utils import make_response


class PageNumberPagination(BasePagination):
    page_size = admin_settings.PAGE_SIZE
    max_page_size = admin_settings.MAX_PAGE_SIZE

    django_paginator_class = DjangoPaginator

    invalid_page_message = _("Invalid page.")

    def get_page_size(self, request):
        try:
            return _positive_int(
                request.data["size"], strict=True, cutoff=self.max_page_size
            )
        except (KeyError, ValueError):
            pass

    def paginate_queryset(self, queryset, request, view=None):  # pragma: no cover
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.data.get("page", 1)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):  # pragma: no cover
        return make_response(
            OrderedDict(
                [
                    (
                        "pagination",
                        OrderedDict(
                            [
                                ("size", self.page.paginator.per_page),
                                ("page", self.page.number),
                                ("total", self.page.paginator.object_list.count()),
                            ]
                        ),
                    ),
                    ("list", data),
                ]
            )
        )

    def get_results(self, data):
        return data["results"]
