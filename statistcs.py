#!/usr/bin/env python

import json
from enum import OrderedDict
from pprint import pprint
from socialmediaparse import EmojiDict
with open('result.json') as f:
    data = json.load(f)

messages_per_person = OrderedDict()
for message in data['messages']:
	if message['type'] == "message":
		key = None
		message_type = 'text'
		message_value = None
		if 'from' in message.keys():
			key = message['from']
		elif 'actor' in message.keys():
			key = message['actor']
		else:
			print(message)

		if 'media_type' in message.keys() and message['media_type'] == 'sticker':
			message_type = 'sticker'
			message_value = message['sticker_emoji']

		if not key in messages_per_person:
			messages_per_person[key] = []

		messages_per_person[key].append({
			'date': message['date'],
			'message_type': message_type,
			'message_value': message_value,
			})

print([(y,len(x)) for y,x in messages_per_person.items()])
stickers_use = {}
rel_stickers_use = {}
stickers = {}
emoji_list = []

for person, messages in messages_per_person.items():
	tmp_sticker = None
	tmp_sticker = EmojiDict()
	tmp_sticker.clear()
	sticker = []
	sticker_use = 0
	for message in messages:
		if message['message_type'] == 'sticker':
			tmp_sticker.add_emoji_count(message['message_value'])
			sticker_use += 1

	for k in sorted(tmp_sticker.dict, key=tmp_sticker.dict.get, reverse=True):
		if tmp_sticker.dict[k] > 0:
			if not k in emoji_list:
				emoji_list.append(k)

			sticker.append((k, tmp_sticker.dict[k]))

	stickers_use[person] = sticker_use #/len(messages)
	rel_stickers_use[person] = sticker_use /len(messages)
	stickers[person] = sticker


print("Name, Total use, Rel use, %s" % ', '.join(emoji_list))
for k in sorted(stickers_use, key=stickers_use.get, reverse=True):
	emojis = sorted(stickers[k], key=lambda tup: tup[1], reverse=True)
	emojis = ""

	for key in emoji_list:
		key_found = False
		for v, count in stickers[k]:
			if key == v:
				key_found = True
				emojis += "%d," % count
		if not key_found:
			emojis += "%d," % 0

	print("%s, %d, %f, %s" % (k, stickers_use[k], rel_stickers_use[k], emojis))