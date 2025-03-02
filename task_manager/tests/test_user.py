from django.test import TestCase
from task_manager.models import User


class UserCreationTestCase(TestCase):
    create_url = '/users/create/'
    redirect_url = '/login/'

    def test_user_creation_get_request(self):
        response = self.client.get(self.create_url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_default_user_creation(self):
        response = self.client.post(
            self.create_url,
            {
                'first_name': 'Viserys',
                'last_name': 'Targaryen',
                'username': 'beggar_king',
                'password1': 'i9o',
                'password2': 'i9o',
            },
            follow=True,
        )

        self.assertRedirects(response, self.redirect_url)
        self.assertContains(response, 'Account has been successfully created')
        self.assertTrue(User.objects.filter(username='beggar_king').exists())

    def test_creating_user_with_occupied_username(self):
        User.objects.create(
            first_name='Robert',
            last_name='Baratheon',
            username='lord_of_the_seven_kingdoms',
            password='j1s8',
        )

        response = self.client.post(
            self.create_url,
            {
                'first_name': 'Viserys',
                'last_name': 'Targaryen',
                'username': 'lord_of_the_seven_kingdoms',
                'password1': 'i9o',
                'password2': 'i9o',
            },
        )

        self.assertFormError(
            response.context['form'],
            'username',
            'A user with that username already exists.',
        )
        self.assertEqual(
            User.objects.filter(username='lord_of_the_seven_kingdoms').count(),
            1,
        )

    def test_creating_user_with_invalid_username(self):
        response = self.client.post(
            self.create_url,
            {
                'first_name': 'Viserys',
                'last_name': 'Targaryen',
                'username': 'lord_of_the_$even_kingdoms',
                'password1': 'i9o',
                'password2': 'i9o',
            },
        )

        self.assertFormError(
            response.context['form'],
            'username',
            'Enter a valid username. This value may contain only letters, '
            'numbers, and @/./+/-/_ characters.',
        )
        self.assertFalse(
            User.objects.filter(username='lord_of_the_$even_kingdoms').exists()
        )

    def test_creating_user_with_weak_password(self):
        response = self.client.post(
            self.create_url,
            {
                'first_name': 'Viserys',
                'last_name': 'Targaryen',
                'username': 'beggar_king',
                'password1': 'i9',
                'password2': 'i9',
            },
        )

        self.assertFormError(
            response.context['form'],
            'password2',
            'This password is too short. '
            'It must contain at least 3 characters.',
        )
        self.assertFalse(User.objects.filter(username='beggar_king').exists())

    def test_password_confirmation_failure(self):
        response = self.client.post(
            self.create_url,
            {
                'first_name': 'Viserys',
                'last_name': 'Targaryen',
                'username': 'beggar_king',
                'password1': 'i9o',
                'password2': 'i9p',
            },
        )

        self.assertFormError(
            response.context['form'],
            'password2',
            'The two password fields didn’t match.',
        )
        self.assertFalse(User.objects.filter(username='beggar_king').exists())


class UserViewingTestCase(TestCase):
    fixtures = ['user.json']
    list_url = '/users/'

    def test_viewing_user_list_without_logging_in(self):
        response = self.client.get(self.list_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['user_list'],
            User.objects.all().order_by('id'),
        )

    def test_default_user_list_viewing(self):
        self.client.login(username='quiet_wolf', password='a8v3')
        response = self.client.get(self.list_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['user_list'],
            User.objects.all().order_by('id'),
        )


class UserUpdatingTestCase(TestCase):
    fixtures = ['user.json']

    def test_updating_user_without_logging_in(self):
        update_url = '/users/1/update/'
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'
        user = User.objects.get(id=1)

        get_response = self.client.get(update_url, follow=True)
        post_response = self.client.post(
            update_url,
            {
                'first_name': 'Robert',
                'last_name': 'Baratheon',
                'username': 'usurper',
                'password1': 'q7d3',
                'password2': 'q7d3',
            },
            follow=True,
        )

        updated_user = User.objects.get(id=1)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertEqual(user, updated_user)

    def test_updating_another_user(self):
        update_url = '/users/1/update/'
        redirect_url = '/users/'
        error_message = 'You have no permission to edit another user.'
        user = User.objects.get(id=1)

        self.client.login(username='dragonmother', password='u5t7')
        get_response = self.client.get(update_url, follow=True)
        post_response = self.client.post(
            update_url,
            {
                'first_name': 'Robert',
                'last_name': 'Baratheon',
                'username': 'usurper',
                'password1': 'q7d3',
                'password2': 'q7d3',
            },
            follow=True,
        )

        updated_user = User.objects.get(id=1)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertEqual(user, updated_user)

    def test_default_user_updating(self):
        update_url = '/users/4/update/'
        user = User.objects.get(id=4)

        self.client.login(username='lord_snow', password='f6m0')
        get_response = self.client.get(update_url, follow=True)
        post_response = self.client.post(
            update_url,
            {
                'first_name': 'Jon',
                'last_name': 'Snow',
                'username': 'lord_commander',
                'password1': 'h5y8',
                'password2': 'h5y8',
            },
            follow=True,
        )

        updated_user = User.objects.get(id=4)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/users/')
        self.assertContains(
            post_response,
            'Account has been successfully updated',
        )
        self.assertEqual(updated_user.username, 'lord_commander')
        self.assertNotEqual(user.password, updated_user.password)

    def test_updating_user_with_occupied_username(self):
        user = User.objects.get(id=4)

        self.client.login(username='lord_snow', password='f6m0')
        response = self.client.post(
            '/users/4/update/',
            {
                'first_name': 'Jon',
                'last_name': 'Snow',
                'username': 'quiet_wolf',
                'password1': 'h5y8',
                'password2': 'h5y8',
            },
        )

        updated_user = User.objects.get(id=4)

        self.assertFormError(
            response.context['form'],
            'username',
            'A user with that username already exists.',
        )
        self.assertEqual(user, updated_user)


class UserDeletionTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'label.json', 'task.json']

    def test_deleting_user_without_logging_in(self):
        delete_url = '/users/1/delete/'
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'

        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertTrue(
            User.objects.filter(username='lord_of_the_seven_kingdoms').exists()
        )

    def test_deleting_another_user(self):
        delete_url = '/users/1/delete/'
        redirect_url = '/users/'
        error_message = 'You have no permission to edit another user.'

        self.client.login(username='dragonmother', password='u5t7')
        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertTrue(
            User.objects.filter(username='lord_of_the_seven_kingdoms').exists()
        )

    def test_default_user_deletion(self):
        delete_url = '/users/7/delete/'

        self.client.login(username='dragonmother', password='u5t7')
        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/users/')
        self.assertContains(
            post_response,
            'Account has been successfully deleted',
        )
        self.assertFalse(User.objects.filter(username='dragonmother').exists())

    def test_deleting_author(self):
        delete_url = '/users/5/delete/'

        self.client.login(username='halfman', password='b7z2')
        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/users/')
        self.assertContains(
            post_response,
            'User cannot be deleted because it is being used',
        )
        self.assertTrue(User.objects.filter(username='halfman').exists())

    def test_deleting_executor(self):
        delete_url = '/users/4/delete/'

        self.client.login(username='lord_snow', password='f6m0')
        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/users/')
        self.assertContains(
            post_response,
            'User cannot be deleted because it is being used',
        )
        self.assertTrue(User.objects.filter(username='lord_snow').exists())
