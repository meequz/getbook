#! /usr/bin/env python3
# coding: utf-8
import sys

import requests
import lxml.html
from lxml.cssselect import CSSSelector


# get page
url = sys.argv[1]
page = requests.get(url).text
page = page.replace('\xa0', ' ')
tree = lxml.html.fromstring(page)


# get title
title_tag = CSSSelector('div#main h1')(tree)[0]
title = title_tag.text_content()
fb2 = title.find(' (fb2)')
if fb2 != -1:
    title = title[:fb2]


# get text
text_tag = CSSSelector('div#main div._ga1_on_')(tree)[0]
text = text_tag.text_content().strip()


# get refs
ref_sup_tags = CSSSelector('sup')(text_tag)
ref_tags = [CSSSelector('a')(ref_sup_tag)[1] for ref_sup_tag in ref_sup_tags]
refs = [ref_tag.get('title').strip() for ref_tag in ref_tags]


# fill the refs
template = '[{}]'
i = 1
ref_marker = template.format(i)
while text.find(ref_marker) != -1:
    text = text.replace(ref_marker, template.format(refs[i-1]))
    i += 1
    ref_marker = template.format(i)


# write to file
with open (title+'.txt', 'w') as f:
    f.write(text)
