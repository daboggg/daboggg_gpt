from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import Italic
from aiogram_dialog import StartMode, DialogManager

from bot.state_groups import MainSG

cmd_router = Router()


# @cmd_router.message(CommandStart())
# async def cmd_start(message: Message) -> None:
#     await message.answer(Italic("Тестовый ответ").as_html())


@cmd_router.message(CommandStart())
async def settings_reminders(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainSG.start, mode=StartMode.RESET_STACK)

