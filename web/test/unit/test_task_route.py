from unittest import TestCase
from flaskr import app
from unittest.mock import patch
from test.unit.test_utils import TestUtils

from routes.task_messages import TaskMessages


class TestTaskRoute(TestCase):

    def setUp(self):
        app.testing = True
        self.app = app
        self.test_client = app.test_client()

        self.add_route = '/task/add'

    """
    Add route tests
    """

    @patch('services.task_service.insert')
    @patch('services.task_service.is_registered')
    def test_add_valid(self, mocked_task_service_is_registered, mocked_task_service_insert):
        """
        It should return 201 when a task is created
        """

        mocked_task_service_is_registered.return_value = False

        response = self.test_client.post(self.add_route,
                                         json=TestUtils.task_with_valid_body)
        response_json = response.get_json()

        self.assertTrue(mocked_task_service_insert.called)
        self.assertEqual(response_json['Message'], TaskMessages.created)
        self.assertEqual(201, response.status_code)

    @patch('services.task_service.insert')
    def test_add_invalid_body(self, mocked_task_service_insert):
        """
        It should return 400 when trying to add a task with invalid body
        """

        response = self.test_client.post(self.add_route,
                                         json=TestUtils.task_with_invalid_body)
        response_json = response.get_json()

        self.assertFalse(mocked_task_service_insert.called)
        self.assertEqual(response_json['Message'], TaskMessages.incorrect_parameters)
        self.assertEqual(400, response.status_code)

    @patch('services.task_service.insert')
    def test_add_invalid_status(self, mocked_task_service_insert):
        """
        It should return 400 when trying to add a task with invalid status
        """

        response = self.test_client.post(self.add_route,
                                         json=TestUtils.task_with_invalid_status)
        response_json = response.get_json()

        self.assertFalse(mocked_task_service_insert.called)
        self.assertEqual(response_json['Message'], TaskMessages.invalid_status)
        self.assertEqual(400, response.status_code)

    @patch('services.task_service.insert')
    @patch('services.task_service.is_registered')
    def test_add_duplicated(self, mocked_task_service_is_registered, mocked_task_service_insert):
        """
        It should return 400 when trying to add a task that already exists
        """

        mocked_task_service_is_registered.return_value = True

        response = self.test_client.post(self.add_route,
                                         json=TestUtils.task_with_valid_body)
        response_json = response.get_json()

        self.assertFalse(mocked_task_service_insert.called)
        self.assertEqual(response_json['Message'], TaskMessages.duplicated)
        self.assertEqual(400, response.status_code)
