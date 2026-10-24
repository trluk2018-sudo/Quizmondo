import os
import unittest
from itsdangerous import URLSafeTimedSerializer
from app import create_app
from app.models import db, User, Post, Page, Category, MenuItem, SidebarWidget, SiteSetting, PageModule


class QuizmondoTestCase(unittest.TestCase):
    def setUp(self):
        self.sso_secret = 'test-sso-secret-xyz123'
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'WTF_CSRF_ENABLED': False,
            'SECRET_KEY': 'test-secret-key',
            'APP_SSO_SECRET': self.sso_secret,
        })
        self.client = self.app.test_client()

    def test_01_public_pages(self):
        """Verify all primary public endpoints render successfully in Quizmondo."""
        routes = ['/', '/posts', '/about', '/contact', '/category/science-cosmos']
        for r in routes:
            res = self.client.get(r)
            self.assertEqual(res.status_code, 200, f"Route {r} failed with status {res.status_code}")
            self.assertIn(b'Quizmondo', res.data)

    def test_02_post_detail(self):
        """Verify post detail page renders with astronomy/trivia lore."""
        res = self.client.get('/posts/which-planet-has-the-most-moons-saturn-jupiter')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Which Planet Has the Most Moons?', res.data)
        self.assertIn(b'146 confirmed satellites', res.data)

    def test_03_login_and_admin(self):
        """Verify standard admin authentication."""
        res = self.client.get('/admin/', follow_redirects=True)
        self.assertIn(b'Log In', res.data)

        res = self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Dashboard', res.data)
        self.assertIn(b'Quizmondo', res.data)

    def test_04_cross_instance_sso(self):
        """Verify SaaS Control Plane cross-instance SSO token verification."""
        serializer = URLSafeTimedSerializer(self.sso_secret, salt='cross-instance-sso')
        token = serializer.dumps({'u': 'platform_admin', 'ret': 'http://control.saas.local/control/'})

        res = self.client.get(f'/sso?token={token}', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'SaaS Support Mode:', res.data)
        self.assertIn(b'Return to Control Centre', res.data)
        self.assertIn(b'platform_admin', res.data)

        # Profile accessible
        res = self.client.get('/admin/profile')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Admin Profile', res.data)

    def test_05_interactive_daily_quiz_component(self):
        """Verify interactive JavaScript trivia challenge renders on homepage."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'DAILY BRAIN CHALLENGE', res.data)
        self.assertIn(b'Which planet in our solar system has the highest number of confirmed moons?', res.data)
        self.assertIn(b'Jupiter', res.data)
        self.assertIn(b'Saturn', res.data)
        self.assertIn(b'submitQuizOption', res.data)

    def test_06_sitemap_xml(self):
        """Verify XML sitemap generation."""
        res = self.client.get('/sitemap.xml')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/xml; charset=utf-8')
        self.assertIn(b'urlset', res.data)
        self.assertIn(b'/posts/which-planet-has-the-most-moons-saturn-jupiter', res.data)

    def test_07_admin_modules_and_ordering(self):
        """Verify admin modular homepage layout manager."""
        self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'})
        res = self.client.get('/admin/appearance/layout')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Home Page Layout and Sections', res.data)


if __name__ == '__main__':
    unittest.main()
