import requests

# url_1 = 'http://bullet.video.qq.com/fcgi-bin/target/regist?otype=json&vid='
#
# file_bullet_url = open('bullet_url', 'w')
# for line in open("video_http", "r"):
#     file_bullet_url.write(requests.get(url_1 + line[41:41+11]).text + '\n')
# file_bullet_url.close()

url_2_1 = 'http://mfm.video.qq.com/danmu?timestamp='
url_2_2 = '&target_id='
titles = ["\"content\"", "\"upcount\"", "\"timepoint\"", "\"opername\""]
root_dir = 1

file_input = open('bullet_url', 'r')
bullet = file_input.readline()
file_count = open('count.txt', 'w')
while bullet:

    target_id = bullet[bullet.rindex('"')-10:bullet.rindex('"')]
    delay_times = 0
    timestamp = 0
    numbers = 0
    file_data = open(str(root_dir) + '.txt', 'w')
    while 1:
        res = requests.get(url_2_1 + str(timestamp) + url_2_2 + target_id)
        res.encoding = 'utf-8'
        text = res.text

        count_index = text.index('"count"')
        count = int(text[count_index+8:text.index(',', count_index+8)])
        if count < 1:
            if delay_times < 100:
                delay_times = delay_times + 1
            else:
                break
        else:
            numbers = numbers + count
            i = 0
            loc = text.index("\"comments\"")

            flag = 1

            # file_data = open(str(root_dir) + '/' + str(timestamp) + '.txt', 'w')
            while i < count:
                j = 0
                while j < len(titles):
                    t_loc = text.find(titles[j], loc)
                    if t_loc == -1:
                        flag = 0
                        break
                    token = text[t_loc+len(titles[j])+1:text.index(',', t_loc+len(titles[j])+1)]

                    if token[0] == '"':
                        token = token[1:len(token)-1]
                    file_data.write(token+'\t')
                    loc = text.index(',', t_loc+len(titles[j])+1)
                    j = j + 1
                if flag == 0:
                    file_data.write('\n')
                    break
                file_data.write('\n')
                i = i + 1
                file_data.flush()
            # file_data.close()
        # print(timestamp)
        timestamp = timestamp + 30

    file_data.close()
    print(numbers)
    file_count.write(str(numbers) + '\n')
    bullet = file_input.readline()
    root_dir = root_dir + 1

file_count.close()
file_input.close()
