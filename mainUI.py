#for chinese + eng sub => cn + pinyin + eng track

import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import conversion
import pysrt
import subprocess
import json

#!todo
    # assign functions to button
    #1：extract sub from mkv
    #2: use srt/ass manually

    # checkbox
        #function 1: merge 2 files
        #function 2: pinyin add (chinese specific)
                                                            #function 3: hiragana katakana add, not interested atm
    #output:
        #1: srt
            # track 1: put on top/below
            # track 2: put on top/below
        #2: ass
            # -> conversyion.py update:
                #pinyin: put as smaller text on top of chinese characters
                #possibly add extra space between CN lines to have space for pinyin
                #or add directly on top of CN chars if possible
            # track 1: put on top/below
            # track 2: put on top/below

    #text box1: chinese srt
    #text box2: srt to add in
        # make box gray/hide if merge is not selected

    #text box3: output filename (automate based on options selected)
        #Auto button: suggest name automatically based on selected options

    # on function call assign to variable being passed to function
    # check for overwrite if filename exists

    

# import sys
# sys.stdout.reconfigure(encoding='utf-8')  # For Windows, GBK encoding
print("你好，世界！")

def extract_subtitle(input_file, output_file, track_number):
    # Run mkvmerge command to extract subtitle track
    cmd = ['mkvextract', 'tracks', input_file, f'{track_number}:{output_file}']
    #cmd = ['mkvmerge', '-o', output_file, '--subtitle-tracks', str(track_number), input_file]
    
    # Execute the command
    try:
        subprocess.run(cmd, check=True)
        print(f"Subtitle track #{track_number} extracted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting subtitle track #{track_number}: {e}")

input_file = 'xiao1.mkv'
output_file = 'xiaoOutTest.srt'
extract_subtitle(input_file, output_file, 4)


def extract_dialogue_from_srt(srt_file):
    dialogue_parts = []

    # Load the SRT file
    subs = pysrt.open(srt_file, encoding='utf-8')

    for sub in subs:
        # Print the start and end time of the subtitle
        print(f"Start: {sub.start} --> End: {sub.end}")
        
        # Print the subtitle text line by line
        lines = sub.text.split('\n')
        for line in lines:
            print(line)

        # Print a separator after each subtitle
        print("-" * 20)
    return
    # Extract dialogue parts
    for sub in subs:
        print(sub)
        #dialogue_parts.append(sub.text.strip())
        dialogue_parts.append(sub)
    return dialogue_parts
    for text in subtitle_texts:
        print(text)

# Example usage
srt_file = 'xiaoOutTest.srt'
subtitle_texts = extract_dialogue_from_srt(srt_file)

# Print the extracted subtitle texts
print("hello?")


def extract_subtitle_track(input_file, output_file, language_code):
    # Construct the mkvextract command to extract the specific language subtitle track
    cmdCNextract = ['mkvextract', 'tracks', input_file, f'0:{output_file}', f'subtitles_{language_code}.srt']
    
    # Run the command
    result = subprocess.run(cmdCNextract, capture_output=True, text=True)
    
    # Check if the command ran successfully
    if result.returncode == 0:
        print(f"Subtitle track in language '{language_code}' extracted successfully.")
    else:
        print(f"Error extracting subtitle track: {result.stderr}")


def extract_chinese_track(subtitle_tracks):
    #subtitle_tracks

    for track in subtitle_tracks:
        #print("counting track")
        properties = track.get('properties', {})
        language = properties.get('language', '')
        track_name = properties.get('track_name', '')

        #print(language)
        if 'chi' in language.lower():
            print(f"track found")
        if 'chi' in track['properties'].get('language'):
            if 'implified' or '简体' in track.get('properties',{}).get('track_name'):
                print(f"Track found")                
                print(track_name + ' ' + str(track['id']))
                return track['id']
            print(f"track found")
            print(track_name + ' ' + str(track['id']))
            return track['id']
        else:
            print("nah not found")
        
#[{'codec': 'SubStationAlpha', 'id': 2, 'properties': {'codec_id': 'S_TEXT/ASS', 'codec_private_data': '', 'codec_private_length': 2249, 'default_track': True, 'enabled_track': True, 'encoding': 'UTF-8', 'forced_track': False, 'language': 'eng', 'minimum_timestamp': 0, 'num_index_entries': 85, 'number': 3, 'text_subtitles': True, 'track_name': 'English', 'uid': 462745026940914277}, 'type': 'subtitles'}, {'codec': 'SubStationAlpha', 'id': 3, 'properties': {'codec_id': 'S_TEXT/ASS', 'codec_private_data': '', 'codec_private_length': 2251, 'default_track': False, 'enabled_track': True, 'encoding': 'UTF-8', 'forced_track': False, 'language': 'hun', 'minimum_timestamp': 0, 'num_index_entries': 
#86, 'number': 4, 'text_subtitles': True, 'track_name': 'Magyar (Hungarian)', 'uid': 17243306552787917594}, 'type': 'subtitles'}, {'codec': 'SubStationAlpha', 'id': 4, 'properties': {'codec_id': 'S_TEXT/ASS', 'codec_private_data': '', 'codec_private_length': 1473, 'default_track': False, 'enabled_track': True, 'encoding': 'UTF-8', 'forced_track': False, 'language': 'chi', 'minimum_timestamp': 0, 'num_index_entries': 73, 'number': 5, 'text_subtitles': True, 'track_name': '汉语（简体）(Chinese (Simplified))', 'uid': 4468965953380107694}, 'type': 'subtitles'}]


def get_subtitle_tracks(mkv_file):
    cmd = ['mkvmerge', '-J', mkv_file]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode != 0:
        print(f"Error running command: {result.stderr}")
        return None
    
    if result.stdout is None:
        print("No output received from command.")
        return None
    
    try:
        info = json.loads(result.stdout)
        tracks = info['tracks']
        subtitle_tracks = [track for track in tracks if track['type'] == 'subtitles']
        return subtitle_tracks
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

# Example usage
mkv_file_path = 'xiao1.mkv'
subtitle_tracks = get_subtitle_tracks(mkv_file_path)
extract_chinese_track(subtitle_tracks)

if subtitle_tracks:
    print("Subtitle tracks found:")
    for track in subtitle_tracks:
        print(f"Track ID: {track['id']}, Track Type: {track['properties']['track_name']}, Language: {track['properties']['language']}")

def file_browse(browse_box):
    #file = filedialog.askopenfile(mode='r')
    filename = filedialog.askopenfilename()
    if filename:
        browse_box.delete(0,tk.END)
        browse_box.insert(0,filename)

    #get extension
    #if mkv dont doubt mkv
        #set mkv flag?
    #if srt doubt
        #open file and check if ass
    #if ass doubt
        #open file and check if ass

    return

m = tk.Tk()
m.minsize(500,600)
m.title('SubtitlePolymer - Subtitle Merger + Pinyin adder')

master = m

#def load subtitle from filename function
#autorun if browsed
#manual click if path paste


#if manual
#row 1
Label(master, text='Chinese ass/srt/mkv').grid(row=0)
file_master_box = Entry(master)
file_master_box.grid(row=0,column=1, padx=5, pady=0)
button_master_file = tk.Button(m, text='...',command = lambda: file_browse(file_master_box)) 
button_master_file.grid(row=0,column=3, padx=0, pady=0)

#row 2
Label(master, text='Subtitle Tracks:\n\nChoose main sub\nto merge into').grid(row=1)
subScrollCN = Scrollbar(m)
subScrollCN.grid(row=1,column=2)
mylist = Listbox(m, yscrollcommand=subScrollCN.set)
subListBoxCN = Listbox()
subListBoxCN.grid(row=1,column=1)
subScrollCN.config(command=subListBoxCN.yview)

#row 3
file_second_box = Entry(master)
file_second_box.grid(row=2,column=1, padx=5, pady=0)
button_second_file = tk.Button(m, text='...',command = lambda: file_browse(file_second_box)) 
button_second_file.grid(row=2,column=3, padx=0, pady=0)

buttonEN = tk.Button(m, text='...',command = file_browse)
Label(master, text='English ass/srt/mkv').grid(row=2)
buttonEN.grid(row=1,column=3, padx=0, pady=0)


m.mainloop()


#ui with drag functionality
#box 1
#on drag:
#detect subtitles and list them
#ask user for which sub is chinese
#if multi
    #have checkbox for correct sub number

#checkbox 
#if eng sub im same mkv, disable box2
#ask user for which sub is english
    #if multi have checkbox for correct sub number

#box 2
#drag mkv or srt
#if mkv, do extraction into srt
#if srt, use srt directly

#extract chinese srt
#convert each chinese line to pinyin
#make pinyin srt
#shift pinyin +20px of chinese
#eng xy = +20px of pinyin
#recombine all srt into one