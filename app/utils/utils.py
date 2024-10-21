from flask import session
from uuid import uuid4
def create_session(user_id: str):
    session_id = f"{uuid4}-user-{user_id}"
    session['session_id'] = session_id
    session[session_id] = {
        "user_id": user_id,
        "conversations": {}
    }