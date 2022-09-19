# module connection
import requests
import time
import sqlite3

# Token & id
token = '11ed0931ae8362f6977111dd9ba8357c39e6f41e1facf1720dd72b374affcd51accbcb2af88cac51d45fe'
group_id = 'etorabotaet'
kolyan_N_id = '187199017'


# general code
def vk_download(method, parameters, token=token):
    url = \
        'https://api.vk.com/method/' + method + '?' + parameters + '&access_token=' + token + "&v=5.81"
    response = requests.get(url)
    try:
        return (response.json())['response']
    except:
        print('Нужно обновить токен по ссылке из main.py')
        exit()


title_group = vk_download('groups.getById', 'group_id=' + group_id)
wall = vk_download('wall.get', 'domain=' + group_id)
count_notes = wall['count']
name_group = title_group[0]['name']
amount_of_posts = int(input('на странице ' + str(count_notes)+' записей. Сколько скачать? '))

conn = sqlite3.connect(name_group + '.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS wall(
   number TEXT,
   author TEXT,
   comments TEXT,
   likes TEXT,
   reposts TEXT);
""")

for i in range(0,amount_of_posts):
    param = '&count=1&offset=' + str(i)
    note = vk_download('wall.get', 'domain=' + group_id + param)
    note = note['items'][0]
    author_note, comments_count = 'Гость', str(note['comments']['count'])
    likes_count, reposts_count = str(note['likes']['count']), str(note['reposts']['count'])
    if int(note['from_id']) == int(note['owner_id']):
        author_note = 'Владелец'
    information_recording = (i, author_note, comments_count, likes_count, reposts_count)
    cur.execute("INSERT INTO wall VALUES(?,?,?,?,?);", information_recording)
    conn.commit()
    time.sleep(0.5)
    print('Записей скачано:', i+1)

print('Посты скачаны. Всего скачано: ' + str(amount_of_posts))

