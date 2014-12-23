import unittest
import random
import string
from datetime import datetime, timedelta
from random import randint

from cms import api
from cms.utils import get_cms_setting
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from aldryn_people.models import Person

from aldryn_newsblog.models import Article


def rand_str():
    return ''.join(random.choice(string.ascii_letters) for _ in range(23))


class TestAldrynNewsBlog(TestCase):
    def create_person(self):
        user = User.objects.create(
            username=rand_str(), first_name=rand_str(), last_name=rand_str())
        person = Person.objects.create(user=user, slug=rand_str())
        return person

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.page = api.create_page(
            'page', self.template, self.language, published=True,
            apphook='NewsBlogApp', apphook_namespace='NewsBlog')
        self.page.publish('en')
        self.placeholder = self.page.placeholders.all()[0]

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
        with self.assertRaises(Article.DoesNotExist):
            response = self.client.get(article_url)

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


if __name__ == '__main__':
    unittest.main()
