import os
from discord import PrivilegedIntentsRequired
from filip_bot import FilipRBot
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')


def main():
    bot = FilipRBot()
    try:
        bot.run(TOKEN)
    except PrivilegedIntentsRequired as error:
        return error


if __name__ == "__main__":
    main()
