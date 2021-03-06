import os
from array import array


# Класс для работы с файлами и создания отчетов
class Fstream:
    def __init__(self, application_path) -> None:
        self.reports_path = os.path.join(application_path, "reports")

        if not os.path.isdir(self.reports_path):
            os.mkdir(self.reports_path)

    def create_single_report(prefix, filename, participants):
        pass

    def fread_by_line(self, path) -> array:
        '''
        Принимет путь до файла и возвращает массив, где элементами являются строчки
        '''
        if not os.path.isfile(path):
            with open(path, "w") as fp:
                pass

        with open(path, "r") as f:
            data = []
            for each in f.readlines():
                data.append(each.strip())
            return data

    def create_dual_report(self, target, filename, participants):
        '''
        Cоздает два файла: первый со списком людей у которых есть username,
        второй - с id, для тех людей, которые юзернейм не поставили.
        '''
        with_username = []
        without_username = []

        if type(participants[0]) == dict:
            for user in participants:
                if user["username"]:
                    with_username.append(user["username"])
                else:
                    without_username.append(user["id"])
        else:
            for user in participants:
                if user.username:
                    with_username.append(user.username)
                else:
                    without_username.append(user.id)

        with open(f"{self.reports_path}/{target}_{filename}.txt", "w") as f:
            for i in with_username:
                f.write(f"@{i} \n")
        print("Отчет сохранен в", os.path.join(self.reports_path, filename + ".txt"))

        with open(f"{self.reports_path}/{target}_{filename}_id.txt", "w") as f:
            for i in without_username:
                f.write(f"{i} \n")
        print("Отчет сохранен в", os.path.join(self.reports_path, filename + "_id.txt"))
