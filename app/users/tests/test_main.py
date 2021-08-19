import json
from fastapi import status


def test_all_users(test_app, test_get_headers):
    response = test_app.get('/user/all', headers=test_get_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()


def test_get_user(test_app, test_get_headers, test_get_data):
    response = test_app.get('/user/1', headers=test_get_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_get_data


def test_get_user_incorrect_id(test_app, test_get_headers):
    response = test_app.get('/user/0', headers=test_get_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_delete_user(test_app, test_get_headers):
    response = test_app.delete('/user/5/delete', headers=test_get_headers)
    assert response.status_code == status.HTTP_200_OK


def test_delete_user_incorrect_id(test_app, test_get_headers):
    response = test_app.get('/user/0', headers=test_get_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_update_user(test_app, test_get_headers, test_get_data_for_update):
    response = test_app.patch('/user/3/update', data=json.dumps(test_get_data_for_update), headers=test_get_headers)
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == test_get_data_for_update


def test_update_user_incorrect_id(test_app, test_get_headers):
    response = test_app.get('/user/0', headers=test_get_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_me(test_app, test_get_headers, test_get_data):
    response = test_app.get('/user/me/', headers=test_get_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_get_data


def test_get_me_incorrect_credentials(test_app, test_get_fake_headers):
    response = test_app.get('/user/me/', headers=test_get_fake_headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials"
