import json

with open('friends_transcript.json', 'r') as f:
    data = json.load(f)
with open('u.txt', 'w') as w:
    for k, v in data.items():
        for s in v:
            for u in s['utterances']:
                w.write(u['utterance_id'] + '\t' + u['transcript'] + '\n')
