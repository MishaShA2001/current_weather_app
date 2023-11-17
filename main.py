"""Entry point"""
from services.main_menu_handler import react_to_user_message
from content.main_messages import MAIN_MENU_MESSAGE
from db.config import TABLE_NAME, TABLE_COLUMNS
from db.methods import initialize_db_table


def main() -> None:
    """Start and interact with user"""
    initialize_db_table(TABLE_NAME, TABLE_COLUMNS)

    while True:
        user_message = input(MAIN_MENU_MESSAGE)
        react_to_user_message(user_message.strip())


if __name__ == '__main__':
    main()
