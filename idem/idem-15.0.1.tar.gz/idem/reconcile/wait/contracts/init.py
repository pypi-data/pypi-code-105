def sig_get(hub, **kwargs):
    """
    Validate the signature of the reconcile.wait get function
    """
    ...


def post_get(self, hub):
    """
    Conform the return value of every reconcile.wait get()
    """
    try:
        assert isinstance(hub.ret, int)
    except KeyError:
        hub.log.error("reconcile.wait plugins wait functions should return integers")
