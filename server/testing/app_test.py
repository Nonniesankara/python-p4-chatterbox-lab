from datetime import datetime
import pytest

from app import app, db, Message

class TestMessage:
    '''Tests for the Message model'''

    @pytest.fixture(autouse=True)
    def clean_database(self):
        '''
        Runs before and after each test to ensure a clean DB state.
        '''
        with app.app_context():
            # Delete all messages before test
            Message.query.delete()
            db.session.commit()

        yield

        with app.app_context():
            # Delete all messages after test
            Message.query.delete()
            db.session.commit()

    def test_can_create_message(self):
        '''Can create a message and save to DB'''
        with app.app_context():
            message = Message(
                body="Hello 👋",
                username="Liza"
            )

            db.session.add(message)
            db.session.commit()

            fetched = Message.query.filter_by(body="Hello 👋").first()

            assert fetched is not None
            assert fetched.body == "Hello 👋"
            assert fetched.username == "Liza"
            assert isinstance(fetched.created_at, datetime)

    def test_updated_at_auto_updates(self):
        '''updated_at field changes when message is updated'''
        with app.app_context():
            message = Message(
                body="Original",
                username="Liza"
            )

            db.session.add(message)
            db.session.commit()

            original_updated_at = message.updated_at

            # update the body
            message.body = "Updated!"
            db.session.add(message)
            db.session.commit()

            assert message.updated_at > original_updated_at

    def test_message_repr_contains_username(self):
        '''repr string includes username'''
        with app.app_context():
            message = Message(
                body="Hi",
                username="Liza"
            )
            repr_string = repr(message)
            assert "Liza" in repr_string
