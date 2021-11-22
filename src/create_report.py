def createReport(preferGender, participants, application_path):
    with_username = []
    without_username = []

    for i in participants:
        if i['username'] != 'none' and i['gender'] == preferGender: with_username.append(i['username'])
        elif i['username'] == 'none' and i['gender'] == preferGender: without_username.append(i['id'])


    with open(f'{application_path}/{preferGender}.txt', 'w') as f:
        for i in with_username:
            f.write(f"@{i} \n")

    with open(f'{application_path}/{preferGender}_id.txt', 'w') as f:
        for i in without_username:
            f.write(f"{i} \n")