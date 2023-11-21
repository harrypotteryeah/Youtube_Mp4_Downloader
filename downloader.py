import pytube as py
import os
import pyperclip
import keyboard
from concurrent.futures import ThreadPoolExecutor
from tkinter import filedialog,Tk
import time
download_mp4=True #If False will download mp3
video_quality='360p'
use_clipboard=False#If False urls will get loaded from the text file

#Get the folder to put the downloaded files in
Tk().withdraw() 
OUTPUT_PATH = filedialog.askdirectory(initialdir=os.path.abspath(os.getcwd()))

#Get the list of urls of the files you want to download
if use_clipboard:#Adds every text you copy into the list
    url_list=[]
    while not keyboard.is_pressed('enter'):#Press enter to stop adding urls and start downloading
        try:
            pyperclip.waitForNewPaste(timeout=1)
            copied_text=pyperclip.paste()
            url_list.append(copied_text)
            print(copied_text)
        except pyperclip.PyperclipTimeoutException:
            pass
else:
    with open("Video_Urls.txt","r+") as f:
        url_list=list(filter(lambda x:x!="" and x[0]!='#',map(lambda x:x.strip(" \t\n"),f.readlines())))


new_url_list=[]
for url in url_list:
    if '?si=' in url:
        url=url[:url.find('?si=')]#Remove the extra part of the link used for sharing
    if not url in new_url_list:
        new_url_list.append(url)#Remove any duplicates
url_list=new_url_list

def download_video(url):
    try:
        yt = py.YouTube(url)
        #Change the filters acording to download_mp4 variable
        video = yt.streams.filter(only_audio=not download_mp4,res=video_quality if download_mp4 else None).first()
        out_file= video.download(output_path=OUTPUT_PATH)
        base, ext = os.path.splitext(out_file)
        new_file_name = base + '.mp4' if download_mp4 else 'mp3'
        os.rename(out_file, new_file_name)
        print(f"Downloaded {new_file_name}\n")
    except:
        print(f"Error while downloading {url}")

print(f"Started downloading {len(url_list)} files")
start_time=time.time()
with ThreadPoolExecutor() as executor:#Using multiple threads to speed up downloading
    for url in url_list:
        executor.submit(download_video,url) 

    
print(f"Finished downloading {len(url_list)} files in {time.time()-start_time} seconds")
