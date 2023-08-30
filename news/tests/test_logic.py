from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse
from news.forms import CommentForm
from news.models import Comment, News
from news.forms import BAD_WORDS, WARNING


User = get_user_model()

class TextCommentCreation(TestCase):
    COMMENT_TEXT = 'Текст комментария'

    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(title='title', text='text')
        cls.url = reverse('news:detail', args=(cls.news.id,))
        cls.user = User.objects.create(username='username')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        # Данные для POST-запроса при создании комментария.
        cls.form_data = {'text': cls.COMMENT_TEXT}

    def test_anonymous_user_cant_create_comment(self):
        # Совершаем запрос от анонимного клиента, в POST-запросе отправляем
        # предварительно подготовленные данные формы с текстом комментария.
        self.client.post(self.url, data=self.form_data)
        # Считаем количество комментариев.
        comments_count = Comment.objects.count()
        # Ожидаем, что комментариев в базе нет - сравниваем с нулём.
        self.assertEqual(comments_count, 0)

    def test_user_can_create_comment(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, f'{self.url}#comments')
        comments_count = Comment.objects.count()
        self.assertEqual(comments_count, 1)
        # Получаем объект комментария из базы.
        comment = Comment.objects.get()
        # Проверяем, что все атрибуты комментария совпадают с ожидаемыми.
        self.assertEqual(comment.text, self.COMMENT_TEXT)
        self.assertEqual(comment.news, self.news)
        self.assertEqual(comment.author, self.user)

    def test_user_cant_use_bad_words(self):
        bad_words_data = {'text': f'Text {BAD_WORDS[0]} djfhgdjhfg'}
        response = self.auth_client.post(self.url, data=bad_words_data)
        # Проверяем, есть ли в ответе ошибка формы.
        self.assertFormError(
            response,
            form='form',
            field='text',
            errors=WARNING
        )
        # Дополнительно убедимся, что комментарий не был создан.
        comments_count = Comment.objects.count()
        self.assertEqual(comments_count, 0)


    class TestCommentEditDelete(TestCase):
        # Тексты для комментариев не нужно дополнительно создавать
        # (в отличие от объектов в БД), им не нужны ссылки на self или cls,
        # поэтому их можно перечислить просто в атрибутах класса.
        COMMENT_TEXT = 'Текст комментария'
        NEW_COMMENT_TEXT = 'Обновлённый комментарий'

        @classmethod
        def setUpTestData(cls):
            cls.news = News.objects.create(title='title', text='text')
            news_url = reverse('news:detail', args=(cls.news.id,))
            cls.url_to_comment = news_url + '#comments'
            cls.author = User.objects.create(username='author')
            cls.author_client = Client()
            cls.author_client.force_login(cls.author)
            cls.reader = User.objects.create(username='reader')
            cls.reader_client = Client()
            cls.reader_client.force_login(cls.reader)
            cls.comment = Comment.objects.create(
                news = cls.news,
                author = cls.author,
                text = cls.COMMENT_TEXT
            )
            # URL для редактирования комментария.
            cls.edit_url = reverse('news:edit', args=(cls.comment.id,))
            # URL для удаления комментария.
            cls.delete_url = reverse('news:delete', args=(cls.comment.id,))
            # Формируем данные для POST-запроса по обновлению комментария.
            cls.form_data = {'text': cls.NEW_COMMENT_TEXT}

        def test_author_can_delete_comment(self):
            response = self.author_client.delete(self.delete_url)
            self.assertRedirects(response, self.url_to_comment)
            comments_count = Comment.objects.count()
            self.assertEqual(comments_count, 0)

        def test_reader_cant_delete_comment(self):
            response = self.reader_client.delete(self.delete_url)
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
            comment_count = Comment.objects.count()
            self.assertEqual(comment_count, 1)

        def test_author_can_edit_comment(self):
            response = self.author_client.post(self.edit_url, data=self.form_data)
            self.assertRedirects(response, self.url_to_comment)
            self.comment.refresh_from_db()
            self.assertEqual(self.comment.text, self.NEW_COMMENT_TEXT)

        def test_user_cant_edit_comment_of_another_user(self):
            response = self.reader_client.post(self.edit_url, data=self.form_data)
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
            self.comment.refresh_from_db()
            self.assertEqual(self.comment.text, self.COMMENT_TEXT)







