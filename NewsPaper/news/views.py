from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post
from .filters import PostFilter
from .forms import NewsForm
from django.urls import reverse_lazy



class NewsList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'news.html'
    context_object_name = 'all_news'
    paginate_by = 10

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации
        # self.request.GET содержит объект QueryDict
        # Сохраняем фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список постов
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post_detail'


# представление для создания поста/НОВОСТИ
class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        news_post = form.save(commit=False)
        news_post.postType = 'NW'
        return super().form_valid(form)


# представление для редактирования поста/НОВОСТИ
class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.change_post',)


# представление для удаления поста/НОВОСТИ
class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


# представление для создания поста/СТАТЬИ
class ArticleCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        news_post = form.save(commit=False)
        news_post.postType = 'AR'
        return super().form_valid(form)


# представление для редактирования поста/СТАТЬИ
class ArticleUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.change_post',)


# представление для удаления поста/СТАТЬИ
class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


# Представление для страницы с поиском постов
class SearchList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'search.html'
    context_object_name = 'found_news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context