#!/usr/bin/env python3

import io, sys, argparse
import json
from random import randint, choice, random

def main(fname, options):
  try:
    fd = io.open(fname, 'r')
    content = fd.read()
    fd.close()
    notes = json.loads(content)
  except BaseException:
    sys.exit("Error loading or parsing the JSON file.")

  group_numbers = max(notes, key=lambda n: n['notes_level'])['notes_level']
  groups = []
  for i in range(group_numbers):
    curr_group = []
    for note in notes:
      if note['notes_level'] == i + 1:
        curr_group.append(note)
    groups.append(curr_group)

  timing_keys = dict()
  target = groups[0]
  prev = target[0]['timing_sec']
  for note in target[1:]:
    curr = note['timing_sec']
    diff = curr - prev
    diff = round(diff, 5)
    if diff in timing_keys:
      timing_keys[diff] += 1
    else:
      timing_keys[diff] = 1
    prev = curr

  new_dict = dict()
  skip = set()
  stt = sorted(timing_keys.keys())
  for i in range(1, len(stt)):
    if i in skip:
      continue
    for j in range(i+1, len(stt)):
      if j in skip:
        continue
      if abs(stt[i] - stt[j]) <= 0.002:
        if stt[i] in new_dict:
          new_dict[stt[i]] += timing_keys[stt[j]]
          skip.add(j)
        elif stt[i] != 0:
          new_dict[stt[i]] = timing_keys[stt[i]]+timing_keys[stt[j]]
          skip.add(j)
    if stt[i] not in new_dict:
      if stt[i] != 0:
        new_dict[stt[i]] = timing_keys[stt[i]]

  total = sum(new_dict.values())
  filtered = dict()
  total = sum(new_dict.values())
  for k, v in new_dict.items():
    if v / total < 0.01:
      continue
    filtered[k] = round(v / total, 3)

  avails = dict()
  for k, v in filtered.items():
    bpm = int(60 / k)
    while bpm < 60:
      bpm *= 2
    while bpm > 250:
      bpm = bpm // 2
    
    success = False
    for i in range(-5, 6):
      if bpm + i in avails:
        avails[bpm + i] += v
        success = True
    if not success:
      avails[bpm] = v

  for k, v in avails.items():
    print("BPM is {0}, with rating {1}".format(k, v))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to a JSON note file.")
    args = parser.parse_args()

    options = set()
    main(args.file, options)