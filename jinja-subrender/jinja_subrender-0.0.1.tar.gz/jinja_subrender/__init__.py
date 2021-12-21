from flask import (
    Blueprint,
    render_template
)
from markupsafe import Markup

bp = Blueprint('jinja_subrender', __name__)

app = None


@bp.record
def Record(state):
    global app
    app = state.app

    @app.template_filter()
    def render(obj, templateName):
        """
        Render an object within a jinja template like

        {{ object | render('item.html') }}

        ^ the above says to render the 'object' using the jinja tempalte 'item.html'

        inside 'item.html' template, you can reference the object as obj

        for example:
            {{ obj['description'] }}

        :param obj: any python object
        :param templateName: str > jinja template to render the obj
        :return:
        """
        return Markup(render_template(templateName, obj=obj))
