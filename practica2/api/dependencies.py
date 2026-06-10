from fastapi import Request


def get_admin_session(request: Request):
    return request.session.get("admin")
