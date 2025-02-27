from django.test import TestCase
from task_manager.models import Task


class TaskCreationTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'label.json']
    create_url = '/tasks/create/'

    def test_creating_task_without_logging_in(self):
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'

        get_response = self.client.get(self.create_url, follow=True)
        post_response = self.client.post(
            self.create_url,
            {
                'name': 'Take over the office of Hand of the king',
                'status': 1,
                'executor': 2,
                'labels': [1, 3],
            },
            follow=True,
        )

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertFalse(
            Task.objects.filter(name='Take over the office of '
                                     'Hand of the king').exists()
        )

    def test_creating_task_with_no_description(self):
        self.client.login(
            username='lord_of_the_seven_kingdoms',
            password='j1s8',
        )
        get_response = self.client.get(self.create_url, follow=True)
        post_response = self.client.post(
            self.create_url,
            {
                'name': 'Take over the office of Hand of the king',
                'status': 1,
                'executor': 2,
                'labels': [1, 3],
            },
            follow=True,
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/tasks/')
        self.assertContains(
            post_response,
            'Task has been successfully created',
        )
        self.assertTrue(
            Task.objects.filter(name='Take over the office of '
                                     'Hand of the king').exists()
        )
        self.assertFalse(
            Task.objects.get(name='Take over the office of '
                                     'Hand of the king').description
        )

    def test_creating_task_with_no_executor(self):
        self.client.login(username='halfman', password='b7z2')
        get_response = self.client.get(self.create_url, follow=True)
        post_response = self.client.post(
            self.create_url,
            {
                'name': 'Fight for me in a trial by combat',
                'description': 'Fight as a champion in a trial by combat '
                               'against ser Gregor Clegane',
                'status': 1,
                'labels': [1, 3, 7],
            },
            follow=True,
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/tasks/')
        self.assertContains(
            post_response,
            'Task has been successfully created',
        )
        self.assertTrue(
            Task.objects.filter(name='Fight for me in a trial '
                                     'by combat').exists()
        )
        self.assertFalse(
            Task.objects.get(name='Fight for me in a trial '
                                  'by combat').executor
        )

    def test_creating_task_with_no_label(self):
        self.client.login(username='lady_stoneheart', password='n4x9')
        get_response = self.client.get(self.create_url, follow=True)
        post_response = self.client.post(
            self.create_url,
            {
                'name': 'Return Arya and Sansa to Riverrun',
                'description': 'Locate and escort my daughters '
                               'safely back to Riverrun',
                'status': 1,
                'executor': 8,
            },
            follow=True,
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/tasks/')
        self.assertContains(
            post_response,
            'Task has been successfully created',
        )
        self.assertTrue(
            Task.objects.filter(name='Return Arya and Sansa '
                                     'to Riverrun').exists()
        )
        self.assertFalse(
            Task.objects.get(name='Return Arya and Sansa '
                                  'to Riverrun').labels.all()
        )

    def test_task_author_auto_assignment(self):
        self.client.login(username='quiet_wolf', password='a8v3')
        get_response = self.client.get(self.create_url, follow=True)
        post_response = self.client.post(
            self.create_url,
            {
                'name': "Join the Night's Watch",
                'description': 'Depart for the Wall with Benjen Stark '
                               'and take the black',
                'status': 1,
                'executor': 4,
                'labels': [4, 6],
            },
            follow=True,
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/tasks/')
        self.assertContains(
            post_response,
            'Task has been successfully created',
        )
        self.assertEqual(
            Task.objects.get(name="Join the Night's Watch").author.username,
            'quiet_wolf',
        )

    def test_creating_task_with_occupied_name(self):
        Task.objects.create(
            name="Join the Night's Watch",
            status_id=3,
            executor_id=4,
        )

        self.client.login(username='halfman', password='b7z2')
        response = self.client.post(
            self.create_url,
            {
                'name': "Join the Night's Watch",
                'status': 1,
                'executor': 10,
            },
            follow=True,
        )

        self.assertFormError(
            response.context['form'],
            'name',
            'Task with such name already exists.',
        )
        self.assertEqual(
            Task.objects.filter(name="Join the Night's Watch").count(),
            1,
        )


class TaskUpdatingTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'label.json', 'task.json']
    update_url = '/tasks/5/update/'

    def test_updating_task_without_logging_in(self):
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'
        task = Task.objects.get(id=5)

        get_response = self.client.get(self.update_url, follow=True)
        post_response = self.client.post(
            self.update_url,
            {
                'name': 'Fight for me in a trial by combat',
                'description': 'Fight as a champion in a trial by combat '
                               'against ser Gregor Clegane',
                'status': 2,
                'executor': 9,
                'labels': [1, 3, 7],
            },
            follow=True,
        )

        updated_task = Task.objects.get(id=5)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertEqual(task, updated_task)

    def test_default_task_updating(self):
        self.client.login(username='red_viper', password='e0r8')
        get_response = self.client.get(self.update_url, follow=True)
        post_response = self.client.post(
            self.update_url,
            {
                'name': 'Fight for me in a trial by combat',
                'description': 'Fight as a champion in a trial by combat '
                               'against ser Gregor Clegane',
                'status': 2,
                'executor': 9,
                'labels': [1, 3, 7],
            },
            follow=True,
        )

        updated_task = Task.objects.get(id=5)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/tasks/')
        self.assertContains(
            post_response,
            'Task has been successfully updated',
        )
        self.assertEqual(updated_task.status.name, 'in progress')
        self.assertEqual(updated_task.executor.username, 'red_viper')


class TaskDeletingTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'label.json', 'task.json']
    delete_url = '/tasks/4/delete/'

    def test_deleting_task_without_logging_in(self):
        redirect_url = '/login/'
        error_message = \
            'You are not authorized! Please log in to your account.'

        get_response = self.client.get(self.delete_url, follow=True)
        post_response = self.client.post(self.delete_url, follow=True)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertTrue(
            Task.objects.filter(name='Return Arya and '
                                     'Sansa to Riverrun').exists()
        )

    def test_deleting_task_by_non_author(self):
        redirect_url = '/tasks/'
        error_message = 'Task can be deleted only by the author'

        self.client.login(username='brienne_the_beauty', password='s6p4')
        get_response = self.client.get(self.delete_url, follow=True)
        post_response = self.client.post(self.delete_url, follow=True)

        self.assertRedirects(get_response, redirect_url)
        self.assertContains(get_response, error_message)
        self.assertRedirects(post_response, redirect_url)
        self.assertContains(post_response, error_message)
        self.assertTrue(
            Task.objects.filter(name='Return Arya and '
                                     'Sansa to Riverrun').exists()
        )

    def test_default_task_deletion(self):
        self.client.login(username='lady_stoneheart', password='n4x9')
        get_response = self.client.get(self.delete_url, follow=True)
        post_response = self.client.post(self.delete_url, follow=True)

        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(post_response, '/tasks/')
        self.assertContains(
            post_response,
            'Task has been successfully deleted',
        )
        self.assertFalse(
            Task.objects.filter(name='Return Arya and '
                                     'Sansa to Riverrun').exists()
        )
