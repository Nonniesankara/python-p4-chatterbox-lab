from app import app, db, Message

def make_messages():
    print("Deleting existing messages...")
    Message.query.delete()

    messages = [
        Message(body="Hello, world!", username="Alice"),
        Message(body="Flask is awesome.", username="Bob"),
        Message(body="React and Flask - perfect combo!", username="Carol"),
    ]

    db.session.add_all(messages)
    db.session.commit()
    print("🌱 Database seeded successfully!")

if __name__ == '__main__':
    with app.app_context():
        make_messages()
