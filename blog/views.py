from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from blog.models import Blog
from pytils.translit import slugify


class BlogCreateView(CreateView):
    """Контроллер создания блога"""

    model = Blog
    fields = ("title", "content", "image")
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogListView(ListView):
    """Контроллер списка блогов"""

    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        blog = Blog.objects.all()

        context_data['object_list'] = blog
        context_data['title'] = 'Блог'

        return context_data


class BlogDetailView(DetailView):
    """Контроллер детального просмотра блога"""

    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    """Контроллер редактирования блога"""

    model = Blog
    fields = ("title", "content", "image")

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    """Контроллер удаления блога"""

    model = Blog
    success_url = reverse_lazy('blog:blog_list')


def toggle_publish(request, pk):
    """Функция изменения признака публикации блога"""

    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True

    blog_item.save()
    return redirect(reverse('blog:blog_list'))


