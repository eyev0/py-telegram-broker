from app import config


def admin_lambda():
    return lambda m: m.from_user.id in config.check_admin


def not_admin_lambda():
    return lambda m: m.from_user.id not in config.check_admin
