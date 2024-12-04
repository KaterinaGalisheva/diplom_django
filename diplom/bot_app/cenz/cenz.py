'''пишем код в отдельном файле питона
создаем файл в байтовом виде
cenz.txt пишем все запрещенные слова в столбик с абзацем
открываем его  с помощью with и делаем из него джейсон
ЗАПУСКАЕМ
чтобы добавить какие-то слова, добавьте их в файл badwords.txt 
и запусти файл заново, слова просто перезапишутся'''

import json
 
 
ar = []

with open('badwords.txt', encoding='utf-8') as r:
    for i in r:
        n=i.lower().split('\n')[0]
        if n != '':
            ar.append(n)

with open('cenz.json', 'w', encoding='utf-8') as e:
    json.dump(ar, e)