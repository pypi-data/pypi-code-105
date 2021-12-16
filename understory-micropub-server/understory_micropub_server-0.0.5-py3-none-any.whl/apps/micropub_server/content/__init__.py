""""""

from understory import web
from understory.web import tx

app = web.application(
    __name__,
    args={
        "year": r"\d{4}",
        "month": r"\d{2}",
        "day": r"\d{2}",
        "post": web.nb60_re + r"{,4}",
        "slug": r"[\w_-]+",
    },
)


@app.control(r"")
class Homepage:
    """Your primary feed."""

    def get(self):
        """"""
        # resource = tx.m.pub.read(tx.request.uri.path)["resource"]
        # if resource["visibility"] == "private" and not tx.user.session:
        #     raise web.Unauthorized(f"/auth?return_to={tx.request.uri.path}")
        # # mentions = web.indie.webmention.get_mentions(str(tx.request.uri))
        # return templates.content.entry(resource)  # , mentions)
        try:
            posts = tx.m.pub.get_posts()
        except AttributeError:
            posts = []
        return app.view.homepage(posts)


@app.control(r"{year}")
class Year:
    """All posts from given year."""

    def get(self):
        """"""


@app.control(r"{year}/{month}")
class Month:
    """All posts from given month."""

    def get(self):
        """"""


@app.control(r"{year}/{month}/{day}")
class Day:
    """All posts from given day."""

    def get(self):
        """"""


@app.control(r"{year}/{month}/{day}/{post}(/{slug})?")
class Permalink:
    """An individual entry."""

    def get(self):
        """"""
        try:
            resource = tx.m.pub.read(tx.request.uri.path)["resource"]
        except micropub.server.PostNotFoundError:
            web.header("Content-Type", "text/html")  # TODO FIXME XXX
            raise web.NotFound(templates.post_not_found())
        if resource["visibility"] == "private" and not tx.user.session:
            raise web.Unauthorized(f"/auth?return_to={tx.request.uri.path}")
        # mentions = web.indie.webmention.get_mentions(str(tx.request.uri))
        return app.view.entry(resource)  # , mentions)
