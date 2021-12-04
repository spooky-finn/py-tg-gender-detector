import uuid, re, os, sys
from telethon import TelegramClient
import asyncio
from gender_Computer.genderComputer import GenderComputer

from cfg.cfg import *
# from src.check_license import checkLicense
from src.create_report import createReport

from py_hardware_binding.main

async def main(application_path, path_to_session):
    gc = GenderComputer()
    # pgi = input('Пожалуйста, выберите предпочинаемый пол (М или Ж) \n')
    preferGender = 'male'

    # if  pgi == 'М' or pgi == 'м':
    #     preferGender = 'male'

    # elif pgi == 'Ж' or pgi == 'ж':
    #     preferGender = 'female'
    # else:
    #     print('Выберите пол (М или Ж)')
    #     exit(1)


    async with TelegramClient(path_to_session, api_id, api_hash) as client:

        # url  = input('insert link on channel')
        chat = await client.get_entity("https://t.me/instalogiya_chat")
        print('parsing chat..')
        participants = []
        async for user in client.iter_participants(chat, limit=200, aggressive=True):
            #  Вырезаем ботов ебаных
            if user.bot == True:
                continue

            fn, ln = user.first_name or 'none', user.first_name or 'none'
            try:
                gender = gc.resolveGender(f'{fn} {ln}', 'Russia')
                userData = {
                    'id'         : user.id,
                    'first_name' : user.first_name or 'none',
                    'last_name'  : user.last_name  or 'none',
                    'username'   : user.username   or 'none',
                    'gender'     : gender or 'none',
                }
                participants.append(userData)
                
            except:
                continue
           
        createReport(preferGender, participants, application_path)
        print(f"Report saved at {application_path}")




        # print(len(participants))

        # while i < 200000: 

        #     a = await client(GetParticipantsRequest(channel, ChannelParticipantsSearch(''), i, 100, hash=0))
        #     time.sleep(1)
        #     i+=100
        #     for user in a.users:
        #         participants.append(user)
        #     print(len(participants))
        # participants =  await client.get_participants(channel.id)

        # pic = client.download_media(participants.users[6].photo.photo_id, './')
        # print(participants.users[6].photo)
        # print(m.photo.photo_id.download_media("image/"+str(uuid.uuid1())))
        # full =  await client(GetFullUserRequest(participants.users[6]))
        # downloading images
        # for i in range(0, 100):
        #     fn, ln = participants.users[i].first_name or 'none', participants.users[i].last_name or 'none'
        #     gender = gc.resolveGender(f'{fn} {ln}', 'Russia') or 'none'
            # print(f"{fn: <20} {ln: <20} {gender: <20}")
            # await client.download_profile_photo(participants.users[i].id)

        # client.download_profile_photo('me')

        # for e in participants.users:
        #     print(e)
        # await client.send_message('me', 'Hello, myself!')
        # print(await client.download_profile_photo('me'))

        # @client.on(events.NewMessage(pattern='(?i).*Hello'))
        # async def handler(event):
        #     await event.reply('Hey!')

        # await client.run_until_disconnected()

@
def run(WORKDIR):
    
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(WORKDIR))

    path_to_license = os.path.join(base_path, 'cfg/license.txt')
    path_to_session = os.path.join(base_path, 'cfg/anon.session')
    
    # determine if the application is a frozen `.exe` (e.g. pyinstaller --onefile) 
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    # or a script file (e.g. `.py` / `.pyw`)
    elif __file__:
        application_path = WORKDIR
    
    
    if checkLicense(path_to_license):
        asyncio.run( main(
            application_path, 
            path_to_session
            ))