from django.core.urlresolvers import resolve
from django.views.generic import View, ListView
from django.http import HttpResponse

import reversion

from .models import Article


class NamespaceView(View):
    def dispatch(self, request, *args, **kwargs):
        self.current_app = resolve(self.request.path).namespace
        return super(NamespaceView, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['current_app'] = self.current_app
        return super(NamespaceView, self).render_to_response(
            context, **response_kwargs)


class ArticleDetail(NamespaceView):
    def get(self, request, slug):
        return HttpResponse(Article.objects.get(
            slug=slug, namespace=self.current_app).title)


class ArticleList(NamespaceView, ListView):
    def get(self, request):
        return HttpResponse('\n'.join(
            article.title for article in Article.objects.all()))


class AuthorArticleList(ArticleList):
    """A list of articles written by a specific author."""
    def get(self, request, author):
        return HttpResponse('\n'.join(
            article.title for article
            in Article.objects.filter(author__slug=author)))


class CategoryArticleList(ArticleList):
    """A list of articles filtered by categories."""
    def get(self, request, category):
        return HttpResponse('\n'.join(
            article.title for article
            in Article.objects.filter(category=category)))


class DateRangeArticleList(ArticleList):
    """A list of articles for a specific date range"""
