
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import packages
import csv
import math
import glob
from os import listdir
from os.path import isfile, join
import re


mypath = "D:\\PROJECT\\upwork\\python\\vtt"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

m = re.compile(r"\<.*?\>")  # strip/remove unwanted tags


def clean(content):
    new_content = m.sub('', content)
    new_content = new_content.replace('align:start position:0%', '')
    new_content = new_content.replace('-->', '')
    return new_content


def clean_time(time):
    times = time[0].split('.')
    return times[0] + ":" + str(math.floor(int(times[1]) / 40)).zfill(2)


for filename in onlyfiles:

    filepath = mypath + "\\" + filename
    opened_file = open(filepath, encoding='utf8')
    content = opened_file.read()
    segments = content.split('\n\n')  # split on double line

    new_segments = [clean(s) for s in segments if len(s) != 0][2:]

    trimmed_segments = []
    count = 1
    for segment in new_segments:
        split_segment = segment.split()
        time_code_in = split_segment[0],
        time_code_out = split_segment[1],
        text = ' '.join(segment.split()[2:])
        trimmed_segment = (str(filename)[:-2], count, clean_time(time_code_in),
                           clean_time(time_code_out), time_code_in[0].replace(".", ","), time_code_out[0].replace(".", ","), text)
        trimmed_segments.append(trimmed_segment)
        count += 1

    # write output as csv file

    with open(mypath + "\\" + str(filename)[:-3]+'csv', 'w', encoding='utf8', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(["id", "No", "Timecode In", "Timecode Out",
                            "Timecode IN(milliseconds)", "Timecode Out(milliseconds)", "Subtitle"])
        for line in trimmed_segments:
            thewriter.writerow(line)
