import pytest
from sample_backend_refactored import find_users

def test_find_users_by_name():
    result = find_users("Mac", "") 
    assert result == { 
        'users_list' :
        [
            {  
                'id' : 'xyz789',
                'name' : 'Mac',
                'job': 'Professor',
            }
        ]
    }

    #check these https://changhsinlee.com/pytest-mock/
    # https://pypi.org/project/pytest-mock/
    # https://github.com/mongomock/mongomock (more promisable)

    #Integration testing with Postoman: https://learning.postman.com/docs/running-collections/using-newman-cli/command-line-integration-with-newman/