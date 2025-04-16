import asyncio
from config import dp, bot
from db import init_db
import handlers
import admin

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
