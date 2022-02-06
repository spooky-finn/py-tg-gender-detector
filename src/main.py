import json
import ast
import shutil
from turtle import circle

import uuid, re, os, sys

from .gender_entrypoint import gender_entrypoint
from telethon import TelegramClient
import asyncio

from gender_computer import GenderComputer

from cfg.cfg import *
from src.create_report import createReport

from py_hardware_binding import authenticate
from .startupMessage import startup_message
from .contextExcluder import ContextExcluder

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
async def main(application_path, path_to_session):
    async with TelegramClient(path_to_session, api_id, api_hash) as client:
                
        pamyatka = "2. Хочешь отобрать аккаунты с плохими параметрами. И разделить их хорошие и плохие аккаунты в разные папки? Тогда заранее создай 3 файла с расширением .txt и назови так(скопируй их названия и вставь):" \
                "\n" \
                "app_id_normal" \
                "\n" \
                "app_version_normal" \
                "\n" \
                "system_lang_pack_normal" \
                "\n" \
                "\n" \
                "После чего занеси в нужный тебе текстовый документ хорошие параметры для регистрации. Плохие параметры отсеются сами " \
                "и аккаунты с плохими параметрами автоматически перенесутся в созданную папку под названием 'Плохие аккаунты'" \
                "\n" \
                "\n" \
                "3. Хочешь поставить @ перед username?" \
                "\n" \
                "Создай заранее файл с расширением .txt и назови его 'all', в него помести юзернеймы, ничего страшного, если у кого то будет собачка, у кого то нет. Скрипт сделает свою работу отлично! " \
                "\n" \
                "\n" \
                "4. Хочешь разделить username и id по разным файлам?" \
                "\n" \
                "Создай заранее файл с расширением .txt и назови его 'ID'. Далее помести туда список из username и id в перемешку." \
                "\n" \
                "Скрипт все отсортирует и запишет id в один файл, username в другой" \
                "\n" \
                "\n" \
                "5. Хочешь найти уникальных юзеров среди чатов конкурентов(ту аудиторию, которой нет у тебя?)" \
                "\n" \
                "Создай заранее 2 файла с расширением .txt и назови их 'user_drugix_chatov' и 'user_my_chat' помести туда username или id и запусти." \
                "\n" \
                "Скрипт сам отберет уникальные элементы и сохранит в другой файл" \
                "\n" \
                "\n" \
                "7. Хочешь вытащить параметры из лучших аккаунтов после спама?" \
                "\n" \
                "Создай заранее 1 файл с расширением .txt и назови его 'stat'.Помести туда информацию в следующем виде:" \
                "\n" \
                "03:18:27 - Sent:: 917904689102:15\n"\
                "03:18:27 - Sent:: 916206862097:3\n"\
                "03:18:28 - Sent:: 917905568687:25\n"\
                "03:18:29 - Sent:: 916307306964:9\n"\
                "03:18:30 - Sent:: 917065423240:13\n"\
                "03:18:31 - Sent:: 917643875701:11\n"\
                "03:18:32 - Sent:: 917023423708:8\n"\
                "03:18:32 - Sent:: 918107049578:33\n" \
                "\n" \
                "\n" \
                "8. Хочешь убрать стоп-слова из username?" \
                "\n" \
                "Создай заранее 2 файла с расширением .txt и назови их 'stop_slova' и 'all_users_tg' соответственно." \
                "\n" \
                "Помести в файл 'stop_slova'  -  слова, которые не должен содержать username. А в файл 'all_users_tg' необходимые username для отбора" \
                "\n" \
                "\n" \
                "Если какого-то пункта здесь нет, значит там все интуитивно понятно и просто!" \
                "\n" \
                "Успехов в работе!"

        with open('Памятка для работы.txt', 'w') as m:
            print(pamyatka, file=m)

        print(bcolors.HEADER + startup_message + bcolors.ENDC)
        
        target = int(input("Введите только цифру: "))

        #-------------------------------------------------------------------------------------------------
        # 1 - Достать все параметры аккаунтов из указанной папки

        if target == 1:

            prov = input('Очищаем предыдущую информацию? "Да" или "Нет" ')
            # # Очищение информации внутри файлов, если она там была
            if prov.lower() == 'да' or prov.lower() == 'lf' or prov.lower() == 'Да':
                open('lang_pack.txt', 'w').close()
                open('system_lang_pack.txt', 'w').close()
                open('app_version.txt', 'w').close()
                open('device.txt', 'w').close()
                open('app_id.txt', 'w').close()
                open('app_hash.txt', 'w').close()
                open('first_name.txt', 'w').close()
                open('last_name.txt', 'w').close()

            a = input('Введите путь до папки с файлами .json: ')
            lang_pack = []
            system_lang_pack = []
            app_version = []
            device = []
            app_id = []
            app_hash = []
            first_name = []
            last_name = []
            path_to_photos = a
            valid_files = ".json"

            for file_name in os.listdir(path_to_photos):
                ext = os.path.splitext(file_name)[1]
                if ext.lower() != valid_files:
                    continue

                path = os.path.join(path_to_photos, file_name)
                with open(path, 'r') as f:
                    line = f.readlines()
                line = json.loads(line[0])
                lang_pack.append(line['lang_pack'])
                system_lang_pack.append(line['system_lang_pack'])
                app_version.append(line['app_version'])
                app_id.append(line['app_id'])
                app_hash.append(line['app_hash'])
                device.append(line['device'] + ":" + line['sdk'])
                first_name.append(line['first_name'])
                last_name.append(line["last_name"])

            # Оставляем только уникальные элементы
            lang_pack = set(lang_pack)
            lang_pack = list(lang_pack)
            system_lang_pack = set(system_lang_pack)
            system_lang_pack = list(system_lang_pack)
            device = set(device)
            device = list(device)
            app_version = set(app_version)
            app_version = list(app_version)
            app_id = set(app_id)
            app_id = list(app_id)
            app_hash = set(app_hash)
            app_hash = list(app_hash)
            first_name = set(first_name)
            first_name = list(first_name)
            last_name = set(last_name)
            last_name = list(last_name)

            # write lang_pack
            with open('lang_pack.txt', 'r') as f:
                ost_elem = f.readline()
                if ost_elem != '':
                    ost_elem = str(ost_elem)
                    ost_elem = "[" + ost_elem[1:-1] + "]"
                    ost_elem = ost_elem.replace("|", r', ')
                    ost_elem = ost_elem[1:-2].split(', ')

                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        lang_pack.append(ost_elem[i])
            lang_pack = set(lang_pack)
            lang_pack = list(lang_pack)
            lang_pack = str(lang_pack)
            lang_pack = lang_pack.replace("'", r'')
            lang_pack = lang_pack.replace(", ", r'|')
            lang_pack = "{" + lang_pack[1:-1] + "}"

            open('lang_pack.txt', 'w').close()

            with open('lang_pack.txt', 'w') as m:
                if len(lang_pack) != 0:
                    print(lang_pack, file=m)

            # write system_lang_pack
            with open('system_lang_pack.txt', 'r') as f:
                ost_elem = f.readline()
                if ost_elem != '':
                    ost_elem = str(ost_elem)
                    ost_elem = "[" + ost_elem[1:-1] + "]"
                    ost_elem = ost_elem.replace("|", r', ')
                    ost_elem = ost_elem[1:-2].split(', ')

                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        system_lang_pack.append(ost_elem[i])
            system_lang_pack = set(system_lang_pack)
            system_lang_pack = list(system_lang_pack)
            system_lang_pack = str(system_lang_pack)
            system_lang_pack = system_lang_pack.replace("'", r'')
            system_lang_pack = system_lang_pack.replace(", ", r'|')
            system_lang_pack = "{" + system_lang_pack[1:-1] + "}"

            open('system_lang_pack.txt', 'w').close()

            with open('system_lang_pack.txt', 'w') as m:
                if len(system_lang_pack) != 0:
                    print(system_lang_pack, file=m)

            # write device
            with open('device.txt', 'r') as f:
                ost_elem = f.readlines()
                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        device.append(ost_elem[i])

            device = [line.rstrip() for line in device]

            device = set(device)
            device = list(device)

            open('device.txt', 'w').close()

            with open('device.txt', 'w') as m:
                if len(device) != 0:
                    for i in range(len(device)):
                        print(device[i], file=m)

            # write app_version
            with open('app_version.txt', 'r') as f:
                ost_elem = f.readlines()
                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        app_version.append(ost_elem[i])

            app_version = [line.rstrip() for line in app_version]

            app_version = set(app_version)
            app_version = list(app_version)

            open('app_version.txt', 'w').close()

            with open('app_version.txt', 'w') as m:
                if len(app_version) != 0:
                    for i in range(len(app_version)):
                        print(app_version[i], file=m)

            # write app_hash
            with open('app_hash.txt', 'r') as f:
                ost_elem = f.readlines()
                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        app_hash.append(ost_elem[i])

            app_hash = [line.rstrip() for line in app_hash]

            app_hash = set(app_hash)
            app_hash = list(app_hash)

            open('app_hash.txt', 'w').close()

            with open('app_hash.txt', 'w') as m:
                if len(app_hash) != 0:
                    for i in range(len(app_hash)):
                        print(app_hash[i], file=m)

            # write
            for i in range(len(app_id)):
                app_id[i] = str(app_id[i])
            with open('app_id.txt', 'r') as f:
                ost_elem = f.readlines()
                if ost_elem != [] or ost_elem != '':
                    for i in range(len(ost_elem)):
                        app_id.append(ost_elem[i])

            app_id = [line.rstrip() for line in app_id]

            app_id = set(app_id)
            app_id = list(app_id)

            open('app_id.txt', 'w').close()

            with open('app_id.txt', 'w') as m:
                if len(app_id) != 0:
                    for i in range(len(app_id)):
                        print(app_id[i], file=m)

            # write first_name
            with open('first_name.txt', 'r') as f:
                ost_elem = f.readlines()
                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        first_name.append(ost_elem[i])

            first_name = [line.rstrip() for line in first_name]

            first_name = set(first_name)
            first_name = list(first_name)

            open('first_name.txt', 'w').close()

            with open('first_name.txt', 'w', encoding='UTF-8') as m:
                if len(first_name) != 0:
                    for i in range(len(first_name)):
                        print(first_name[i], file=m)

            # write last_name
            with open('last_name.txt', 'r') as f:
                ost_elem = f.readlines()
                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        last_name.append(ost_elem[i])
            try:
                last_name = [line.rstrip() for line in last_name]
            except:
                pass
            last_name = set(last_name)
            last_name = list(last_name)

            open('last_name.txt', 'w').close()

            with open('last_name.txt', 'w') as m:
                if len(last_name) != 0:
                    for i in range(len(last_name)):
                        print(last_name[i], file=m)


        #-----------------------------------------------------------------------------------------------------------------------
        # 2 - Отобрать аккаунты с плохими параметрами. И разделить их хорошие и плохие аккаунты в разные папки

        if target == 2:

            try:
                os.mkdir("Плохие аккаунты")
            except:
                pass
            a = input('Введите путь до папки с файлами .json: ')
            oshib_param = input("Какой параметр ошибочный? 'system_lang_pack' или 'app_version' или 'app_id': ")
            path_to_photos = a
            valid_files = ".json"
            ost_elem = []


            if oshib_param == "app_version":
                # Читаем из файла и убираем \n если они тут есть
                with open('app_version_normal.txt', 'r') as l:
                    ost_elem = l.readlines()

                for i in range(len(ost_elem)):
                    if "\n" in ost_elem[i]:
                        ost_elem[i] = ost_elem[i][:-1]

            if oshib_param == "system_lang_pack":
                # Читаем из файла и убираем \n если они тут есть
                with open('system_lang_pack.txt', 'r') as f:
                    ost_elem = f.readline()
                    if ost_elem != '':
                        ost_elem = str(ost_elem)
                        ost_elem = "[" + ost_elem[1:-1] + "]"
                        ost_elem = ost_elem.replace("|", r', ')
                        ost_elem = ost_elem[1:-2].split(', ')


            if oshib_param == "app_id":
                # Читаем из файла и убираем \n если они тут есть
                with open('app_id_normal.txt', 'r') as l:
                    ost_elem = l.readlines()
                print(ost_elem)
                for i in range(len(ost_elem)):
                    if "\n" in ost_elem[i]:
                        ost_elem[i] = ost_elem[i][:-1]






            for file_name in os.listdir(path_to_photos):
                ext = os.path.splitext(file_name)[1]
                if ext.lower() != valid_files:
                    continue

                path = os.path.join(path_to_photos, file_name)
                with open(path, 'r') as f:
                    line = f.readlines()
                line = json.loads(line[0])

                #Если ошибочный параметр app_version
                if oshib_param == "app_version":
                    if ost_elem != []:
                        if str(line['app_version']) not in ost_elem:
                            file_source = a
                            file_destination = os.getcwd() + "\\" + "Плохие аккаунты"

                            get_files = os.listdir(file_source)

                            try:
                                os.replace(file_source + "/" + line['session_file']+".json",
                                        file_destination + "/" + line['session_file']+".json")
                            except:
                                pass

                            try:
                                os.replace(file_source + "/" + line['session_file']+".session",
                                        file_destination + "/" + line['session_file']+".session")
                            except:
                                pass




                # Если ошибочный параметр system_lang_pack

                if oshib_param == "system_lang_pack":
                    if ost_elem != []:
                        if str(line['system_lang_pack']) not in ost_elem:
                            file_source = a
                            file_destination = os.getcwd() + "\\" + "Плохие аккаунты"

                            get_files = os.listdir(file_source)

                            try:
                                os.replace(file_source + "/" + line['session_file']+".json",
                                        file_destination + "/" + line['session_file']+".json")
                            except:
                                pass

                            try:
                                os.replace(file_source + "/" + line['session_file']+".session",
                                        file_destination + "/" + line['session_file']+".session")
                            except:
                                pass




                # Если ошибочный параметр system_lang_pack

                if oshib_param == "app_id":
                    if ost_elem != []:
                        if str(line['app_id']) not in ost_elem:
                            file_source = a
                            file_destination = os.getcwd() + "\\" + "Плохие аккаунты"

                            get_files = os.listdir(file_source)

                            try:
                                os.replace(file_source + "/" + line['session_file'] + ".json",
                                        file_destination + "/" + line['session_file'] + ".json")
                            except:
                                pass

                            try:
                                os.replace(file_source + "/" + line['session_file'] + ".session",
                                        file_destination + "/" + line['session_file'] + ".session")
                            except:
                                pass

        #------------------------------------------------------------------------------------
        # 3 - Поставить @ перед username

        if target == 3:
            with open('all.txt','r') as f:
                all = f.read().split()
            for i in range(len(all)):
                if all[i][0] != '@':
                    with open('COMPLETED.txt', 'a') as m:
                        print('@'+all[i], file=m)
                else:
                    with open('COMPLETED.txt', 'a') as m:
                        print(all[i], file=m)

        #-------------------------------------------------------------------------------------
        # 4 - Хочешь разделить username и id по разным файлам?

        if target == 4:
            open('@Username_completed.txt', 'w').close()
            open('id_completed.txt', 'w').close()

            with open('id.txt','r') as f:
                all = f.read().split()

            for i in range(len(all)):
                if all[i][0] == "@":
                    with open('@Username_completed.txt', 'a') as m:
                        print(all[i], file=m)
                else:
                    with open('id_completed.txt', 'a') as m:
                        print(all[i], file=m)



        #---------------------------------------------------------------------------------
        #5 - Хочешь найти уникальных юзеров среди чатов конкурентов(ту аудиторию, которой нет у тебя?)

        if target == 5:
            with open('user_drugix_chatov.txt','r') as f:
                user_drugix_chatov = f.read().split()

            with open('user_my_chat.txt','r') as g:
                user_my_chat = g.read().split()

            list = []
            open('unique_user.txt', 'w').close()
            for i in range(len(user_drugix_chatov)):
                n = 0
                for j in range(len(user_my_chat)):
                    if user_drugix_chatov[i] != user_my_chat[j]:
                        n = 1
                    else:
                        n = 0
                        break
                if n == 1:
                    list.append(user_drugix_chatov[i])
                    with open('unique_user.txt', 'a') as m:
                        print(user_drugix_chatov[i], file=m)

        #-------------------------------------------------------------------------------------------------------------
        # 7 - Вытащить параметры из лучших аккаунтов после спама

        if target == 6:

            prov = input('Очищаем предыдущую информацию? "Да" или "Нет" ')
            # # Очищение информации внутри файлов, если она там была
            if prov.lower() == 'да' or prov.lower() == 'lf' or prov.lower() == 'Да':
                open('lang_pack.txt', 'w').close()
                open('system_lang_pack.txt', 'w').close()
                open('app_version.txt', 'w').close()
                open('device.txt', 'w').close()
                open('app_id.txt', 'w').close()
                open('app_hash.txt', 'w').close()
                open('first_name.txt', 'w').close()
                open('last_name.txt', 'w').close()

            a = input('Введите путь до папки с файлами .json: ')
            min_kolvo_message = int(input("Введите мин. кол-во сообщений, которое должен был отправить аккаунт: "))
            kolvo_message_po_factu = 0
            flag = 0
            lang_pack = []
            system_lang_pack = []
            app_version = []
            device = []
            app_id = []
            app_hash = []
            first_name = []
            last_name = []
            path_to_photos = a
            valid_files = ".json"




            with open("stat.txt",'r') as f:
                stroki = f.read().split(':')

            for i in range(len(stroki)):
                if len(stroki[i]) >= 11:
                    try:
                        stroki[i] = int(stroki[i])
                    except:
                        pass
                    if type(stroki[i]) == int:
                        if (len(str(stroki[i+1]))) >= 2:
                            if stroki[i+1][1] not in ['1','2','3','4','5','6','7','8','9']:
                                kolvo_message_po_factu = int(stroki[i+1][0])
                                if kolvo_message_po_factu >= min_kolvo_message:
                                    path = os.path.join(path_to_photos, str(stroki[i])+".json")
                                    with open(path, 'r') as f:
                                        line = f.readlines()
                                    line = json.loads(line[0])
                                    lang_pack.append(line['lang_pack'])
                                    system_lang_pack.append(line['system_lang_pack'])
                                    app_version.append(line['app_version'])
                                    app_id.append(line['app_id'])
                                    app_hash.append(line['app_hash'])
                                    device.append(line['device'] + ":" + line['sdk'])
                                    first_name.append(line['first_name'])
                                    last_name.append(line["last_name"])
                            elif (len(str(stroki[i+1]))) >= 2:
                                if stroki[i + 1][1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                                    kolvo_message_po_factu = int(stroki[i + 1][0] + stroki[i + 1][1])
                                    if kolvo_message_po_factu >= min_kolvo_message:
                                        path = os.path.join(path_to_photos, str(stroki[i]) + ".json")
                                        with open(path, 'r') as f:
                                            line = f.readlines()
                                        line = json.loads(line[0])
                                        lang_pack.append(line['lang_pack'])
                                        system_lang_pack.append(line['system_lang_pack'])
                                        app_version.append(line['app_version'])
                                        app_id.append(line['app_id'])
                                        app_hash.append(line['app_hash'])
                                        device.append(line['device'] + ":" + line['sdk'])
                                        first_name.append(line['first_name'])
                                        last_name.append(line["last_name"])


            # Оставляем только уникальные элементы
            lang_pack = set(lang_pack)
            lang_pack = list(lang_pack)
            system_lang_pack = set(system_lang_pack)
            system_lang_pack = list(system_lang_pack)
            device = set(device)
            device = list(device)
            app_version = set(app_version)
            app_version = list(app_version)
            app_id = set(app_id)
            app_id = list(app_id)
            app_hash = set(app_hash)
            app_hash = list(app_hash)
            first_name = set(first_name)
            first_name = list(first_name)
            last_name = set(last_name)
            last_name = list(last_name)

            # write lang_pack
            with open('lang_pack.txt', 'r') as f:
                ost_elem = f.readline()
                if ost_elem != '':
                    ost_elem = str(ost_elem)
                    ost_elem = "[" + ost_elem[1:-1] + "]"
                    ost_elem = ost_elem.replace("|", r', ')
                    ost_elem = ost_elem[1:-2].split(', ')

                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        lang_pack.append(ost_elem[i])
            lang_pack = set(lang_pack)
            lang_pack = list(lang_pack)
            lang_pack = str(lang_pack)
            lang_pack = lang_pack.replace("'", r'')
            lang_pack = lang_pack.replace(", ", r'|')
            lang_pack = "{" + lang_pack[1:-1] + "}"

            open('lang_pack.txt', 'w').close()

            with open('lang_pack.txt', 'w') as m:
                if len(lang_pack) != 0:
                    print(lang_pack, file=m)

            # write system_lang_pack
            with open('system_lang_pack.txt', 'r') as f:
                ost_elem = f.readline()
                if ost_elem != '':
                    ost_elem = str(ost_elem)
                    ost_elem = "[" + ost_elem[1:-1] + "]"
                    ost_elem = ost_elem.replace("|", r', ')
                    ost_elem = ost_elem[1:-2].split(', ')

                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        system_lang_pack.append(ost_elem[i])
            system_lang_pack = set(system_lang_pack)
            system_lang_pack = list(system_lang_pack)
            system_lang_pack = str(system_lang_pack)
            system_lang_pack = system_lang_pack.replace("'", r'')
            system_lang_pack = system_lang_pack.replace(", ", r'|')
            system_lang_pack = "{" + system_lang_pack[1:-1] + "}"

            open('system_lang_pack.txt', 'w').close()

            with open('system_lang_pack.txt', 'w') as m:
                if len(system_lang_pack) != 0:
                    print(system_lang_pack, file=m)

            # write device
            with open('device.txt', 'r') as f:
                ost_elem = f.readlines()
                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        device.append(ost_elem[i])

            device = [line.rstrip() for line in device]

            device = set(device)
            device = list(device)

            open('device.txt', 'w').close()

            with open('device.txt', 'w') as m:
                if len(device) != 0:
                    for i in range(len(device)):
                        print(device[i], file=m)

            # write app_version
            with open('app_version.txt', 'r') as f:
                ost_elem = f.readlines()
                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        app_version.append(ost_elem[i])

            app_version = [line.rstrip() for line in app_version]

            app_version = set(app_version)
            app_version = list(app_version)

            open('app_version.txt', 'w').close()

            with open('app_version.txt', 'w') as m:
                if len(app_version) != 0:
                    for i in range(len(app_version)):
                        print(app_version[i], file=m)

            # write app_hash
            with open('app_hash.txt', 'r') as f:
                ost_elem = f.readlines()
                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        app_hash.append(ost_elem[i])

            app_hash = [line.rstrip() for line in app_hash]

            app_hash = set(app_hash)
            app_hash = list(app_hash)

            open('app_hash.txt', 'w').close()

            with open('app_hash.txt', 'w') as m:
                if len(app_hash) != 0:
                    for i in range(len(app_hash)):
                        print(app_hash[i], file=m)

            # write
            for i in range(len(app_id)):
                app_id[i] = str(app_id[i])
            with open('app_id.txt', 'r') as f:
                ost_elem = f.readlines()
                if ost_elem != [] or ost_elem != '':
                    for i in range(len(ost_elem)):
                        app_id.append(ost_elem[i])

            app_id = [line.rstrip() for line in app_id]

            app_id = set(app_id)
            app_id = list(app_id)

            open('app_id.txt', 'w').close()

            with open('app_id.txt', 'w') as m:
                if len(app_id) != 0:
                    for i in range(len(app_id)):
                        print(app_id[i], file=m)

            # write first_name
            with open('first_name.txt', 'r') as f:
                ost_elem = f.readlines()
                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        first_name.append(ost_elem[i])

            first_name = [line.rstrip() for line in first_name]

            first_name = set(first_name)
            first_name = list(first_name)

            open('first_name.txt', 'w').close()

            with open('first_name.txt', 'w', encoding='UTF-8') as m:
                if len(first_name) != 0:
                    for i in range(len(first_name)):
                        print(first_name[i], file=m)

            # write last_name
            with open('last_name.txt', 'r', encoding="UTF-8") as f:
                ost_elem = f.readlines()
                if ost_elem != []:
                    for i in range(len(ost_elem)):
                        last_name.append(ost_elem[i])
            try:
                last_name = [line.rstrip() for line in last_name]
            except:
                pass
            last_name = set(last_name)
            last_name = list(last_name)

            open('last_name.txt', 'w').close()

            with open('last_name.txt', 'w') as m:
                if len(last_name) != 0:
                    for i in range(len(last_name)):
                        try:
                            print(last_name[i], file=m)
                        except:
                            continue


        #--------------------------------------------------------------------------------
        # 8. Хочешь убрать стоп-слова из username?
        if target == 7:
            with open("all_users_tg.txt","r") as f:
                all_users_tg = f.readlines()
            with open("stop_slova.txt","r") as g:
                stop_slova = g.readlines()
            for i in range(len(stop_slova)):
                stop_slova[i] = stop_slova[i].rstrip()
            for j in range(len(all_users_tg)):
                all_users_tg[j] = all_users_tg[j].rstrip()
            flagnm = 0
            bad_username = []
            good_username = []

            for i in range(len(stop_slova)):
                for j in range(len(all_users_tg)):
                    try:
                        if stop_slova[i].lower() in all_users_tg[j].lower():
                                bad_username.append(all_users_tg[j])
                    except:
                        pass

            open('user_not_in_stopslov.txt', 'w').close()
            for i in range(len(all_users_tg)):
                if all_users_tg[i] not in bad_username:
                    with open('user_not_in_stopslov.txt', 'a') as m:
                        print(all_users_tg[i], file=m)
            
        if target == 8:
            await gender_entrypoint(client, application_path, target)
        
        cExcluder = ContextExcluder(client, application_path, target)
        
        if target == 9:  await cExcluder.Include ()
        if target == 10: await cExcluder.FullUserIncluder()
        if target == 11: await cExcluder.Exclude()
            
@authenticate
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
    
    
    asyncio.run( main(
        application_path, 
        path_to_session
    ))