from models.user_model import make_admin, find_user_by_username

def promote_to_admin(current_user, target_username):
    if current_user["role"] != "admin":
        return False

    if not find_user_by_username(target_username):
        return False

    make_admin(target_username)
    return True


def remove_user(current_user, target_username):
    """Allow an administrator to delete another user."""
    if current_user["role"] != "admin":
        return False

    if current_user.get("username") == target_username:
        return False

    if not find_user_by_username(target_username):
        return False

    from models.user_model import delete_user
    delete_user(target_username)
    return True


def list_users():
    """Return list of users (sanitized)."""
    from models.user_model import get_all_users
    return get_all_users()