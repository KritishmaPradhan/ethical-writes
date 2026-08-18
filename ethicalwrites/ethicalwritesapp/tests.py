from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ethicalwritesapp.models import UserWork, WorkComment, WorkLike

User = get_user_model()


class WorkOwnershipAndCommunityInteractionTests(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(username='alice', email='alice@example.com', password='password123')
        self.user_b = User.objects.create_user(username='bob', email='bob@example.com', password='password123')
        self.work = UserWork.objects.create(
            user=self.user_a,
            username=self.user_a.username,
            title='The Last Page',
            author='Alice',
            freewriting='A quiet morning with a river and a promise.'
        )

    def test_only_owner_can_edit_or_delete_work(self):
        self.client.force_login(self.user_b)
        response = self.client.post(reverse('delete_work', args=[self.work.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserWork.objects.filter(pk=self.work.pk).exists())

        self.client.force_login(self.user_a)
        response = self.client.post(reverse('edit_work', args=[self.work.pk]), {
            'title': 'Updated Title',
            'author': 'Alice',
            'freewriting': 'Updated story text.'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.work.refresh_from_db()
        self.assertEqual(self.work.title, 'Updated Title')

        response = self.client.post(reverse('delete_work', args=[self.work.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(UserWork.objects.filter(pk=self.work.pk).exists())

    def test_other_users_can_like_and_comment_on_work(self):
        self.client.force_login(self.user_b)

        response = self.client.post(reverse('toggle_like', args=[self.work.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.work.total_likes, 1)

        response = self.client.post(reverse('add_comment', args=[self.work.pk]), {
            'text': 'Beautiful writing.'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.work.total_comments, 1)
        self.assertTrue(WorkComment.objects.filter(work=self.work, user=self.user_b, text='Beautiful writing.').exists())
        self.assertTrue(WorkLike.objects.filter(work=self.work, user=self.user_b).exists())
