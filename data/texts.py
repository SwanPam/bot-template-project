class UserText:
    @staticmethod
    def welcome_main_menu(username: str, user_balance: float, user_ref_balance: float) -> str:
        return f'''Добро пожаловать, {username}
Ваш баланс: {user_balance}
Ваш бонусный баланс: {user_ref_balance}
'''   