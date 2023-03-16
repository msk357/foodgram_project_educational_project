from django.forms import ModelForm
from django.forms.widgets import TextInput

from recipes.models import Tag


class TagForm(ModelForm):
    """Форма для тэгов.
    Добавлен стандартный виджет для выбора цвета.
    """
    class Meta:
        model = Tag
        fields = ("name", "slug", "color")
        widgets = {
            "color": TextInput(attrs={"type": "color"}),
        }
