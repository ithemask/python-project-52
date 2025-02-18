from django.test import TestCase
from task_manager.models import Status


class StatusCreationTestCase(TestCase):
    fixtures = ['user.json', 'status.json']
    create_url = '/statuses/create/'

    def test_creating_without_logging_in(self):
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'

        get_response = self.client.get(self.create_url, follow=True)
        post_response = self.client.post(
            self.create_url,
            {'name': 'complete'},
            follow=True,
        )

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertFalse(Status.objects.filter(name='complete').exists())

    def test_default_creation(self):
        self.client.login(username='littlefinger', password='111')
        get_response = self.client.get(self.create_url, follow=True)
        post_response = self.client.post(
            self.create_url,
            {'name': 'complete'},
            follow=True,
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/statuses/')
        self.assertContains(
            post_response,
            'Status has been successfully created',
        )
        self.assertTrue(Status.objects.filter(name='complete').exists())

    def test_creating_with_occupied_name(self):
        self.client.login(username='littlefinger', password='111')
        response = self.client.post(
            self.create_url,
            {'name': 'new'},
            follow=True,
        )

        self.assertFormError(
            response.context['form'],
            'name',
            'Status with such name already exists.',
        )
        self.assertEqual(
            Status.objects.filter(name='new').count(),
            1,
        )

    def test_creating_with_too_long_name(self):
        self.client.login(username='littlefinger', password='111')
        response = self.client.post(
            self.create_url,
            {'name': 'very very very very very very very very very long name'},
            follow=True,
        )

        self.assertFormError(
            response.context['form'],
            'name',
            'Name is too long. Maximum length is 50 characters.',
        )
        self.assertEqual(
            Status.objects.all().count(),
            2,
        )


class StatusUpdatingTestCase(TestCase):
    fixtures = ['user.json', 'status.json']
    update_url = '/statuses/2/update/'

    def test_updating_without_logging_in(self):
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'

        get_response = self.client.get(self.update_url, follow=True)
        post_response = self.client.post(
            self.update_url,
            {'name': 'complete'},
            follow=True,
        )

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertEqual(Status.objects.get(id=2).name, 'in progress')

    def test_default_updating(self):
        status = Status.objects.get(id=2)

        self.client.login(username='littlefinger', password='111')
        get_response = self.client.get(self.update_url, follow=True)
        post_response = self.client.post(
            self.update_url,
            {'name': 'complete'},
            follow=True,
        )

        updated_status = Status.objects.get(id=2)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/statuses/')
        self.assertContains(
            post_response,
            'Status has been successfully updated',
        )
        self.assertNotEqual(status.name, updated_status.name)
