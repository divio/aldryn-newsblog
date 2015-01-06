import unittest
import random
import string
from datetime import datetime
from random import randint

import six
from cms import api
from cms.utils import get_cms_setting
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase
from django.core.urlresolvers import reverse
from django.db import transaction
from django.utils.translation import activate
from aldryn_people.models import Person
import reversion

from aldryn_newsblog.models import Article


def rand_str(prefix='', length=23, chars=string.ascii_letters):
    return prefix + ''.join(random.choice(chars) for _ in range(length))


class NewsBlogTestsMixin(object):
    def create_person(self):
        user = User.objects.create(
            username=rand_str(), first_name=rand_str(), last_name=rand_str())
        person = Person.objects.create(user=user, slug=rand_str())
        return person

    def create_article(self, **kwargs):
        try:
            author = kwargs['author']
        except KeyError:
            author = self.create_person()

        fields = {
            'title': rand_str(),
            'slug': rand_str(),
            'author': author,
            'owner': author.user,
            'namespace': 'NewsBlog',
            'publishing_date': datetime.now()
        }

        fields.update(kwargs)

        return Article.objects.create(**fields)

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.page = api.create_page(
            'page', self.template, self.language, published=True,
            apphook='NewsBlogApp', apphook_namespace='NewsBlog')
        self.page.publish('en')
        self.placeholder = self.page.placeholders.all()[0]

        for language, _ in settings.LANGUAGES[1:]:
            api.create_title(language, 'page', self.page)
            self.page.publish(language)


class TestAldrynNewsBlog(NewsBlogTestsMixin, TestCase):

    def test_create_post(self):
        title = rand_str()
        author = self.create_person()
        article = Article.objects.create(
            title=title, slug=rand_str(), author=author, owner=author.user,
            namespace='NewsBlog', publishing_date=datetime.now())
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title)

    def test_delete_post(self):
        title = rand_str()
        slug = rand_str()
        author = self.create_person()
        article = Article.objects.create(
            title=title, slug=slug, author=author, owner=author.user,
            namespace='NewsBlog', publishing_date=datetime.now())
        article_url = article.get_absolute_url()
        response = self.client.get(article_url)
        self.assertContains(response, title)
        Article.objects.get(slug=slug).delete()
        response = self.client.get(article_url)
        self.assertEqual(response.status_code, 404)

    def test_articles_by_author(self):
        author1, author2 = self.create_person(), self.create_person()
        for author in (author1, author2):
            articles = [
                Article.objects.create(
                    title=rand_str(), slug=rand_str(), namespace='NewsBlog',
                    author=author, owner=author.user,
                    publishing_date=datetime.now())
                for _ in range(10)]
            response = self.client.get(reverse(
                'aldryn_newsblog:article-list-by-author',
                kwargs={'author': author.slug}))
            for article in articles:
                self.assertContains(response, article.title)

    def test_articles_by_category(self):
        author = self.create_person()
        category1, category2 = rand_str(), rand_str()
        for category in (category1, category2):
            articles = [
                Article.objects.create(
                    title=rand_str(), slug=rand_str(), namespace='NewsBlog',
                    author=author, owner=author.user, category=category,
                    publishing_date=datetime.now())
                for _ in range(10)]
            response = self.client.get(reverse(
                'aldryn_newsblog:article-list-by-category',
                kwargs={'category': category}))
            for article in articles:
                self.assertContains(response, article.title)

    def test_articles_by_date(self):
        author = self.create_person()
        in_articles = [
            Article.objects.create(
                title=rand_str(), slug=rand_str(), namespace='NewsBlog',
                author=author, owner=author.user,
                publishing_date=datetime(1914, 7, 28,
                                         randint(0, 23), randint(0, 59)))
            for _ in range(10)]
        out_articles = [
            Article.objects.create(
                title=rand_str(), slug=rand_str(), namespace='NewsBlog',
                author=author, owner=author.user,
                publishing_date=datetime(1939, 9, 1,
                                         randint(0, 23), randint(0, 59)))
            for _ in range(10)]
        response = self.client.get(reverse(
            'aldryn_newsblog:article-list-by-day',
            kwargs={'year': '1914', 'month': '07', 'day': '28'}))
        for article in out_articles:
            self.assertNotContains(response, article.title)
        for article in in_articles:
            self.assertContains(response, article.title)

    def test_articles_by_month(self):
        author = self.create_person()
        in_articles = [
            Article.objects.create(
                title=rand_str(), slug=rand_str(), namespace='NewsBlog',
                author=author, owner=author.user,
                publishing_date=datetime(1914, 7, randint(1, 31),
                                         randint(0, 23), randint(0, 59)))
            for _ in range(10)]
        out_articles = [
            Article.objects.create(
                title=rand_str(), slug=rand_str(), namespace='NewsBlog',
                author=author, owner=author.user,
                publishing_date=datetime(1939, 9, 1,
                                         randint(0, 23), randint(0, 59)))
            for _ in range(10)]
        response = self.client.get(reverse(
            'aldryn_newsblog:article-list-by-month',
            kwargs={'year': '1914', 'month': '07'}))
        for article in out_articles:
            self.assertNotContains(response, article.title)
        for article in in_articles:
            self.assertContains(response, article.title)

    def test_articles_by_year(self):
        author = self.create_person()
        in_articles = [
            Article.objects.create(
                title=rand_str(), slug=rand_str(), namespace='NewsBlog',
                author=author, owner=author.user,
                publishing_date=datetime(1914, randint(1, 12), randint(1, 28),
                                         randint(0, 23), randint(0, 59)))
            for _ in range(10)]
        out_articles = [
            Article.objects.create(
                title=rand_str(), slug=rand_str(), namespace='NewsBlog',
                author=author, owner=author.user,
                publishing_date=datetime(1939, randint(1, 12), randint(1, 28),
                                         randint(0, 23), randint(0, 59)))
            for _ in range(10)]
        response = self.client.get(reverse(
            'aldryn_newsblog:article-list-by-year', kwargs={'year': '1914'}))
        for article in out_articles:
            self.assertNotContains(response, article.title)
        for article in in_articles:
            self.assertContains(response, article.title)

    def test_has_content(self):
        title = rand_str()
        content = rand_str()
        author = self.create_person()
        article = Article.objects.create(
            title=title, slug=rand_str(), author=author, owner=author.user,
            namespace='NewsBlog', publishing_date=datetime.now())
        api.add_plugin(article.content, 'TextPlugin', self.language)
        plugin = article.content.get_plugins()[0].get_plugin_instance()[0]
        plugin.body = content
        plugin.save()
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title)
        self.assertContains(response, content)


class TestVersioning(NewsBlogTestsMixin, TransactionTestCase):
    def create_revision(self, article, **kwargs):
        with transaction.atomic(), reversion.create_revision():
            for k, v in six.iteritems(kwargs):
                setattr(article, k, v)
            article.save()

    def revert_to(self, article, revision):
        reversion.get_for_object(article)[revision].revision.revert()

    def test_revert_revision(self):
        title1 = rand_str(prefix='title1_')
        title2 = rand_str(prefix='title2_')

        article = self.create_article()

        # Revision 1
        self.create_revision(article, title=title1)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1)

        # Revision 2
        self.create_revision(article, title=title2)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title2)

        # Revert to revision 1
        self.revert_to(article, 1)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1)

    def test_revert_translated_revision(self):
        title1_en = rand_str(prefix='title1_en_')
        title1_de = rand_str(prefix='title1_de_')
        title2_en = rand_str(prefix='title2_en_')
        title2_de = rand_str(prefix='title2_de_')

        article = self.create_article()

        # Revision 1
        article.set_current_language('en')
        self.create_revision(article, title=title1_en)

        article.set_current_language('de')
        self.create_revision(article, title=title1_de)

        activate('en')
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1_en)

        activate('de')
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1_de)

        # Revision 2a (modify just EN)
        article.set_current_language('en')
        self.create_revision(article, title=title2_en)

        activate('en')
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title2_en)

        activate('de')
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1_de)

        # Revision 2b (modify just DE)
        article.set_current_language('de')
        self.create_revision(article, title=title2_de)

        activate('en')
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title2_en)

        activate('de')
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title2_de)

        # Revert to revision 2a (EN=2, DE=1)
        self.revert_to(article, 1)

        activate('en')
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title2_en)

        activate('de')
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1_de)

        # Revert to revision 1 (EN=1, DE=1)
        self.revert_to(article, 2)

        activate('en')
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1_en)

        activate('de')
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1_de)


if __name__ == '__main__':
    unittest.main()
