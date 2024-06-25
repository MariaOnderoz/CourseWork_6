from django.forms import ModelForm

from blog.models import Blog


class BlogForm(ModelForm):
    """Форма редактирования блога"""
    class Meta:
        model = Blog
        fields = ('title', 'content',)
