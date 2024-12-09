'''пишем код в отдельном файле питона
создаем файл в байтовом виде
cenz.txt пишем все запрещенные слова в столбик с абзацем
открываем его  с помощью with и делаем из него джейсон
ЗАПУСКАЕМ
чтобы добавить какие-то слова, добавьте их в файл badwords.txt 
и запусти файл заново, слова просто перезапишутся'''

import json
import os
 
# Определяем путь к файлу
base_path = os.path.dirname(__file__)  # Получаем путь к текущему файлу
badwords_path = os.path.join(base_path, 'badwords.txt')
output_path = os.path.join(base_path, 'cenz.json')



ar = []

with open(badwords_path, encoding='utf-8') as r:
    for i in r:
        n=i.lower().split('\n')[0]
        if n != '':
            ar.append(n)

with open(output_path, 'w', encoding='utf-8') as e:
    json.dump(ar, e)