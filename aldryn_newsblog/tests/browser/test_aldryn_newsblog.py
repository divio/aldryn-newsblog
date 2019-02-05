from django.test import LiveServerTestCase

from selenium import webdriver


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_sees_an_empty_page_message(self):
        # visit the home page of the facts appplication
        self.browser.get(self.live_server_url)

        # the default title of the home page is "News"
        self.assertIn("News", self.browser.title)

        # the default h1 is also "News"
        h1_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("News", h1_text)

    def test_admin_user_can_login(self):
        # go to the admin
        self.browser.get("http://localhost:8000/admin")

        self.fail("finish the test")
