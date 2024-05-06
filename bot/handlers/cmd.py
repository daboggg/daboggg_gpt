from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import Italic

cmd_router = Router()


@cmd_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(Italic("Тестовый ответ").as_html())

