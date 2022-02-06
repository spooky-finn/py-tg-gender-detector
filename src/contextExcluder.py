import re

from telethon import functions

from .fstream import Fstream
from .tgparser import Tgparser


class ContextExcluder:
    def __init__(self, client, application_path, target_prefix) -> None:
        self.client = client
        self.application_path = application_path
        self.target_prefix = target_prefix

    async def Include(self):
        parser = Tgparser(self.client)
        fstream = Fstream(self.application_path)
        participants = await parser.GetChatParticipants()
        wordlist = fstream.fread_by_line(self.application_path + "/wordlist.txt")

        if len(wordlist) == 0:
            print(
                "Файл wordlist.txt пустой. Чиркни туда ключевых словечек (по одному слову на строчку)"
            )
            exit()

        target_participants = []

        for user in participants:
            if not user.first_name and not user.last_name:
                continue

            userdata = []
            for dd in [user.first_name, user.last_name, user.username]:
                if not isinstance(dd, str):
                    continue
                userdata += re.split("_|-| ", dd)

            have_kword = False
            for keyword in wordlist:
                for user_data_unit in userdata:
                    if keyword.lower() in user_data_unit.lower():
                        have_kword = True

            if have_kword:
                target_participants.append(user)

        fstream.create_dual_report(self.target_prefix, "include", target_participants)
        print("key-words: ", wordlist)
        # for user in target_participants: print(user.first_name, user.last_name, f'@{user.username}')

    async def Exclude(self):
        parser = Tgparser(self.client)
        fstream = Fstream(self.application_path)
        participants = await parser.GetChatParticipants()
        wordlist = fstream.fread_by_line(self.application_path + "/wordlist.txt")

        if len(wordlist) == 0:
            print(
                "Файл wordlist.txt пустой. Чиркни туда ключевых словечек (по одному слову на строчку)"
            )
            exit()

        target_participants = []

        for user in participants:
            if not user.first_name and not user.last_name:
                continue

            userdata = []
            for dd in [user.first_name, user.last_name, user.username]:
                if not isinstance(dd, str):
                    continue
                userdata += re.split("_|-| ", dd)
            # userdata - это массив, содержащий раздробеннуб информацию об аккаунте
            have_kword = False

            for keyword in wordlist:
                for element in userdata:
                    if keyword.lower() in element.lower():
                        have_kword = True

            if not have_kword:
                target_participants.append(user)

        fstream.create_dual_report(self.target_prefix, "exclude", target_participants)
        print("key-words: ", wordlist)
        # for user in target_participants: print(user.first_name, user.last_name, f'@{user.username}')

    async def FullUserIncluder(self):
        parser = Tgparser(self.client)
        fstream = Fstream(self.application_path)
        participants = await parser.GetChatParticipants()
        wordlist = fstream.fread_by_line(self.application_path + "/wordlist.txt")

        if len(wordlist) == 0:
            print(
                "Файл wordlist.txt пустой. Чиркни туда ключевых словечек (по одному слову на строчку)"
            )
            exit()

        target_participants = []

        fullInfoParticipants = []
        print(
            "Этот процесс может занять весьма весьма много времени из-за ограничений телеграма :_"
        )
        for user in participants:
            result = await self.client(functions.users.GetFullUserRequest(id=user.id))
            fullInfoParticipants.append(result)
            print(
                "Собрано",
                len(fullInfoParticipants),
                "аккаунтов из",
                len(participants),
                end="\r",
            )
            if len(fullInfoParticipants) > 300:
                break
        print("")

        for user in fullInfoParticipants:
            about = user.about
            user = user.user
            if not user.first_name and not user.last_name:
                continue

            userdata = []
            for dd in [user.first_name, user.last_name, user.username, about]:
                if not isinstance(dd, str):
                    continue
                userdata += re.split("_|-| ", dd)

            # userdata - это массив, содержащий раздробеннуб информацию об аккаунте
            have_kword = False

            for keyword in wordlist:
                for element in userdata:
                    if keyword.lower() in element.lower():
                        have_kword = True

            if have_kword:
                target_participants.append(user)

        fstream.create_dual_report(
            self.target_prefix, "full_bio_include", target_participants
        )
        print("key-words: ", wordlist)
        # for user in target_participants: print(user.first_name, user.last_name, f'@{user.username}')
