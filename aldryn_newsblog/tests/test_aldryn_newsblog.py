import unittest
import random
import string

from cms import api
from cms.utils import get_cms_setting
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from aldryn_people.models import Person

from aldryn_newsblog.models import Article


def rand_str():
    return ''.join(random.choice(string.ascii_letters) for _ in range(23))


class TestAldrynNewsBlog(TestCase):
    def create_person(self):
        user = User.objects.create(
            username=rand_str(), first_name=rand_str(), last_name=rand_str())
        person = Person.objects.create(user=user)
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
        article = Article.objects.create(
            title=title, slug=rand_str(), author=self.create_person())
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title)

    def test_delete_post(self):
        title = rand_str()
        slug = rand_str()
        article = Article.objects.create(
            title=title, slug=slug, author=self.create_person())
        article_url = article.get_absolute_url()
        response = self.client.get(article_url)
        self.assertContains(response, title)
        Article.objects.get(slug=slug).delete()
        with self.assertRaises(Article.DoesNotExist):
            response = self.client.get(article_url)

    def test_articles_by_author(self):
        author1 = self.create_person()
        author2 = self.create_person()
        author1_articles = [
            Article.objects.create(
                title=rand_str(), slug=rand_str(), author=author1)
            for _ in range(10)]
        author2_articles = [
            Article.objects.create(
                title=rand_str(), slug=rand_str(), author=author2)
            for _ in range(10)]


if __name__ == '__main__':
    unittest.main()
