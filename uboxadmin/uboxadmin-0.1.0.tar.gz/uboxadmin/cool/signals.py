from django.dispatch import Signal

post_init = Signal(providing_args=["instance"])
