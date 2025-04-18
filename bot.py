import asyncio
from config import dp, bot
from db import init_db
import handlers
import admin


async def main():
    try:
        init_db()
    except Exception as error:
        print(error)

    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Starting bot...")
    asyncio.run(main())
