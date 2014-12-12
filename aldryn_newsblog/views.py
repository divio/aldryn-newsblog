from django.views.generic import View
from django.http import HttpResponse
import reversion

from .models import Article


class ArticleDetail(View):
    def get(self, request, slug):
        return HttpResponse(Article.objects.get(slug=slug).title)


class ArticleList(View):
    def get(self, request):
        return HttpResponse('\n'.join(
            article.title for article in Article.objects.all()))


class AuthorArticleList(ArticleList):
    """A list of articles written by a specific author."""
    def get(self, request, author):
        return HttpResponse('\n'.join(
            article.title for article
            in Article.objects.filter(author=author_person)))


class CategoryArticleList(ArticleList):
    """A list of articles filtered by categories."""


class DateRangeArticleList(ArticleList):
    """A list of articles for a specific date range"""
