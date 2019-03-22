from unittest import TestCase
from todo_list.flask_app import create_app
from unittest.mock import patch
from test.unit import test_utils

from todo_list.services import task_messages
from todo_list.routes import urls


class TestTaskRoute(TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.test_client = self.app.test_client()

        route_prefix = '/task'

        self.add_route = route_prefix + urls.add_task
        self.get_by_name_route = route_prefix + urls.get_task_by_name + '/'
        self.get_by_status_route = route_prefix + urls.get_task_by_status + '/'
        self.get_all_route = route_prefix + urls.get_all_tasks
        self.update_route = route_prefix + urls.update_task + '/'
        self.delete_route = route_prefix + urls.delete_task + '/'

    """
    Add route tests
    """

    @patch('todo_list.repositories.task_repository.insert')
    @patch('todo_list.repositories.task_repository.is_registered')
    def test_add(self, mocked_task_repository_is_registered, mocked_task_repository_insert):
        """
        It should return 201 when a task is created
        """

        mocked_task_repository_is_registered.return_value = False

        response = self.test_client.post(self.add_route,
                                         json=test_utils.task_with_valid_body)
        response_json = response.get_json()

        self.assertTrue(mocked_task_repository_insert.called)
        self.assertEqual(response_json['Message'], task_messages.created)
        self.assertEqual(response.status_code, 201)

    @patch('todo_list.repositories.task_repository.insert')
    def test_add_invalid_body(self, mocked_task_repository_insert):
        """
        It should return 400 when trying to add a task with invalid body
        """

        response = self.test_client.post(self.add_route,
                                         json=test_utils.task_with_invalid_body)
        response_json = response.get_json()

        self.assertFalse(mocked_task_repository_insert.called)
        self.assertEqual(response_json['Message'], task_messages.incorrect_parameters)
        self.assertEqual(response.status_code, 400)

    @patch('todo_list.repositories.task_repository.insert')
    def test_add_invalid_status(self, mocked_task_repository_insert):
        """
        It should return 400 when trying to add a task with invalid status
        """

        response = self.test_client.post(self.add_route,
                                         json=test_utils.task_with_invalid_status)
        response_json = response.get_json()

        self.assertFalse(mocked_task_repository_insert.called)
        self.assertEqual(response_json['Message'], task_messages.invalid_status)
        self.assertEqual(response.status_code, 400)

    @patch('todo_list.repositories.task_repository.insert')
    @patch('todo_list.repositories.task_repository.is_registered')
    def test_add_duplicated(self, mocked_task_repository_is_registered, mocked_task_repository_insert):
        """
        It should return 400 when trying to add a task that already exists
        """

        mocked_task_repository_is_registered.return_value = True

        response = self.test_client.post(self.add_route,
                                         json=test_utils.task_with_valid_body)
        response_json = response.get_json()

        self.assertFalse(mocked_task_repository_insert.called)
        self.assertEqual(response_json['Message'], task_messages.duplicated)
        self.assertEqual(response.status_code, 400)

    @patch('todo_list.repositories.task_repository.insert')
    @patch('todo_list.repositories.task_repository.is_registered')
    def test_add_status_upper_case(self, mocked_task_repository_is_registered, mocked_task_repository_insert):
        """
        It should set status to lower case (.lower()) before saving the task
        """

        mocked_task_repository_is_registered.return_value = False

        response = self.test_client.post(self.add_route,
                                         json=test_utils.task_with_valid_body)

        task_used_by_mock = mocked_task_repository_insert.call_args[0][0]

        self.assertEqual(task_used_by_mock.status,
                         test_utils.task_with_status_upper_case['status'].lower())
        self.assertEqual(response.status_code, 201)

    """
    Get by name route tests
    """

    @patch('todo_list.repositories.task_repository.get_by_name')
    def test_get_by_name_existing(self, mocked_task_repository_get_by_name):
        """
        It should return 200 if the task exists
        """

        mocked_task_repository_get_by_name.return_value = test_utils.task_with_valid_body

        response = self.test_client.get(self.get_by_name_route + 'it_exists')
        response_json = response.get_json()

        self.assertTrue(mocked_task_repository_get_by_name.called)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['name'], test_utils.task_with_valid_body['name'])
        self.assertEqual(response_json['description'], test_utils.task_with_valid_body['description'])
        self.assertEqual(response_json['status'], test_utils.task_with_valid_body['status'])

    @patch('todo_list.repositories.task_repository.get_by_name')
    def test_get_by_name_not_exists(self, mocked_task_repository_get_by_name):
        """
        It should return 404 if the task does not exist
        """
        mocked_task_repository_get_by_name.return_value = None

        response = self.test_client.get(self.get_by_name_route + 'it_does_not_exist')
        response_json = response.get_json()

        self.assertTrue(mocked_task_repository_get_by_name.called)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['Message'], task_messages.not_found)

    """
    Get by status route tests
    """

    @patch('todo_list.repositories.task_repository.get_by_status')
    def test_get_by_status_existing(self, mocked_task_repository_get_by_status):
        """
        It should return 200 with a list
        """

        mocked_task_repository_get_by_status.return_value = [test_utils.task_with_valid_body]

        response = self.test_client.get(self.get_by_status_route + 'to_do')
        response_json = response.get_json()

        self.assertTrue(mocked_task_repository_get_by_status.called)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response_json, list))
        self.assertEqual(response_json[0], test_utils.task_with_valid_body)

    @patch('todo_list.repositories.task_repository.get_by_status')
    def test_get_by_status_invalid(self, mocked_task_repository_get_by_status):
        """
        It should return 400 if  the status is invalid
        """

        response = self.test_client.get(self.get_by_status_route + 'this_is_invalid')
        response_json = response.get_json()

        self.assertFalse(mocked_task_repository_get_by_status.called)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['Message'], task_messages.invalid_status)

    @patch('todo_list.repositories.task_repository.get_by_status')
    def test_get_by_status_upper_case(self, mocked_task_repository_get_by_status):
        """
        It should set status to lower case (.lower()) before returning tasks
        """

        response = self.test_client.get(self.get_by_status_route + 'TO_DO')

        status_used_by_mock = mocked_task_repository_get_by_status.call_args[0][0]

        self.assertEqual(status_used_by_mock, 'to_do')
        self.assertEqual(response.status_code, 200)

    @patch('todo_list.repositories.task_repository.get_by_status')
    def test_get_by_status_invalid_task(self, mocked_task_repository_get_by_status):
        """
        It should not return something that is not a Task
        """

        mocked_task_repository_get_by_status.return_value = [test_utils.task_with_valid_body,
                                                             test_utils.task_with_invalid_body]

        response = self.test_client.get(self.get_by_status_route + 'to_do')
        response_json = response.get_json()

        self.assertEqual(len(response_json), 1)
        self.assertEqual(response.status_code, 200)

    """
    Get all route tests
    """

    @patch('todo_list.repositories.task_repository.get_all')
    def test_get_all(self, mocked_task_repository_get_all):
        """
        It should return 200 with a list
        """

        mocked_task_repository_get_all.return_value = [test_utils.task_with_valid_body]

        response = self.test_client.get(self.get_all_route)
        response_json = response.get_json()

        self.assertTrue(mocked_task_repository_get_all.called)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response_json, list))
        self.assertEqual(response_json[0], test_utils.task_with_valid_body)

    @patch('todo_list.repositories.task_repository.get_all')
    def test_get_all_invalid_task(self, mocked_task_repository_get_all):
        """
        It should not return something that is not a Task
        """

        mocked_task_repository_get_all.return_value = [test_utils.task_with_valid_body,
                                                       test_utils.task_with_invalid_body]

        response = self.test_client.get(self.get_all_route)
        response_json = response.get_json()

        self.assertEqual(len(response_json), 1)
        self.assertEqual(response.status_code, 200)

    """
    Update route tests
    """

    @patch('todo_list.repositories.task_repository.is_registered')
    @patch('todo_list.repositories.task_repository.update')
    def test_update(self, mocked_task_repository_update, mocked_task_repository_is_registered):
        """
        It should return 200 and update the task
        """

        mocked_task_repository_is_registered.return_value = True

        response = self.test_client.put(self.update_route + test_utils.task_with_valid_body['name'],
                                        json=test_utils.task_with_valid_body)
        response_json = response.get_json()

        self.assertTrue(mocked_task_repository_update.called)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['Message'], task_messages.updated)

    @patch('todo_list.repositories.task_repository.is_registered')
    @patch('todo_list.repositories.task_repository.update')
    def test_update_not_found(self, mocked_task_repository_update, mocked_task_repository_is_registered):
        """
        It should return 404 if the task does not exist
        """

        mocked_task_repository_is_registered.return_value = False

        response = self.test_client.put(self.update_route + 'i_dont_exist',
                                        json=test_utils.task_with_valid_body)
        response_json = response.get_json()

        self.assertFalse(mocked_task_repository_update.called)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['Message'], task_messages.not_found)

    @patch('todo_list.repositories.task_repository.is_registered')
    @patch('todo_list.repositories.task_repository.update')
    def test_update_invalid_body(self, mocked_task_repository_update, mocked_task_repository_is_registered):
        """
        It should return 400 if the body is invalid
        """

        mocked_task_repository_is_registered.return_value = True

        response = self.test_client.put(self.update_route + 'i_have_an_invalid_body',
                                        json=test_utils.task_with_invalid_body)
        response_json = response.get_json()

        self.assertFalse(mocked_task_repository_update.called)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['Message'], task_messages.incorrect_parameters)

    @patch('todo_list.repositories.task_repository.is_registered')
    @patch('todo_list.repositories.task_repository.update')
    def test_update_invalid_status(self, mocked_task_repository_update, mocked_task_repository_is_registered):
        """
        It should return 400 if the status is invalid
        """

        mocked_task_repository_is_registered.return_value = True

        response = self.test_client.put(self.update_route + test_utils.task_with_invalid_status['name'],
                                        json=test_utils.task_with_invalid_status)
        response_json = response.get_json()

        self.assertFalse(mocked_task_repository_update.called)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['Message'], task_messages.invalid_status)

    @patch('todo_list.repositories.task_repository.is_registered')
    @patch('todo_list.repositories.task_repository.update')
    def test_update_duplicated(self, mocked_task_repository_update, mocked_task_repository_is_registered):
        """
        It should return 400 if there is a task with the new name
        """

        mocked_task_repository_is_registered.return_value = True

        response = self.test_client.put(self.update_route + test_utils.task_with_valid_body['name'] + '_new',
                                        json=test_utils.task_with_valid_body)
        response_json = response.get_json()

        self.assertFalse(mocked_task_repository_update.called)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['Message'], task_messages.duplicated)

    @patch('todo_list.repositories.task_repository.is_registered')
    @patch('todo_list.repositories.task_repository.update')
    def test_update_change_name(self, mocked_task_repository_update, mocked_task_repository_is_registered):
        """
        It should return 200 and update if there is not a task with the new name
        """

        # Returns True on first call and False on second one
        # Returns True when verifying if 'old_name' exists and returns False when verifying if new name exists
        mocked_task_repository_is_registered.side_effect = [True, False]

        response = self.test_client.put(self.update_route + 'old_name',
                                        json=test_utils.task_with_valid_body)
        response_json = response.get_json()

        self.assertTrue(mocked_task_repository_update.called)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['Message'], task_messages.updated)

    @patch('todo_list.repositories.task_repository.is_registered')
    @patch('todo_list.repositories.task_repository.update')
    def test_update_upper_case(self, mocked_task_repository_update, mocked_task_repository_is_registered):
        """
        It should set status to lower case (.lower()) before updating the task
        """

        mocked_task_repository_is_registered.return_value = True

        response = self.test_client.put(self.update_route + test_utils.task_with_valid_body['name'],
                                        json=test_utils.task_with_status_upper_case)

        task_used_by_mock = mocked_task_repository_update.call_args[0][1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(task_used_by_mock.status,
                         test_utils.task_with_status_upper_case['status'].lower())

    """
    Delete route tests
    """

    @patch('todo_list.repositories.task_repository.delete')
    @patch('todo_list.repositories.task_repository.is_registered')
    def test_delete(self, mocked_task_repository_is_registered, mocked_task_repository_delete):
        """
        It should return 200 and delete the task
        """

        mocked_task_repository_is_registered.return_value = True

        response = self.test_client.delete(self.delete_route + 'test_name')
        response_json = response.get_json()

        self.assertTrue(mocked_task_repository_delete.called)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['Message'], task_messages.deleted)

    @patch('todo_list.repositories.task_repository.delete')
    @patch('todo_list.repositories.task_repository.is_registered')
    def test_delete_not_found(self, mocked_task_repository_is_registered, mocked_task_repository_delete):
        """
        It should return 404 if the task does not exist
        """

        mocked_task_repository_is_registered.return_value = False

        response = self.test_client.delete(self.delete_route + 'test_task')
        response_json = response.get_json()

        self.assertFalse(mocked_task_repository_delete.called)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['Message'], task_messages.not_found)
