from models.user_model import make_admin, find_user_by_username

def promote_to_admin(current_user, target_username):
    if current_user["role"] != "admin":
        return False

    if not find_user_by_username(target_username):
        return False

    make_admin(target_username)
    return True