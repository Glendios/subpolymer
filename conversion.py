import tkinter as tk
from tkinter import *
import pysrt
import subprocess
import json
import pinyin_jyutping_sentence

#！ todo
    # add option to add sub to above instead of below
        # would need to not concatenate
# print(pinyin_jyutping_sentence.pinyin("高兴"))
# print(pinyin_jyutping_sentence.pinyin("gaoxing"))
# print(pinyin_jyutping_sentence.pinyin("高兴gaoxing"))
# print(pinyin_jyutping_sentence.pinyin("高兴 gaoxing"))

def srt_index_fixer(subfile):
    #subfile = pysrt.open(subfile, encoding='utf-8')
    subfile.sort(key=lambda x: x.start)

    for idx, sub in enumerate(subfile, start=1):
        sub.index = idx
    return subfile
    #subs.save(out_subfile, encoding='utf-8')

def srt_time_convert(time):
     return (time.hours * 3600 + time.minutes * 60 + time.seconds)*1000 + time.milliseconds

def srt_timecheck(time1, time2):
     #print(f"{srt_time_convert(time1)} , {srt_time_convert(time2)}")
     return srt_time_convert(time2)-srt_time_convert(time1)
        
def compare_merge_srt(small_sub, big_sub, output_file):
    output_file = 'mergetestxiao.srt'

    #take subs 
    #use sub.start sub.end
    #double pointer search through arranged lists 
    i, j = 0, 0
    len1, len2 = len(small_sub), len(big_sub)
    #len1, len2 = 16, 16
    flag_move_on = False
    #print(small_sub[0].text)
    #print(big_sub[0].text)

    while i < len1:
        subber1 = small_sub[i]
        while j < len2:
            subber2 = big_sub[j]
            #print(srt_timecheck(subber1.start, subber2.start))

            #backcheck if proper sub was skipped due to finding match
            #! may need more backchecks or a logic redo if subs are coded strange#
            if 500 > abs(srt_timecheck(subber1.end, big_sub[j-1].end)):
                #print(f"match found, concat start: {srt_timecheck(subber1.start, subber2.start)}")
                #print(f"match found, concat end: {srt_timecheck(subber1.end, subber2.end)}")
                #print(f"backcheck concat subber1: {subber1.text}")
                #print(f"backcheck concat subber2: {big_sub[j-1].text}")
                #concat to sub2
                big_sub[j-1].text = big_sub[j-1].text + '\n' + subber1.text
                break
            if 500 > abs(srt_timecheck(subber1.end, big_sub[j-2].end)):
                #print(f"match found, concat start: {srt_timecheck(subber1.start, subber2.start)}")
                #print(f"match found, concat end: {srt_timecheck(subber1.end, subber2.end)}")
                #print(f"2backcheck2 concat subber1: {subber1.text}")
                #print(f"2backcheck2 concat subber2: {big_sub[j-2].text}")
                #concat to sub2
                big_sub[j-2].text = big_sub[j-2].text + '\n' + subber1.text
                break
        
            #only 2 actions:
            #if under error concat to bigsubs
            #if over error add as new entry to bigsubs
            elif 50000 < srt_timecheck(subber1.start, subber2.start):
                ##! same functionality as else##
                ##separate logic only to confirm large timing outliers##

                #add to sub2
                big_sub.insert(j, subber1)
                j+=1

                #print(srt_timecheck(subber1.start, subber2.start))
                print(f"doesnt exist, adding: {srt_timecheck(subber1.start, subber2.start)}")
                print(f"subber1: {subber1.text}")
                #print(f"subber2: {subber2.text}")
                #i+=1
                
                #print(f"differecne extreme, adding :{subber1.text} to target")
                break
            elif 500 > abs(srt_timecheck(subber1.start, subber2.start)) or 500 > abs(srt_timecheck(subber1.end, subber2.end)):
                #print(f"match found, concat start: {srt_timecheck(subber1.start, subber2.start)}")
                #print(f"match found, concat end: {srt_timecheck(subber1.end, subber2.end)}")
                #print(f"concat subber1: {subber1.text}")
                #print(f"concat subber2: {subber2.text}")
                #concat to sub2
                subber2.text = subber2.text + '\n' + subber1.text
                #if concatenated, move to next big sub entry
                j+=1
                break
            else:
                #! same functionality as extreme error, add to sub
                big_sub.insert(j, subber1)
                j+=1

                print(f"error between .5s and 50s: {srt_timecheck(subber1.start, subber2.start)}")
                print(f"means too big so ill add go to next smallsub subber1: {subber1.text}")
                #print(f"subber2: {subber2.text}")

                break
        i+=1
    big_sub = srt_index_fixer(big_sub)
    big_sub.save(output_file,encoding='utf-8')

    #if timer matches with error of :00,05
    # add to subtitle
    # if timers mismatch, add to whichever doesnt have
    # at end fix numbering of timers
        #if previous line is SOF or empty, and current line is an int
        #assign number and enumerate through file
     

def modify_function(text):
        # Example modification: add a prefix to each dialogue line
        lines = text.split('\n')
        print(lines)
        modified_lines = [pinyin_jyutping_sentence.pinyin(line) for line in lines]
        return '\n'.join(modified_lines)

def extract_dialogue_from_srt(srt_file, kor_srt):
    dialogue_parts = []
    # Load the SRT file
    subs_kor = pysrt.open(kor_srt, encoding='utf-8')
    subs = pysrt.open(srt_file, encoding='utf-8')

    for sub in subs:
    #for sub, subs_kor in zip(subs, subs_kor):
        #print(f"start: {subs_kor.start} --> end: {subs_kor.end}")
        print(f"start: {sub.start} --> end: {sub.end}")
        original_text = sub.text
        modified_text = modify_function(original_text)
        sub.text = modified_text + '\n' + original_text
    output_file = 'modified_xiaoOutTest.srt'
    subs.save(output_file,encoding='utf-8')
    compare_merge_srt(subs_kor, subs, output_file)

        # # Print a separator after each subtitle
        # print("-" * 20)
    # # Extract dialogue parts
    # for sub in subs:
    #     print(sub)
    #     #dialogue_parts.append(sub.text.strip())
    #     dialogue_parts.append(sub)
    # return dialogue_parts
    # for text in subtitle_texts:
    #     print(text)

# Example usage
srt_file = 'mdzsZ.srt'
kor_sub = 'mdzsK.srt'
output_file = 'modified_xiaoOutTest.srt'
extract_dialogue_from_srt(srt_file, kor_sub)



subs = pysrt.open("mdzsZ.srt")
subs_kor = pysrt.open("mdzsK.srt")

#for sub in subs:
    #print(sub.text)
    #print()