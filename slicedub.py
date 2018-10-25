#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import re
import string
import wave
import pyaudio

# Thanks to schauerlich@ubuntuforums. https://ubuntuforums.org/showthread.php?t=1882580
def slice(infile, outfilename, start_ms, end_ms):
    width = infile.getsampwidth()
    rate = infile.getframerate()
    fpms = int(rate / 1000) # frames per ms
    length = int(end_ms - start_ms) * fpms
    start_index = start_ms * fpms

    out = wave.open(outfilename, "w")
    out.setparams((infile.getnchannels(), width, rate, length, infile.getcomptype(), infile.getcompname()))
    
    infile.rewind()
    anchor = infile.tell()
    infile.setpos(anchor + start_index)
    out.writeframes(infile.readframes(length))

os.system("cls")
print ("SDLPal Voice Dub WAV Slice Tool v1.01 by PalMusicFan \n")
print ("Powered by Python 3 on Microsoft Windows and PyAudio.")
print ("Thanks to schauerlich@ubuntuforums.")
print ("https://ubuntuforums.org/showthread.php?t=1882580 \n")
print ("Please confirm dub.txt and dub.wav are here. \n")
os.system("pause")

file = open("dub.txt", encoding="utf8")
matchObj = re.compile( r'\[BEGIN MESSAGE\](.*)')
fileName=""
idx=""
subIdx=0
line="Start!"

infile = wave.open("dub.wav", "r")

start = 0
end = 0

wf = wave.open("dub.wav", "rb")

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    
    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)


# start the stream (4)
stream.start_stream()

base = stream.get_time()
lines = file.readlines()

i = 0
linesCount = 0
isMessageContent = 0

while i < len(lines):
	if lines[i].find("[BEGIN MESSAGE]") != -1:
		isMessageContent = 1
		linesCount = 0
	elif lines[i].find("[END MESSAGE]") != -1:
		isMessageContent = 0

	if isMessageContent == 1:
		if linesCount >= 4:
			linesCount = 0
			if lines[i].find("[CLEAR MESSAGE]") == -1 and lines[i].find("[BEGIN MESSAGE]") == -1 and lines[i].find("[END MESSAGE]") == -1:
				lines.insert(i, "[CLEAR MESSAGE]")
		else:
			if lines[i].find("[CLEAR MESSAGE]") == -1 and lines[i].find("[BEGIN MESSAGE]") == -1 and lines[i].find("[END MESSAGE]") == -1:
				if lines[i].replace("\n", "") != "" and lines[i].replace("\n", "")[-1] != "：" and lines[i].replace("\n", "")[-1] != ":":
					linesCount = linesCount + 1
	i = i + 1

	
isMessageContent = 0
	
for index in range(len(lines)):
	line=lines[index]
	if line.find("[BEGIN MESSAGE]") != -1:
		isMessageContent = 1
		linesCount = 0
	elif line.find("[END MESSAGE]") != -1:
		isMessageContent = 0
		
	if isMessageContent == 1:

		m = matchObj.match(line)
		if m is None:
			if line.find("[CLEAR MESSAGE]") != -1:
				subIdx += 1
				fileName = idx + "_" + str("%02d" % subIdx) + ".wav"
				os.system("cls")
				print ("Ready to save " + fileName)
				
				tmpIndex = 1
				while lines[index + tmpIndex].find("[CLEAR MESSAGE]") == -1 and lines[index + tmpIndex].find("[END MESSAGE]") == -1:
					print(lines[index + tmpIndex])
					
					
					tmpIndex = tmpIndex + 1
					
				os.system("pause")
				
				start = end
				end = int((stream.get_time() - base) * 1000)
				slice(infile, fileName, start, end)
				print ("Sliced at " + str(end)) # seconds

		else:
			subIdx = 0
			idx = m.group(1).strip().zfill(5)
			fileName = idx + "_" + str("%02d" % subIdx) + ".wav"
			os.system("cls")
			print ("Ready to save " + fileName)
			
			tmpIndex = 1
			while lines[index + tmpIndex].find("[CLEAR MESSAGE]") == -1 and lines[index + tmpIndex].find("[END MESSAGE]") == -1:
				print(lines[index + tmpIndex])
				tmpIndex = tmpIndex + 1
				
			os.system("pause")
			
			start = end
			end = int((stream.get_time() - base) * 1000)
			slice(infile, fileName, start, end)
			print ("Sliced at " + str(end)) # seconds

			
			
			
