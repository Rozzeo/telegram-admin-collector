# list_my_admin_channels.py
from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio

api_id = 21108803   # замените на число
api_hash = 'f20c9463c0e3006826bf44dec6a326fc'  # замените на строку
session_name = 'me'  # любое имя сессии, например 'me'

async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()  # попросит номер и код, если нужно

    # Получаем все диалоги (chats, каналлы, чаты, группы)
    dialogs = await client.get_dialogs()
    admin_channels = []

    for dialog in dialogs:
        entity = dialog.entity
        # проверяем, является ли это каналом/супергруппой
        if getattr(entity, 'broadcast', False) or getattr(entity, 'megagroup', False) or getattr(entity, 'gigagroup', False):
            # получаем список админов (если у вас права админа, вы увидите себя в списке)
            try:
                admins = await client.get_participants(entity, filter=ChannelParticipantsAdmins)
                # ищем себя в списке админов
                me = await client.get_me()
                am_i_admin = any(a.id == me.id for a in admins)
                if am_i_admin:
                    admin_channels.append({
                        'title': getattr(entity, 'title', str(entity)),
                        'id': entity.id,
                        'username': getattr(entity, 'username', None)
                    })
            except Exception as e:
                # некоторые чаты/каналы могут быть приватны и вернуть ошибку — игнорируем
                # print('skip', entity, e)
                pass

    # Вывод
    for c in admin_channels:
        print(f"{c['title']}  — id: {c['id']}  username: {c['username']}")

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
