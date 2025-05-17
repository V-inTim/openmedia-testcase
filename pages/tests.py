import json

from django.test import TestCase, Client
from django.urls import reverse

from .models import Page


class PageViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.page1 = Page.objects.create(
            url="https://example1.com",
            h1_count=1,
            h2_count=2,
            h3_count=3,
            a_links=["link1"]
        )
        self.page2 = Page.objects.create(
            url="https://example2.com",
            h1_count=3,
            h2_count=2,
            h3_count=1,
            a_links=["link2"]
        )

    def test_missing_url(self):
        response = self.client.post(reverse('create_page'))
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.content))

    def test_parse_wrong_method(self):
        response = self.client.get(reverse('create_page'))
        self.assertEqual(response.status_code, 405)

    def test_success_get_oage(self):
        response = self.client.get(reverse('get_page', args=[self.page1.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['h1'], self.page1.h1_count)
        self.assertEqual(data['h2'], self.page1.h2_count)
        self.assertEqual(data['h3'], self.page1.h3_count)
        self.assertEqual(data['a'], self.page1.a_links)

    def test_get_page_not_found(self):
        response = self.client.get(reverse('get_page', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_get_page_wrong_method(self):
        response = self.client.post(reverse('get_page', args=[self.page1.id]))
        self.assertEqual(response.status_code, 405)

    def test_success_get_all(self):
        response = self.client.get(reverse('get_page_list'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['h1'], self.page1.h1_count)
        self.assertEqual(data[1]['h1'], self.page2.h1_count)

    def test_get_all_h1(self):
        response = self.client.get(reverse('get_page_list') + '?order=-h1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]['h1'], self.page1.h1_count)
        self.assertEqual(data[1]['h1'], self.page2.h1_count)

    def test_get_all_invalid_order(self):
        response = self.client.get(reverse('get_page_list') + '?order=invalid')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.content))

    def test_get_all_wrong_method(self):
        response = self.client.post(reverse('get_page_list'))
        self.assertEqual(response.status_code, 405)
