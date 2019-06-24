from bs4 import BeautifulSoup
import copy
import re
import json
import os

speaker1 = '<p><strong>(.+)</strong>:'
speaker2 = '<p><b>(.+):</b>'
speaker3 = '<p><strong>(.+):</strong>'

speaker_regex_1 = re.compile(speaker1)
speaker_regex_2 = re.compile(speaker2)
speaker_regex_3 = re.compile(speaker3)

u_re = '^([a-zA-Z\. ’]+):'
u_re = re.compile(u_re)


def episode_id(s, e):
    return 's%02d_e%02d' % (s, e)


def scene_id(s, e, c):
    return '%s_c%02d' % (episode_id(s, e), c)


def utt_id(s, e, c, u):
    return '%s_u%03d' % (scene_id(s, e, c), u)


def parse_line(tag):
    line = str(tag)
    if '</strong>:' in line:
        speaker = speaker_regex_1.findall(line)
    elif ':</b>' in line:
        speaker = speaker_regex_2.findall(line)
    elif ':</strong>' in line:
        speaker = speaker_regex_3.findall(line)
    if speaker is None or len(speaker) == 0:
        return None, None
    speaker = speaker[0]
    utt = tag.text.replace(speaker + ':', '').strip().replace('\n', ' ').replace('', "'").replace('…', '...').replace(
        '', '').replace('', '-').replace('', '-')
    utt = utt.split()
    utt = ' '.join([i for i in utt if i != ''])
    return speaker, utt


def parse_p(p_list, s, e, scene_flag):
    c = 0
    u = 0
    in_scene = False
    episode_data = []
    scenes_data = {}
    for line in p_list:
        # print(line)
        if in_scene:
            r = u_re.findall(line)

            if '[Scene' not in line and len(r) <= 0:
                continue
            if '[Scene' not in line and len(r) > 0:
                speakers = r[0]
                utt = line.replace(speakers + ':', '').strip().replace('\n', ' ').replace('', "'").replace('…',
                                                                                                            '...').replace(
                    '', '').replace('', '-').replace('', '-')
                u += 1
                uttid = utt_id(s, e, c, u)
                # print(uttid, utt)
                utt = {'utterance_id': uttid, 'speakers': [speakers], 'transcript': utt}
                scenes_data['utterances'].append(utt)
            elif '[Scene' in line:
                c += 1
                t = copy.deepcopy(scenes_data)
                episode_data.append(t)
                scenes_data = {'scene_id': scene_id(s, e, c), 'scenes_name': line, 'utterances': []}
        else:
            if '[Scene' in line or scene_flag < 0:
                c += 1
                scenes_data = {'scene_id': scene_id(s, e, c), 'scenes_name': line, 'utterances': []}
                in_scene = True
    if in_scene and 'scene_id' in scenes_data:
        episode_data.append(scenes_data)
    return episode_data


# htmlfile = open('season/0204.html', 'r', encoding='utf-8')
# htmlhandle = htmlfile.read()
# soup = BeautifulSoup(htmlhandle, "lxml")
# data = soup.findAll(text=True)
# data = [i.strip().replace('\n', ' ') for i in data if i.strip() != '']
# episode_data = parse_p(data, 2, 4)
# print(json.dumps(episode_data))

#
folder = 'season'
jsondata = {}
for filename in os.listdir(folder):
    htmlfile = open(os.path.join(folder, filename), 'r', encoding='utf-8')
    htmlhandle = htmlfile.read()
    htmlhandle = htmlhandle.replace('</b>', '').replace('<b>', '').replace('</strong>', '').replace('<strong>',
                                                                                                    '').replace('</B>',
                                                                                                                '').replace(
        '<B>', '')
    scene_flag = htmlhandle.find('[Scene')
    soup = BeautifulSoup(htmlhandle, "lxml")
    data = soup.findAll(text=True)
    data = [i.strip().replace('\n', ' ') for i in data if i.strip() != '']
    s = int(filename[:2])
    e = int(filename[2:4])
    episode_data = parse_p(data, s, e, scene_flag)
    jsondata[episode_id(s, e)] = episode_data
with open('friends_transcript.json', 'w', encoding='utf-8') as w:
    w.write(json.dumps(jsondata))
print(len(jsondata.keys()))
