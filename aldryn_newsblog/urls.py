from django.conf.urls import patterns, url

from aldryn_newsblog.views import (
    ArticleDetail, AuthorArticleList, CategoryArticleList,
    DateRangeArticleList)

urlpatterns = patterns(
    '',
    url(r'^(?P<slug>\w[-\w]*)/$', ArticleDetail.as_view(), name='article-detail'),
    url(r'^author/(?P<author>\w[-\w]*)/$', AuthorArticleList.as_view(),
        name='article-list-by-author'),
)
