from unittest import TestCase
from app import app
from models import db, User, Post
from datetime import datetime

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User")
        post = Post(
            title="Test Post",
            content="This is a test post.",
            created_at=datetime.utcnow(),
            user=self.user,
        )
        db.session.add(user)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.user = user
        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users_index(self):
        """Test that users index page displays."""

        with self.client as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)

    def test_users_new(self):
        """Test adding a new user."""

        with self.client as client:
            d = {"first_name": "New", "last_name": "User", "image_url": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("New User", html)

    def test_users_show(self):
        """Test showing a user."""

        with self.client as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)

    def test_users_update(self):
        """Test updating a user."""

        with self.client as client:
            d = {"first_name": "Updated", "last_name": "User", "image_url": ""}
            resp = client.post(
                f"/users/{self.user_id}/edit", data=d, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Updated User", html)

    def test_users_delete(self):
        """Test deleting a user."""

        with self.client as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test User", html)

    def test_posts_new_form(self):
        """Test the posts_new_form route"""
        response = self.client.get(f"/users/{self.user.id}/posts/new")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"New Post", response.data)

    def test_posts_new(self):
        """Test the posts_new route"""
        data = {"title": "Test Post 2", "content": "This is another test post."}
        response = self.client.post(
            f"/users/{self.user.id}/posts/new", data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Post 2", response.data)

    def test_posts_show(self):
        """Test the posts_show route"""
        response = self.client.get(f"/posts/{self.post.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Post", response.data)

    def test_posts_edit(self):
        """Test the posts_edit route"""
        response = self.client.get(f"/posts/{self.post.id}/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit Post", response.data)

    def test_posts_update(self):
        """Test the posts_update route"""
        data = {"title": "Updated Post", "content": "This post has been updated."}
        response = self.client.post(
            f"/posts/{self.post.id}/edit", data=data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Updated Post", response.data)

    def test_posts_destroy(self):
        """Test the posts_destroy route"""
        response = self.client.post(
            f"/posts/{self.post.id}/delete", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Test Post", response.data)
