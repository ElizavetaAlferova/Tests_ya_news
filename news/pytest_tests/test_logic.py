from http import HTTPStatus

import pytest
from django.urls import reverse
# Импортируем функции для проверки редиректа и ошибки формы:
from pytest_django.asserts import assertFormError, assertRedirects

# Импортируем из модуля forms сообщение об ошибке:
from news.forms import BAD_WORDS, WARNING
from news.models import Comment

# Дополнительно импортируем функцию slugify.
# from pytils.translit import slugify


# Указываем фикстуру form_data в параметрах теста.
@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        client, form_comment_data, id_for_args):
    url = reverse('news:detail', args=id_for_args)
    response = client.post(url, data=form_comment_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        author_client, form_comment_data,
        id_for_args, author, news):
    url = reverse('news:detail', args=id_for_args)
    response = author_client.post(url, data=form_comment_data)
    assertRedirects(response, f'{url}#comments')
    comment_count = Comment.objects.count()
    assert comment_count == 1
    comment = Comment.objects.get()
    assert comment.news == news
    assert comment.author == author
    assert comment.text == form_comment_data['text']


@pytest.mark.django_db
def test_user_cant_use_bad_words(id_for_args, author_client, author):
    bad_words_data = {'text': f'Text {BAD_WORDS[0]} djfhgdjhfg'}
    url = reverse('news:detail', args=id_for_args)
    response = author_client.post(url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=(WARNING))
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, news, comment, id_for_args):
    url = reverse('news:delete', args=(comment.id, ))
    response = author_client.delete(url)
    news_url = reverse('news:detail', args=id_for_args)
    url_to_comment = news_url + '#comments'
    print(url_to_comment)
    assertRedirects(response, url_to_comment)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_reader_cant_delete_comment(admin_client, comment):
    url = reverse('news:delete', args=(comment.id, ))
    response = admin_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_count = Comment.objects.count()
    assert comment_count == 1


def test_author_can_edit_comment(
        author_client, form_comment_data,
        comment, id_for_args):
    url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(url, data=form_comment_data)
    news_url = reverse('news:detail', args=id_for_args)
    url_to_comment = news_url + '#comments'
    assertRedirects(response, url_to_comment)
    comment.refresh_from_db()
    assert comment.text == form_comment_data['text']


def test_user_cant_edit_comment_of_another_user(
        admin_client, form_comment_data, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = admin_client.post(url, data=form_comment_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == form_comment_data['text']
