from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

class Tgparser:
    def __init__(self, client) -> None:
        self.client = client
      
    async def GetChatParticipants(self, chat_url=''):
        limit_user = None  # максимальное число записей, передаваемых за один раз
        all_participants = []
        
        # chat_url = "https://t.me/algoritm_schools"
        if not chat_url: chat_url = input('Cсылка на чат: ')
        
        chat = await self.client.get_entity(chat_url)
        print("Чат: ", chat.title)
        
        async for user in self.client.iter_participants(chat, limit_user, aggressive=True):
            all_participants.append(user)
            
        print("Собрано", len(all_participants), 'аккаунтов.')
        return all_participants
            