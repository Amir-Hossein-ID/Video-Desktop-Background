import cv2
import win32gui
import win32api
import win32process
import ctypes
import random
import os
 
ctypes.windll.shcore.SetProcessDpiAwareness(1) # to get correct screen resolutions

def set_video_wallpaper(window_name):
    # win32gui.SystemParametersInfo(20, "", 0) # delete current wallpaper
    window = win32gui.FindWindow(None, window_name)
    parent1 = win32gui.GetDesktopWindow()
    progman = win32gui.FindWindow("Progman", None)

    win32gui.SendMessageTimeout(progman, 0x052C, 0, 0, 0, 1000) # creates a workerW that is behind icons and above default wallpaper
    # to find the newly created workerw, we should find a workerW with shellDll... as a child, then choose its next sibling

    worker = 0
    shell = 0
    while shell == 0:
        worker = win32gui.FindWindowEx(parent1, worker, "WorkerW", None)
        shell = win32gui.FindWindowEx(worker, 0, "SHELLDLL_DefView", None)

    worker = win32gui.FindWindowEx(0, worker, "WorkerW", None)

    old_window = win32gui.FindWindowEx(worker, 0, None, window_name) # destroy the old one if it is present
    while old_window != 0:
        # win32gui.DestroyWindow(old_window)
        # win32gui.SendMessageTimeout(old_window, 0x0002, 0, 0, 0, 1000) # doesn't work because opencv creates the window again, so the old window process should be killed
        pid = win32process.GetWindowThreadProcessId(old_window)
        os.kill(pid[1], 9)
        print('Closed old window')
        old_window = win32gui.FindWindowEx(worker, 0, None, window_name)

    win32gui.SetParent(window, worker)

def resize_video(video_path): # turned out the resizing took a lot of resources and couldn't resize all the time, so resize the video once, use it everytime
    if '_resized' in video_path:
        return video_path

    screen_size =  (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
    new_name = video_path[:video_path.find('.')] + '_resized' + video_path[video_path.find('.'):]

    if os.path.isfile(new_name): # if the video has already been resized
        return new_name

    print('Resizing Video')
    vidcap = cv2.VideoCapture(video_path)
    newvidcap = cv2.VideoWriter(new_name, cv2.VideoWriter_fourcc(*'mp4v'), vidcap.get(cv2.CAP_PROP_FPS), screen_size)
    success, image = vidcap.read()
    count = 0
    while success:
        image = cv2.resize(image, screen_size)
        newvidcap.write(image)
        success,image = vidcap.read()
        if count % 100 == 0:
            print(count, 'frames resized')
        count += 1

    vidcap.release()
    newvidcap.release()
    print('Video Resized')
    return new_name

def framize(video_path):
    video_path = resize_video(video_path)

    cv2.namedWindow('win1', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("win1", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    set_video_wallpaper('win1')

    while True:
        vidcap = cv2.VideoCapture(video_path)
        success, image = vidcap.read()
        while success:
            cv2.imshow('win1', image)
            cv2.waitKey(15)
            success,image = vidcap.read()
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, 0)

if __name__ == '__main__':
    choice = random.choice([i for i in os.listdir() if i.endswith('.mp4')])
    framize(choice)
