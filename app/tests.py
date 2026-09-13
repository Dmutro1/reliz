from django.contrib.auth.models import User as AuthUser
from django.test import TestCase
from django.urls import reverse

from .models import Comment, Mod


class SiteFlowTests(TestCase):
    def setUp(self):
        self.user = AuthUser.objects.create_user(
            username='testuser',
            password='StrongTestPass123!',
        )
        self.mod = Mod.objects.create(
            title='Test Mod',
            slug='test-mod',
            summary='A test mod for request flow tests.',
            game_version='1.21.1',
        )

    def test_homepage_shows_one_featured_mod(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['mods']), 1)
        self.assertContains(response, 'Test Mod')

    def test_mod_list_is_paginated(self):
        for index in range(12):
            Mod.objects.create(
                title=f'Extra Mod {index}',
                slug=f'extra-mod-{index}',
            )

        response = self.client.get(reverse('mods_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 2)
        self.assertEqual(len(response.context['page_obj']), 12)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))

        self.assertRedirects(response, '/login/?next=/profile/')

    def test_logout_clears_authenticated_session(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_authenticated_user_can_comment_on_mod(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('mod_detail', kwargs={'slug': self.mod.slug}),
            {'text': 'This mod works well.'},
        )

        self.assertRedirects(response, reverse('mod_detail', kwargs={'slug': self.mod.slug}))
        self.assertTrue(
            Comment.objects.filter(
                mod=self.mod,
                user=self.user,
                text='This mod works well.',
            ).exists()
        )

    def test_mod_detail_increments_view_count(self):
        self.assertEqual(self.mod.views, 0)

        response = self.client.get(
            reverse('mod_detail', kwargs={'slug': self.mod.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.mod.refresh_from_db()
        self.assertEqual(self.mod.views, 1)