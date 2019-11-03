from django.test import TestCase
from django.urls import reverse


class TodayListViewTest(TestCase):
    def test_today_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_today_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_today_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'today.html')

    def test_today_view_is_paginated(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)


class YesterdayListViewTest(TestCase):
    def test_yesterday_view_url_exists_at_desired_location(self):
        response = self.client.get('/yesterday/')
        self.assertEqual(response.status_code, 200)

    def test_yesterday_view_url_accessible_by_name(self):
        response = self.client.get(reverse('yesterday-matches'))
        self.assertEqual(response.status_code, 200)

    def test_yesterday_view_uses_correct_template(self):
        response = self.client.get(reverse('yesterday-matches'))
        self.assertTemplateUsed(response, 'yesterday.html')

    def test_yesterday_view_is_paginated(self):
        response = self.client.get(reverse('yesterday-matches'))
        self.assertTrue('is_paginated' in response.context)


class TomorrowListViewTest(TestCase):
    def test_tomorrow_view_url_exists_at_desired_location(self):
        response = self.client.get('/tomorrow/')
        self.assertEqual(response.status_code, 200)

    def test_tomorrow_view_url_accessible_by_name(self):
        response = self.client.get(reverse('tomorrow-matches'))
        self.assertEqual(response.status_code, 200)

    def test_tomorrow_view_uses_correct_template(self):
        response = self.client.get(reverse('tomorrow-matches'))
        self.assertTemplateUsed(response, 'tomorrow.html')

    def test_tomorrow_view_is_paginated(self):
        response = self.client.get(reverse('tomorrow-matches'))
        self.assertTrue('is_paginated' in response.context)


class LiveListViewTest(TestCase):
    def test_live_view_url_exists_at_desired_location(self):
        response = self.client.get('/live/')
        self.assertEqual(response.status_code, 200)

    def test_live_view_url_accessible_by_name(self):
        response = self.client.get(reverse('live-matches'))
        self.assertEqual(response.status_code, 200)

    def test_live_view_uses_correct_template(self):
        response = self.client.get(reverse('live-matches'))
        self.assertTemplateUsed(response, 'live.html')

    def test_live_view_is_paginated(self):
        response = self.client.get(reverse('live-matches'))
        self.assertTrue('is_paginated' in response.context)


class HighlightsListViewTest(TestCase):
    def test_highlights_view_url_exists_at_desired_location(self):
        response = self.client.get('/highlights/')
        self.assertEqual(response.status_code, 200)

    def test_highlights_view_url_accessible_by_name(self):
        response = self.client.get(reverse('match-highlights'))
        self.assertEqual(response.status_code, 200)

    def test_highlights_view_uses_correct_template(self):
        response = self.client.get(reverse('match-highlights'))
        self.assertTemplateUsed(response, 'highlights.html')

    def test_highlights_view_is_paginated(self):
        response = self.client.get(reverse('match-highlights'))
        self.assertTrue('is_paginated' in response.context)
