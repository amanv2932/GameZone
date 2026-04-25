from django.test import TestCase
from django.urls import reverse


class PageViewTests(TestCase):
    def _login(self):
        return self.client.post(
            reverse("login"),
            {"userid": "aman", "password": "123"},
        )

    def test_all_protected_pages_render_after_login(self):
        self._login()
        pages = {
            "home": "home.html",
            "aboutus": "aboutus.html",
            "gallery": "gallery.html",
            "blog": "blog.html",
            "contactus": "contactus.html",
        }

        for name, template in pages.items():
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)

    def test_login_page_renders_without_auth(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_protected_pages_redirect_to_login_when_logged_out(self):
        protected_pages = ["home", "aboutus", "gallery", "blog", "contactus"]
        for page_name in protected_pages:
            with self.subTest(page=page_name):
                response = self.client.get(reverse(page_name))
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, reverse("login"))

    def test_contact_page_is_frontend_only(self):
        self._login()
        response = self.client.get(reverse("contactus"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="contact-name"')
        self.assertContains(response, 'id="contact-email"')
        self.assertContains(response, 'id="contact-message"')

    def test_login_accepts_only_aman_and_123(self):
        valid_response = self.client.post(
            reverse("login"),
            {"userid": "aman", "password": "123"},
            follow=True,
        )
        self.assertEqual(valid_response.status_code, 200)
        self.assertTemplateUsed(valid_response, "home.html")

        self.client.get(reverse("logout"))
        invalid_response = self.client.post(
            reverse("login"),
            {"userid": "aman", "password": "wrong"},
        )
        self.assertEqual(invalid_response.status_code, 200)
        self.assertContains(invalid_response, "Invalid credentials")

    def test_logout_clears_session_and_redirects_to_login(self):
        self._login()
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))

        protected_response = self.client.get(reverse("home"))
        self.assertEqual(protected_response.status_code, 302)
        self.assertEqual(protected_response.url, reverse("login"))
