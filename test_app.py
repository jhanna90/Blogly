# from unittest import TestCase
# from app import app
# from models import db, User, Post, PostTag, Tag
# from datetime import datetime

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
# app.config["SQLALCHEMY_ECHO"] = False

# db.drop_all()
# db.create_all()


# class UserViewsTestCase(TestCase):
#     """Test views for users."""

#     def setUp(self):
#         """Add sample user."""

#         User.query.delete()

#         user = User(first_name="Test", last_name="User")
#         post = Post(
#             title="Test Post",
#             content="This is a test post.",
#             created_at=datetime.utcnow(),
#             user=self.user,
#         )
#         db.session.add(user)
#         db.session.add(post)
#         db.session.commit()

#         self.user_id = user.id
#         self.user = user
#         self.client = app.test_client()

#     def tearDown(self):
#         """Clean up any fouled transaction."""

#         db.session.rollback()

#     def test_users_index(self):
#         """Test that users index page displays."""

#         with self.client as client:
#             resp = client.get("/users")
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn("Test User", html)

#     def test_users_new(self):
#         """Test adding a new user."""

#         with self.client as client:
#             d = {"first_name": "New", "last_name": "User", "image_url": ""}
#             resp = client.post("/users/new", data=d, follow_redirects=True)
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn("New User", html)

#     def test_users_show(self):
#         """Test showing a user."""

#         with self.client as client:
#             resp = client.get(f"/users/{self.user_id}")
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn("Test User", html)

#     def test_users_update(self):
#         """Test updating a user."""

#         with self.client as client:
#             d = {"first_name": "Updated", "last_name": "User", "image_url": ""}
#             resp = client.post(
#                 f"/users/{self.user_id}/edit", data=d, follow_redirects=True
#             )
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn("Updated User", html)

#     def test_users_delete(self):
#         """Test deleting a user."""

#         with self.client as client:
#             resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertNotIn("Test User", html)

#     def test_posts_new_form(self):
#         """Test the posts_new_form route"""
#         response = self.client.get(f"/users/{self.user.id}/posts/new")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"New Post", response.data)

#     def test_posts_new(self):
#         """Test the posts_new route"""
#         data = {"title": "Test Post 2", "content": "This is another test post."}
#         response = self.client.post(
#             f"/users/{self.user.id}/posts/new", data=data, follow_redirects=True
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Test Post 2", response.data)

#     def test_posts_show(self):
#         """Test the posts_show route"""
#         response = self.client.get(f"/posts/{self.post.id}")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Test Post", response.data)

#     def test_posts_edit(self):
#         """Test the posts_edit route"""
#         response = self.client.get(f"/posts/{self.post.id}/edit")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Edit Post", response.data)

#     def test_posts_update(self):
#         """Test the posts_update route"""
#         data = {"title": "Updated Post", "content": "This post has been updated."}
#         response = self.client.post(
#             f"/posts/{self.post.id}/edit", data=data, follow_redirects=True
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Updated Post", response.data)

#     def test_posts_destroy(self):
#         """Test the posts_destroy route"""
#         response = self.client.post(
#             f"/posts/{self.post.id}/delete", follow_redirects=True
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertNotIn(b"Test Post", response.data)

from unittest import TestCase
from app import app, db
from models import User, Post, Tag, PostTag, connect_db


# Use test database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class FlaskTests(TestCase):
    """Test class for Blogly app"""

    def setUp(self):
        """Clean up any exists users and add a new user"""
        User.query.delete()
        Post.query.delete()
        Tag.query.delete()

        user = User(first_name="AAA", last_name="BBB", image_url="sample_url")
        db.session.add(user)
        db.session.commit()

        post = Post(user_id=user.id, title="test title", content="test content")
        db.session.add(post)
        db.session.commit()

        tag = Tag(name="tag test")
        db.session.add(tag)
        db.session.commit()

        post.tags.append(tag)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id
        self.tag_id = tag.id

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_users(self):
        """Testing the all users page"""
        with app.test_client() as client:
            res = client.get("/users")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("AAA BBB", html)

    def test_user(self):
        """Testing the user detail page"""
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("AAA BBB", html)
            self.assertIn("sample_url", html)
            self.assertIn("test title", html)

    def test_user_new(self):
        """Testing the add user form"""
        with app.test_client() as client:
            res = client.get(f"/users/new")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Create User", html)

    def test_user_new_post(self):
        """Testing the add user form handling"""
        with app.test_client() as client:
            res = client.post(
                f"/users/new",
                data={"first_name": "CCC", "last_name": "DDD", "image_url": "test_url"},
                follow_redirects=True,
            )
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("CCC DDD", html)

    def test_user_edit(self):
        """Testing the edit user form"""
        user = User.query.first()

        with app.test_client() as client:
            res = client.get(f"/users/{user.id}/edit")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Edit ", html)
            self.assertIn(user.first_name, html)
            self.assertIn(user.last_name, html)

    def test_user_edit_post(self):
        """Testing the update user handling"""
        user = User.query.first()
        with app.test_client() as client:
            res = client.post(
                f"/users/{user.id}/edit",
                data={
                    "id": user.id,
                    "first_name": "CCC",
                    "last_name": "DDD",
                    "image_url": "test_url",
                },
                follow_redirects=True,
            )
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("CCC DDD", html)

    def test_user_delete(self):
        """Testing the delete user handling"""
        user = User.query.first()
        id = user.id
        with app.test_client() as client:
            res = client.post(
                f"/users/{user.id}/delete", data={}, follow_redirects=True
            )
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn(user.full_name, html)

    def test_index(self):
        """Testing the home page"""
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Blogly Recent Posts", html)

    def test_post(self):
        """Testing the post detail page"""
        with app.test_client() as client:
            res = client.get(f"/posts/{self.post_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("test title", html)

    def test_post_new(self):
        """Testing the add post form"""

        user = User.query.get(self.user_id)

        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}/posts/new")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f"Add Post for {user.full_name}", html)

    def test_post_edit(self):
        """Testing the edit post form"""
        post = Post.query.first()

        with app.test_client() as client:
            res = client.get(f"/posts/{post.id}/edit")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Edit Post", html)
            self.assertIn(post.title, html)
            self.assertIn(post.content, html)

    def test_post_edit_post(self):
        """Testing the update post handling"""
        post = Post.query.first()
        with app.test_client() as client:
            res = client.post(
                f"/posts/{post.id}/edit",
                data={
                    "id": post.id,
                    "title": "Title",
                    "content": "Post Content",
                },
                follow_redirects=True,
            )
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)

            self.assertIn("Title", html)
            self.assertIn("Edit", html)

    def test_tags(self):
        """Testing the tags page"""
        with app.test_client() as client:
            res = client.get("/tags")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Tags", html)

    def test_tag(self):
        """Testing the tag detail page"""
        with app.test_client() as client:
            res = client.get(f"/tags/{self.tag_id}")
            html = res.get_data(as_text=True)

            tag = Tag.query.get(self.tag_id)

            self.assertEqual(res.status_code, 200)
            self.assertIn(tag.name, html)

    def test_post_new(self):
        """Testing the add tag form"""

        with app.test_client() as client:
            res = client.get(f"/tags/new")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Add Tag", html)

    def test_tag_edit(self):
        """Testing the edit tag form"""
        tag = Tag.query.first()

        with app.test_client() as client:
            res = client.get(f"/tags/{tag.id}/edit")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Edit Tag", html)
            self.assertIn(tag.name, html)
