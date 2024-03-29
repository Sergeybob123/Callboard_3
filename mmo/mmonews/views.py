from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, TemplateView

from .filters import ResponseFilter, MyResponseFilter
from .forms import PostForm, ResponseForm
from .mixins import AuthorRequiredMixin, AuthorNecessaryMixin
from .models import Post, User, Response



class HomeView(TemplateView):
    template_name = 'flatpages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostsListView(ListView):
    model = Post
    ordering = '-datetime_post'
    template_name = 'mmonews/posts.html'
    context_object_name = 'posts'
    paginate_by = 5



class PostDetailView(DetailView):
    model = Post
    template_name = 'mmonews/post.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'mmonews/post_create.html'
    context_object_name = 'post'



    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def add_post(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post_item = form.save(commit=False)
                post_item.save()
                return redirect('/')
            else:
                form = PostForm()
            return render(request, 'mmonews/post_create.html', {'form': form})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    model_search = Post
    template_name = 'mmonews/post_edit.html'
    form_class = PostForm


    def get_object(self, **kwargs):
        my_id = self.kwargs.get('pk')
        return Post.objects.get(pk=my_id)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    model_search = Post
    template_name = 'mmonews/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'



class PersonalAccountView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'account/personal_account.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        context['user'] = User.objects.get(id=user_id)
        return context


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    model_search = Post
    form_class = ResponseForm
    template_name = 'mmonews/response_create.html'
    context_object_name = 'response'

    def form_valid(self, form):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)

        response = form.save(commit=False)
        response.post = post
        response.author = self.request.user
        response.save()

        return super().form_valid(form)


class ResponseDetailView(DetailView):
    model = Response
    template_name = 'mmonews/response.html'
    context_object_name = 'response'


class ResponseUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Response
    model_search = Response
    template_name = 'mmonews/response_edit.html'
    form_class = ResponseForm



    def get_object(self, **kwargs):
        my_id = self.kwargs.get('pk')
        return Response.objects.get(pk=my_id)


class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'mmonews/response_delete.html'
    queryset = Response.objects.all()
    success_url = '/search_response/'


class ResponsesSearchView(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-datetime_response'
    template_name = 'mmonews/response_search.html'
    context_object_name = 'responses'
    paginate_by = 5


    def get_queryset(self):
        queryset = super().get_queryset().filter(post__author__user=self.request.user)
        self.queryset = ResponseFilter(self.request.GET, queryset=queryset)
        return self.queryset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.queryset
        return context


class MyResponsesSearchView(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-datetime_response'
    template_name = 'mmonews/response_my_search.html'
    context_object_name = 'responses'
    paginate_by = 5


    def get_queryset(self):
        queryset = super().get_queryset().filter(author=self.request.user)
        self.queryset = MyResponseFilter(self.request.GET, queryset=queryset)
        return self.queryset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.queryset
        return context


@login_required
def response_accept(request, response_id):
    response = get_object_or_404(Response, id=response_id)

    if not response.accept:
        response.accept = True
        response.save()

    return redirect(f'/response/{response_id}/')

