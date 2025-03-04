from django.test import TestCase


class ErrorHandlingTestCase(TestCase):
    def test_400_handling(self):
        with self.settings(DEBUG=False):
            response = self.client.get('/bad-request/')
            self.assertEqual(response.status_code, 400)
            self.assertTemplateUsed(response, 'errors/400.html')

    def test_403_handling(self):
        with self.settings(DEBUG=False):
            response = self.client.get('/forbidden/')
            self.assertEqual(response.status_code, 403)
            self.assertTemplateUsed(response, 'errors/403.html')

    def test_404_handling(self):
        response = self.client.get('/non-existent/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')

    def test_500_handling(self):
        with self.settings(DEBUG=False):
            self.client.raise_request_exception = False
            response = self.client.get('/causes-500/')
            self.assertEqual(response.status_code, 500)
            self.assertTemplateUsed(response, 'errors/500.html')
