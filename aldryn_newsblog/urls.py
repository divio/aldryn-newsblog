from django.conf.urls import url

from aldryn_newsblog import views, feeds

urlpatterns = [
    url(r'^$',
        views.ArticleList.as_view(), name='article-list'),
    url(r'^feed/$', feeds.LatestArticlesFeed(), name='article-list-feed'),

    url(r'^search/$',
        views.ArticleSearchResultsList.as_view(), name='article-search'),

    url(r'^(?P<year>\d{4})/$',
        views.YearArticleList.as_view(), name='article-list-by-year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        views.MonthArticleList.as_view(), name='article-list-by-month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        views.DayArticleList.as_view(), name='article-list-by-day'),

    # Various permalink styles that we support
    # ----------------------------------------
    # This supports permalinks with <article_pk>
    # NOTE: We cannot support /year/month/pk, /year/pk, or /pk, since these
    # patterns collide with the list/archive views, which we'd prefer to
    # continue to support.
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pk>\d+)/$',
        views.ArticleDetail.as_view(), name='article-detail'),
    # These support permalinks with <article_slug>
    url(r'^(?P<slug>\w[-\w]*)/$',
        views.ArticleDetail.as_view(), name='article-detail'),
    url(r'^(?P<year>\d{4})/(?P<slug>\w[-\w]*)/$',
        views.ArticleDetail.as_view(), name='article-detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>\w[-\w]*)/$',
        views.ArticleDetail.as_view(), name='article-detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>\w[-\w]*)/$',  # flake8: NOQA
        views.ArticleDetail.as_view(), name='article-detail'),

    # Same links as above, but for ArticleDetailDraft
    url(r'^(?P<pk>\d+)/draft/$',
        views.ArticleDetailDraft.as_view(), name='article-detail-draft'),
    url(r'^(?P<pk>\d+)/draft/create/$',
        views.ArticleDetailDraft.as_view(create_draft=True), name='article-detail-draft-create'),
    url(r'^(?P<pk>\d+)/draft/publish/$',
        views.ArticleDetailDraft.as_view(publish=True), name='article-detail-draft-publish'),
    url(r'^(?P<pk>\d+)/draft/discard_draft/$',
        views.ArticleDetailDraft.as_view(discard_draft=True), name='article-detail-draft-discard'),
    # url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pk>\d+)/draft/$',
    #     views.ArticleDetailDraft.as_view(), name='article-detail-draft'),
    # # These support permalinks with <article_slug>
    # url(r'^(?P<slug>\w[-\w]*)/draft/$',
    #     views.ArticleDetailDraft.as_view(), name='article-detail-draft'),
    # url(r'^(?P<year>\d{4})/(?P<slug>\w[-\w]*)/draft/$',
    #     views.ArticleDetailDraft.as_view(), name='article-detail-draft'),
    # url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>\w[-\w]*)/draft/$',
    #     views.ArticleDetailDraft.as_view(), name='article-detail-draft'),
    # url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>\w[-\w]*)/draft/$',  # flake8: NOQA
    #     views.ArticleDetailDraft.as_view(), name='article-detail-draft'),


    url(r'^author/(?P<author>\w[-\w]*)/$',
        views.AuthorArticleList.as_view(), name='article-list-by-author'),

    url(r'^category/(?P<category>\w[-\w]*)/$',
        views.CategoryArticleList.as_view(), name='article-list-by-category'),
    url(r'^category/(?P<category>\w[-\w]*)/feed/$',
        feeds.CategoryFeed(), name='article-list-by-category-feed'),

    url(r'^tag/(?P<tag>\w[-\w]*)/$',
        views.TagArticleList.as_view(), name='article-list-by-tag'),
    url(r'^tag/(?P<tag>\w[-\w]*)/feed/$',
        feeds.TagFeed(), name='article-list-by-tag-feed'),

]
