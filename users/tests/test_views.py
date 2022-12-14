from django.http import HttpResponse

from .test_base import UserBaseTestCase


class UserViewTestCase(UserBaseTestCase):

    def test_if_new_user_can_create_an_account(self) -> None:
        response: HttpResponse = self.make_new_user()

        self.assertEqual(response.status_code, 201)

    def test_if_new_user_try_to_get_your_data_without_access_token_returns_404(self) -> None:  # noqa: E501
        self.make_new_user()

        response: HttpResponse = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_if_user_can_get_your_data_with_your_access_token(self) -> None:  # noqa: E501
        self.get_user_authenticated()

        response: HttpResponse = self.client.get(
            self.url, HTTP_AUTHORIZATION=self.auth_token
        )
        self.assertEqual(response.status_code, 200)

    def test_if_a_new_user_can_get_an_access_token(self) -> None:

        self.make_new_user()

        response_token: HttpResponse = self.get_user_token(
            email=self.user_data['email'],
            password=self.user_data['password']
        )

        self.assertEqual(response_token.status_code, 200)

    def if_do_not_logged_user_try_to_update_your_data_returns_404(self) -> None:  # noqa: E501
        new_user_data: dict[str, str] = {
            'username': 'userNotLogged'
        }
        response: HttpResponse = self.client.put(
            self.url, data=new_user_data,
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 404)

    def test_if_logged_user_can_do_a_partial_update(self) -> None:
        self.get_user_authenticated()

        new_user_data: dict[str, str] = {
            'username': 'OtherUserName',
        }
        response: HttpResponse = self.client.patch(
            self.url, data=new_user_data, HTTP_AUTHORIZATION=self.auth_token,
            content_type=self.content_type
        )

        self.assertEqual(response.status_code, 200)

    def test_if_logged_user_can_do_a_full_update(self) -> None:
        self.get_user_authenticated()

        new_user_data: dict[str, str] = {
            'username': 'MyUserFTest',
            'email': 'userEmail123@email.com',
            'first_name': 'MyFirstName',
            'last_name': 'MyLastName',
            'password': '22@22#22',
        }
        response: HttpResponse = self.client.put(
            self.url, data=new_user_data, HTTP_AUTHORIZATION=self.auth_token,
            content_type=self.content_type
        )
        new_user_data.pop('password')

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), new_user_data)

    def test_if_do_not_logged_user_try_to_delete_returns_404(self) -> None:

        self.make_new_user()

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 404)

    def test_if_logged_user_can_delete_your_account(self) -> None:
        self.get_user_authenticated()

        response = self.client.delete(
            self.url,
            HTTP_AUTHORIZATION=self.auth_token
        )
        self.assertEqual(response.status_code, 204)
