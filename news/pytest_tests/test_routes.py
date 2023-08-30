from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize('name, news_object',
                         (('news:home', None),
                          ('users:login', None),
                          ('users:logout', None),
                          ('users:signup', None),
                          ('news:detail', pytest.lazy_fixture('news')),))
def test_pages_availability_for_anonymous_user(client, name, news_object):
    if news_object is None:
        url = reverse(name)
    else:
        url = reverse(name, args=(news_object.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    # parametrized_client - название параметра,
    # в который будут передаваться фикстуры;
    # Параметр expected_status - ожидаемый статус ответа.
    'parametrized_client, expected_status',
    # В кортеже с кортежами передаём значения для параметров:
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize('name', (
    'news:delete', 'news:edit'
))
def test_edit_delete_comment_availability_for_author(
        parametrized_client, expected_status,
        comment, news, name):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize('name', (
    'news:delete', 'news:edit'
))
def test_redirect_for_anonymous(comment, client, news, name):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
