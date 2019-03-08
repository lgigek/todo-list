class TestUtils:
    task_with_valid_body = {'name': 'test_name',
                            'description': 'test_description',
                            'status': 'to_do'}
    task_with_status_upper_case = {'name': 'test_name',
                                   'description': 'test_description',
                                   'status': 'TO_DO'}
    task_with_invalid_body = {'this_is': 'invalid'}
    task_with_invalid_status = {'name': 'test_name',
                                'description': 'test_description',
                                'status': 'this_is_invalid'}
