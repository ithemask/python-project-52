from django.contrib.auth.models import User
from django.test import TestCase


class UserCreationTestCase(TestCase):
    fixtures = ['user.json']
    create_url = '/users/create/'
    redirect_url = '/login/'

    def test_get_request(self):
        response = self.client.get(self.create_url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_default_creation(self):
        response = self.client.post(
            self.create_url,
            {
                'first_name': 'Jaime',
                'last_name': 'Lannister',
                'username': 'kingslayer',
                'password1': '333',
                'password2': '333',
            },
            follow=True,
        )

        self.assertRedirects(response, self.redirect_url)
        self.assertContains(response, 'Account has been successfully created')
        self.assertTrue(User.objects.filter(username='kingslayer').exists())

    def test_creating_with_occupied_username(self):
        response = self.client.post(
            self.create_url,
            {
                'first_name': 'Jaime',
                'last_name': 'Lannister',
                'username': 'littlefinger',
                'password1': '333',
                'password2': '333',
            },
        )

        self.assertFormError(
            response.context['form'],
            'username',
            'A user with that username already exists.',
        )
        self.assertEqual(
            User.objects.filter(username='littlefinger').count(),
            1,
        )

    def test_creating_with_invalid_username(self):
        response = self.client.post(
            self.create_url,
            {
                'first_name': 'Jaime',
                'last_name': 'Lannister',
                'username': 'king$layer',
                'password1': '333',
                'password2': '333',
            },
        )

        self.assertFormError(
            response.context['form'],
            'username',
            'Enter a valid username. This value may contain only letters, '
            'numbers, and @/./+/-/_ characters.',
        )
        self.assertEqual(User.objects.all().count(), 2)

    def test_creating_with_weak_password(self):
        response = self.client.post(
            self.create_url,
            {
                'first_name': 'Jaime',
                'last_name': 'Lannister',
                'username': 'kingslayer',
                'password1': '33',
                'password2': '33',
            },
        )

        self.assertFormError(
            response.context['form'],
            'password2',
            'This password is too short. '
            'It must contain at least 3 characters.',
        )
        self.assertEqual(User.objects.all().count(), 2)

    def test_password_confirmation_failure(self):
        response = self.client.post(
            self.create_url,
            {
                'first_name': 'Jaime',
                'last_name': 'Lannister',
                'username': 'kingslayer',
                'password1': '333',
                'password2': '3333',
            },
        )

        self.assertFormError(
            response.context['form'],
            'password2',
            'The two password fields didn’t match.',
        )
        self.assertEqual(User.objects.all().count(), 2)


class UserUpdatingTestCase(TestCase):
    fixtures = ['user.json']

    def test_updating_without_logging_in(self):
        update_url = '/users/1/update/'
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'

        get_response = self.client.get(update_url, follow=True)
        post_response = self.client.post(
            update_url,
            {
                'first_name': 'Petyr',
                'last_name': 'Baelish',
                'username': 'lord_of_the_seven_kingdoms',
                'password1': '1111',
                'password2': '1111',
            },
            follow=True,
        )

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertTrue(User.objects.filter(username='littlefinger').exists())

    def test_updating_another_user(self):
        update_url = '/users/2/update/'
        redirect_url = '/users/'
        error_message = 'You have no permission to edit another user.'

        self.client.login(username='littlefinger', password='111')
        get_response = self.client.get(update_url, follow=True)
        post_response = self.client.post(
            update_url,
            {
                'first_name': 'Sandor',
                'last_name': 'Clegane',
                'username': 'dog',
                'password1': '000',
                'password2': '000',
            },
            follow=True,
        )

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertTrue(User.objects.filter(username='hound').exists())

    def test_default_updating(self):
        update_url = '/users/1/update/'
        user = User.objects.get(id=1)

        self.client.login(username='littlefinger', password='111')
        get_response = self.client.get(update_url, follow=True)
        post_response = self.client.post(
            update_url,
            {
                'first_name': 'Petyr',
                'last_name': 'Baelish',
                'username': 'lord_of_the_seven_kingdoms',
                'password1': '1111',
                'password2': '1111',
            },
            follow=True,
        )

        updated_user = User.objects.get(id=1)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/users/')
        self.assertContains(
            post_response,
            'Account has been successfully updated',
        )
        self.assertNotEqual(user.username, updated_user.username)
        self.assertNotEqual(user.password, updated_user.password)

    def test_updating_with_occupied_username(self):
        self.client.login(username='littlefinger', password='111')
        response = self.client.post(
            '/users/1/update/',
            {
                'first_name': 'Petyr',
                'last_name': 'Baelish',
                'username': 'hound',
                'password1': '111',
                'password2': '111',
            },
        )

        self.assertFormError(
            response.context['form'],
            'username',
            'A user with that username already exists.',
        )
        self.assertEqual(User.objects.get(id=1).username, 'littlefinger')


class UserDeletionTestCase(TestCase):
    fixtures = ['user.json']

    def test_deleting_without_logging_in(self):
        delete_url = '/users/2/delete/'
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'

        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertTrue(User.objects.filter(username='hound').exists())

    def test_deleting_another_user(self):
        delete_url = '/users/1/delete/'
        redirect_url = '/users/'
        error_message = 'You have no permission to edit another user.'

        self.client.login(username='hound', password='222')
        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertTrue(User.objects.filter(username='littlefinger').exists())

    def test_default_deletion(self):
        delete_url = '/users/2/delete/'

        self.client.login(username='hound', password='222')
        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/users/')
        self.assertContains(
            post_response,
            'Account has been successfully deleted',
        )
        self.assertFalse(User.objects.filter(username='hound').exists())
