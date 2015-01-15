from django.conf.urls import patterns, url

from aldryn_newsblog.views import (
    ArticleDetail, ArticleList, AuthorArticleList, CategoryArticleList,
    YearArticleList, MonthArticleList, DayArticleList)

urlpatterns = patterns(
    '',
    url(r'^$',
        ArticleList.as_view(), name='article-list'),
    url(r'^(?P<year>[0-9]{4})/$',
        YearArticleList.as_view(), name='article-list-by-year'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$',
        MonthArticleList.as_view(), name='article-list-by-month'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})$',
        DayArticleList.as_view(), name='article-list-by-day'),
    url(r'^(?P<slug>\w[-\w]*)/$',
        ArticleDetail.as_view(), name='article-detail'),
    url(r'^author/(?P<author>\w[-\w]*)/$',
        AuthorArticleList.as_view(), name='article-list-by-author'),
    url(r'^category/(?P<category>\w[-\w]*)/$',
        CategoryArticleList.as_view(), name='article-list-by-category'),
)
