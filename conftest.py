import pytest
from news.models import News, Comment
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
import time
@pytest.fixture
def author(django_user_model):
    author = django_user_model.objects.create(username='author')
    return author

@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client

@pytest.fixture
def news():
    news = News.objects.create(title='title',
                               text='text')
    return news

@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(news=news, author=author, text='text')
    return comment


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            # Для каждой новости уменьшаем дату на index дней от today,
            # где index - счётчик цикла.
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)

@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def id_for_args(news):
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return news.id,


@pytest.fixture
def comments_sorted_by_date(news, author):
    today = datetime.today()
    comments_sorted_by_date = [
        Comment(
            news_id=news.id, author_id=author.id, text=f'Tекст {index}', created=today - timedelta(days=index)
        )
        for index in range(3)
    ]
    Comment.objects.bulk_create(comments_sorted_by_date)
    return comments_sorted_by_date


@pytest.fixture
def form_comment_data():
    return {
        'text': 'text'
    }

