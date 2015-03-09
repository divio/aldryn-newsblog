# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool

from aldryn_newsblog.models import Article


@toolbar_pool.register
class NewsBlogToolbar(CMSToolbar):
    watch_models = (Article, )
    supported_apps = ('aldryn_newsblog',)

    def populate(self):
        if not (self.is_current_app and self.request.user.has_perm(
                'aldryn_newsblog.add_article')):
            return

        menu = self.toolbar.get_or_create_menu('newsblog-app', _('News Blog'))
        menu.add_modal_item(_('Add Article'), reverse('admin:aldryn_newsblog_article_add'))

        article = getattr(self.request, 'article', None)
        if article and self.request.user.has_perm(
                'aldryn_newsblog.change_article'):
            menu.add_modal_item(_('Edit Article'),
                                reverse('admin:aldryn_newsblog_article_change',
                                        args=(article.pk,)),
                                active=True
            )
