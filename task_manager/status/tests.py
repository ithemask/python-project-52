from django.test import TestCase

from task_manager.status.models import Status


class StatusCreationTestCase(TestCase):
    fixtures = ['user.json']
    create_url = '/statuses/create/'

    def test_creating_status_without_logging_in(self):
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'

        get_response = self.client.get(self.create_url, follow=True)
        post_response = self.client.post(
            self.create_url,
            {'name': 'new'},
            follow=True,
        )

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertFalse(Status.objects.filter(name='new').exists())

    def test_default_status_creation(self):
        self.client.login(
            username='lord_of_the_seven_kingdoms',
            password='j1s8',
        )
        get_response = self.client.get(self.create_url, follow=True)
        post_response = self.client.post(
            self.create_url,
            {'name': 'new'},
            follow=True,
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/statuses/')
        self.assertContains(
            post_response,
            'Status has been successfully created',
        )
        self.assertTrue(Status.objects.filter(name='new').exists())

    def test_creating_status_with_occupied_name(self):
        Status.objects.create(name='new')

        self.client.login(
            username='lord_of_the_seven_kingdoms',
            password='j1s8',
        )
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

    def test_creating_status_with_too_long_name(self):
        self.client.login(
            username='lord_of_the_seven_kingdoms',
            password='j1s8',
        )
        response = self.client.post(
            self.create_url,
            {'name': 'very very very very very very very very very very new'},
            follow=True,
        )

        self.assertFormError(
            response.context['form'],
            'name',
            'Name is too long. Maximum length is 50 characters.',
        )
        self.assertFalse(
            Status.objects.filter(name='very very very very very very '
                                       'very very very very new').exists()
        )


class StatusViewingTestCase(TestCase):
    fixtures = ['user.json', 'status.json']
    list_url = '/statuses/'

    def test_viewing_status_list_without_logging_in(self):
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'

        response = self.client.get(self.list_url, follow=True)

        self.assertRedirects(response, redirect_url)
        self.assertContains(response, error_message)

    def test_default_status_list_viewing(self):
        self.client.login(username='quiet_wolf', password='a8v3')
        response = self.client.get(self.list_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['status_list'],
            Status.objects.all().order_by('id'),
        )


class StatusUpdatingTestCase(TestCase):
    fixtures = ['user.json', 'status.json']
    update_url = '/statuses/4/update/'

    def test_updating_status_without_logging_in(self):
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'
        status = Status.objects.get(id=4)

        get_response = self.client.get(self.update_url, follow=True)
        post_response = self.client.post(
            self.update_url,
            {'name': 'on hold'},
            follow=True,
        )

        updated_status = Status.objects.get(id=4)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertEqual(status, updated_status)

    def test_default_status_updating(self):
        self.client.login(username='brienne_the_beauty', password='s6p4')
        get_response = self.client.get(self.update_url, follow=True)
        post_response = self.client.post(
            self.update_url,
            {'name': 'on hold'},
            follow=True,
        )

        updated_status = Status.objects.get(id=4)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/statuses/')
        self.assertContains(
            post_response,
            'Status has been successfully updated',
        )
        self.assertEqual(updated_status.name, 'on hold')


class StatusDeletingTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'label.json', 'task.json']

    def test_deleting_status_without_logging_in(self):
        delete_url = '/statuses/2/delete/'
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'

        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertTrue(Status.objects.filter(name='in progress').exists())

    def test_default_status_deletion(self):
        delete_url = '/statuses/2/delete/'

        self.client.login(username='dragonmother', password='u5t7')
        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/statuses/')
        self.assertContains(
            post_response,
            'Status has been successfully deleted',
        )
        self.assertFalse(Status.objects.filter(name='in progress').exists())

    def test_deleting_bound_status(self):
        delete_url = '/statuses/1/delete/'

        self.client.login(username='dragonmother', password='u5t7')
        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/statuses/')
        self.assertContains(
            post_response,
            'Status cannot be deleted because it is being used',
        )
        self.assertTrue(Status.objects.filter(name='new').exists())
