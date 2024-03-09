from django.shortcuts import get_object_or_404
from django.shortcuts import render


class AuthorRequiredMixin:


    def dispatch(self, request, *args, **kwargs):

        model = self.model_search
        post = get_object_or_404(model, pk=kwargs['pk'])
        if request.user.author != post.author:
            return permission_denied_view(request)
        return super().dispatch(request, *args, **kwargs)


class AuthorNecessaryMixin:

    def dispatch(self, request, *args, **kwargs):

        model = self.model_search
        post = get_object_or_404(model, pk=kwargs['pk'])
        if request.user.author == post.author:
            return refusal_to_edit_your_post_view(request)
        return super().dispatch(request, *args, **kwargs)


def permission_denied_view(request):
    return render(request, 'flatpages/permission_denied.html')


def refusal_to_edit_your_post_view(request):
    return render(request, 'flatpages/refusal_to_edit_your_post.html')