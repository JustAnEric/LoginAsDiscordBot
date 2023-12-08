def newline():
    return "\n"

def in_range(a,b):
    if a <= b:
        return True
    else: return False

def create_text_options(orderedOptionsList:list):
    string = ""
    for i,x in enumerate(orderedOptionsList):
        string+=f"{newline() if not i == 0 else ''}[{i}] {x}"
    return string

def get_option_answer(orderedOptionsText:str, number:int):
    for i in orderedOptionsText.split('\n'):
        x = int(i.split('[')[1].split(']')[0])
        if x == int(number):
            return i.split('] ',1)[1]
    return "unknown;"