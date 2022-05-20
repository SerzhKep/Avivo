from string import Template
from django.utils.safestring import mark_safe
from django import forms

class PictureWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        html = Template("""<img src="$link"/>
                            <input type="file" name="image" accept="image/*" id="id_image">""")
        return mark_safe(html.substitute(link=value.url))