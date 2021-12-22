from django import template
from django.template.loader import render_to_string
from django.utils.html import strip_spaces_between_tags

register = template.Library()


@register.simple_tag
def render_empty_form_template(template_name, formset):
    """Transform formset.empty_form in template string"""
    template = render_to_string(template_name, {"form": formset.empty_form})
    return strip_spaces_between_tags(template)
