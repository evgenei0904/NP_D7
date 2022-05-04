from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, User
from .filters import NewsFilter
from .forms import PostForm, AuthorForm, SubscribeForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string


class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(categoryType='NW')
    ordering = 'dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class NewsSearch(ListView):
    model = Post
    queryset = Post.objects.filter(categoryType='NW')
    ordering = 'dateCreation'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    permission_required = ('news.add_post',)
    # success_url = '/news/<int:pk>'
    #
    # html_content = render_to_string('new_send.html')
    # msg = EmailMultiAlternatives(
    #     subject=f'{PostForm} {Post.dateCreation}',
    #     body=Post.text,  # это то же, что и message
    #     from_email='vintazh-m',
    #     to=['evgenei0904@gmail.com'],  # это то же, что и recipients_list
    # )
    # msg.attach_alternative(html_content, "text/html")  # добавляем html
    #
    # msg.send()


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_update.html'
    permission_required = ('news.change_post',)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.delete_post',)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'author_update.html'
    form_class = AuthorForm

    def get_object(self, **kwargs):
        return self.request.user


class CategoryList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'category.html'
    context_object_name = 'category'
    paginate_by = 10


class Subscribe (UpdateView):
    template_name = 'subscribe.html'
    queryset = Category.objects.all()
    success_url = '/news/'


@login_required
def add_subscribe(request, pk):
    a = request.user
    # a.save()
    b = Category.objects.get(id=pk)
    b.subscribers.add(a)
    return redirect('/news/')
