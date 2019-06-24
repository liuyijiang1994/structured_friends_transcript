import json

with open('friends_transcript.json', 'r') as f:
    data = json.load(f)
scene_u_len = dict()
e_list = dict()
with open('u.txt', 'w') as w:
    for k, v in data.items():
        e_list[k] = len(v)
        for s in v:
            scene_u_len[s['scene_id']] = len(s['utterances'])
scene_u_len = sorted(scene_u_len.items(), key=lambda item: item[0])
e_list = sorted(e_list.items(), key=lambda item: item[0])
for k, v in e_list:
    print(k, v)

for k, v in scene_u_len:
    print(k, v)
