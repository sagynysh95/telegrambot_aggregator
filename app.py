import ast

from aiogram import Bot, Dispatcher
import asyncio
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from main import toDatetime, func1
from config import BOT_TOKEN


REQUEST_PATTERN: str = (
        '^{\"dt_from\": \"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\", ' +
        '\"dt_upto\": \"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\",\s' +
        '\"group_type\": \"(?P<group_type>hour|day|month)\"}$'
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Hi {message.from_user.full_name}!')


@dp.message()
async def func(message: Message):
    try:
        input = ast.literal_eval(message.text)
        start_date = input["dt_from"]
        end_date = input["dt_upto"]
        groupby = input["group_type"]
        start = await toDatetime(start_date)
        end = await toDatetime(end_date)
        result = await func1(start, end, groupby)
        await message.answer(f'{result}')
    except TelegramBadRequest:
        await message.answer('Допустимо отправлять только следующие запросы:\n'
                             '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", '
                             '"group_type": "month"}\n'
                             '{"dt_from": "2022-10-01T00:00:00", "dt_upto": "2022-11-30T23:59:00", '
                             '"group_type": "day"}\n'
                             '{"dt_from": "2022-02-01T00:00:00", "dt_upto": "2022-02-02T00:00:00", '
                             '"group_type": "hour"}')
    except Exception:
        await message.answer('Невалидный запрос. Пример запроса:\n'
                             '{"dt_from": "2022-09-01T00:00:00", '
                             '"dt_upto": "2022-12-31T23:59:00", "group_type": "month"}')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())