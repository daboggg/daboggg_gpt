# главный диалог
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import Bold
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from g4f.client import Client

from bot.state_groups import MainSG
from utils.converter import conv_voice


async def getter_start(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data['messages'] = []
    dialog_manager.dialog_data['client'] = Client()
    return {}


async def getter_text(dialog_manager: DialogManager, **kwargs):
    messages = dialog_manager.dialog_data.get('messages')
    client = dialog_manager.dialog_data.get('client')
    client = Client()


    print(messages)
    if messages:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        messages.append(response.choices[0].message.content)
        return {'message': messages[-1]}
    return {'message': ''}

#########################################################################


async def role_handler(message: Message, message_input: MessageInput, manager: DialogManager) -> None:
    manager.show_mode = ShowMode.DELETE_AND_SEND
    try:
        if message.text:
            text = message.text
        else:
            text = await conv_voice(message, message.bot)
        messages: list = manager.dialog_data['messages']
        messages.append({"role": "system", "content": text})
        await manager.switch_to(MainSG.dialog)
    except Exception as e:
        print(e)
        await manager.switch_to(MainSG.get_role)


async def text_handler(message: Message, message_input: MessageInput, manager: DialogManager) -> None:
    manager.show_mode = ShowMode.DELETE_AND_SEND
    try:
        if message.text:
            text = message.text
        else:
            text = await conv_voice(message, message.bot)
        messages: list = manager.dialog_data['messages']
        messages.append({"role": "user", "content": text})
        await manager.switch_to(MainSG.dialog)
    except Exception as e:
        print(e)
        await manager.switch_to(MainSG.get_role)


# async def on_set_role_selected(callback: CallbackQuery, button: Button,
#                              dialog_manager: DialogManager) -> None:
#     apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get("apscheduler")
#     messages:dict = dialog_manager.dialog_data.get('messages')
#     apscheduler.remove_job(dialog_manager.dialog_data.get("job_id"))
#     await callback.answer("напоминание удалено")
#     del dialog_manager.dialog_data["job_id"]
#     await dialog_manager.switch_to(ListOfRemindersSG.start)


main_dialog = Dialog(
    Window(
        Const(Bold("До начала диалога вы можете задать роль ИИ, или нажмите начать").as_html()),
        SwitchTo(Const("Задать роль ИИ"), state=MainSG.get_role, id='get_role'),
        SwitchTo(Const("Начать диалог"), state=MainSG.dialog, id='dialog'),
        # Case(
        #     {
        #         "0": Const("            🫲   🫱"),
        #         ...: Format("           всего: {count} 👇")
        #     },
        #     selector="count"
        # ),
        # ScrollingGroup(
        #     Select(
        #         Format("{item[0]} {item[1]}"),
        #         id="s_reminders",
        #         item_id_getter=operator.itemgetter(2),
        #         items="reminders",
        #         on_click=on_reminder_selected,
        #     ),
        #     id='scroll',
        #     width=1,
        #     height=7
        # ),
        state=MainSG.start,
        getter=getter_start,
    ),
    Window(
        Const("Введите роль ИИ"),
        MessageInput(
            role_handler,
            content_types=[ContentType.TEXT, ContentType.VOICE]
        ),
        state=MainSG.get_role
    ),
    Window(
        Format(text="{message}"),
        Const("\nВведите текст"),
        MessageInput(
            text_handler,
            content_types=[ContentType.TEXT, ContentType.VOICE]
        ),
        getter=getter_text,
        state=MainSG.dialog
    ),
    # Window(
    #     Format('{remind_info}'),
    #     Back(Const("Назад")),
    #     Button(Const("Удалить"), id='delete_reminder', on_click=on_delete_selected),
    #     state=ListOfRemindersSG.show_reminder,
    #     getter=get_reminder,
    # ),
)
