import fitz
doc = fitz.open('./papers/Physics 4/55_C_1 Physics.pdf')
for i in range(10):
    text = doc[i].get_text()
    hindi_score = text.count('{') + text.count('}') + text.count('$') + text.count('©') + text.count('~')
    eng_score = text.lower().count('the ') + text.lower().count(' is ') + text.lower().count(' of ')
    print(f'Page {i}: Hindi Score = {hindi_score}, English Score = {eng_score}')
