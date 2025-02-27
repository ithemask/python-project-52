from django.test import TestCase
from task_manager.models import Label


class LabelCreationTestCase(TestCase):
    fixtures = ['user.json']
    create_url = '/labels/create/'

    def test_creating_label_without_logging_in(self):
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'

        get_response = self.client.get(self.create_url, follow=True)
        post_response = self.client.post(
            self.create_url,
            {'name': 'urgent'},
            follow=True,
        )

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertFalse(Label.objects.filter(name='urgent').exists())

    def test_default_label_creation(self):
        self.client.login(
            username='lord_of_the_seven_kingdoms',
            password='j1s8',
        )
        get_response = self.client.get(self.create_url, follow=True)
        post_response = self.client.post(
            self.create_url,
            {'name': 'urgent'},
            follow=True,
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/labels/')
        self.assertContains(
            post_response,
            'Label has been successfully created',
        )
        self.assertTrue(Label.objects.filter(name='urgent').exists())

    def test_creating_label_with_occupied_name(self):
        Label.objects.create(name='urgent')

        self.client.login(
            username='lord_of_the_seven_kingdoms',
            password='j1s8',
        )
        response = self.client.post(
            self.create_url,
            {'name': 'urgent'},
            follow=True,
        )

        self.assertFormError(
            response.context['form'],
            'name',
            'Label with such name already exists.',
        )
        self.assertEqual(
            Label.objects.filter(name='urgent').count(),
            1,
        )

    def test_creating_label_with_too_long_name(self):
        self.client.login(
            username='lord_of_the_seven_kingdoms',
            password='j1s8',
        )
        response = self.client.post(
            self.create_url,
            {'name': 'very very very very very very very very very urgent'},
            follow=True,
        )

        self.assertFormError(
            response.context['form'],
            'name',
            'Name is too long. Maximum length is 50 characters.',
        )
        self.assertFalse(
            Label.objects.filter(name='very very very very very very very '
                                       'very very urgent').exists()
        )


class LabelUpdatingTestCase(TestCase):
    fixtures = ['user.json', 'label.json']
    update_url = '/labels/7/update/'

    def test_updating_label_without_logging_in(self):
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'
        label = Label.objects.get(id=7)

        get_response = self.client.get(self.update_url, follow=True)
        post_response = self.client.post(
            self.update_url,
            {'name': 'extremely hard'},
            follow=True,
        )

        updated_label = Label.objects.get(id=7)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertEqual(label, updated_label)

    def test_default_label_updating(self):
        self.client.login(username='kingslayer', password='g4c3')
        get_response = self.client.get(self.update_url, follow=True)
        post_response = self.client.post(
            self.update_url,
            {'name': 'extremely hard'},
            follow=True,
        )

        updated_label = Label.objects.get(id=7)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/labels/')
        self.assertContains(
            post_response,
            'Label has been successfully updated',
        )
        self.assertEqual(updated_label.name, 'extremely hard')


class LabelDeletingTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'label.json', 'task.json']

    def test_deleting_label_without_logging_in(self):
        delete_url = '/labels/5/delete/'
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'

        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertTrue(Label.objects.filter(name='low priority').exists())

    def test_default_label_deletion(self):
        delete_url = '/labels/5/delete/'

        self.client.login(username='dragonmother', password='u5t7')
        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/labels/')
        self.assertContains(
            post_response,
            'Label has been successfully deleted',
        )
        self.assertFalse(Label.objects.filter(name='low priority').exists())

    def test_deleting_bound_label(self):
        delete_url = '/labels/1/delete/'

        self.client.login(username='dragonmother', password='u5t7')
        get_response = self.client.get(delete_url, follow=True)
        post_response = self.client.post(delete_url, follow=True)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/labels/')
        self.assertContains(
            post_response,
            'Label cannot be deleted because it is being used',
        )
        self.assertTrue(Label.objects.filter(name='urgent').exists())
