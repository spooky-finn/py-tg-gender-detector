
from .tgparser import Tgparser
from gender_computer import GenderComputer
from .fstream import Fstream

async def gender_entrypoint(client, application_path, target_prefix) -> None:
    parser = Tgparser(client)
    gc = GenderComputer()
    fstream = Fstream(application_path)
    
    chat_url = input("Ссылка на чат: ")
    all_participants = await parser.GetChatParticipants("https://t.me/algoritm_schools")
    
    males = []
    females = []

    for user in all_participants:
        if user.bot: continue
        
        first_name = user.first_name or 'none'
        last_name  = user.last_name or 'none'
        try:
            gender = gc.resolveGender(f'{first_name} {last_name}', 'Russia')
            
            if gender == "male":
                males.append(user)
            elif gender == "female":
                females.append(user)
            else: continue
        except:
            continue
        
    fstream.create_dual_report(target_prefix, 'males', males)
    fstream.create_dual_report(target_prefix, 'females', females)