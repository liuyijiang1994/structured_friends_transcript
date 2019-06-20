import re

speaker1 = '<p><strong>(.+)</strong>:'
speaker2 = '<p><b>(.+):</b>'

speaker_regex_1 = re.compile(speaker1)
speaker_regex_2 = re.compile(speaker2)

results = speaker_regex_1.findall(
    '''<p><strong>Monica</strong>: Whoa-whoa-whoa, Phoebe you gotta take her! Y’know, I-I-I said some really bad stuff about her, but y’know Rachel has some good qualities that make her a good roommate. She gets tons of catalogs and umm, she’ll fold down the pages of the things she thinks that I’d like.</p>''')
print(results)
