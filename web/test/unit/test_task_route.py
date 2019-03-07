from unittest import TestCase
from flaskr import app
from unittest.mock import patch
from test.unit.test_utils import TestUtils


class TestTaskRoute(TestCase):

    def setUp(self):
        app.testing = True
        self.app = app
        self.test_client = app.test_client()

        self.add_route = '/task/add'

    @patch('services.task_service.insert')
    @patch('services.task_service.is_registered')
    def test_add_new_task(self, mocked_task_service_is_registered, mocked_task_service_insert):
        """
        It should return 201 when a new task is created
        """

        mocked_task_service_is_registered.return_value = False

        response = self.test_client.post(self.add_route,
                                         json=TestUtils.valid_task)
        response_json = response.get_json()

        self.assertTrue(mocked_task_service_insert.called)
        self.assertEqual(response_json['Message'], 'Task created')
        self.assertEqual(201, response.status_code)
