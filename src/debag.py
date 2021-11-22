def debagMistakesReport(participants):
    genderComputerMistakes = []
    with open('mistakes report.txt', 'w') as f:
        f.write(f"{'index': <5} | {'first_name': <30} {'last_name': <30} {'gender': <10} \n")
        f.write('\n')
        for index, i in enumerate(participants):
            f.write(f"{index: <5} | {i['first_name']: <30} {i['last_name']: <30} {i['username']: <30} {i['gender']: <10} \n")
            if i['gender'] == 'none': 
                genderComputerMistakes.append(i)
    print('mistakes: ', len(genderComputerMistakes))
    print('amount participants: ', len(participants))
    

def debagPrint(participants):
    for i in participants:
        print(f"{i['first_name']: <20} {i['last_name']: <20} {i['gender']: <20}")    
    print('amount participants: ', len(participants))
        