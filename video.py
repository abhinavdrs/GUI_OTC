#!/usr/bin/env python
import PySimpleGUI as sg
from PIL import Image
import cv2 as cv
import io
from time import perf_counter

"""
Demo program to open and play a file using OpenCV
It's main purpose is to show you:
1. How to get a frame at a time from a video file using OpenCV
2. How to display an image in a PySimpleGUI Window
For added fun, you can reposition the video using the slider.
"""


def main():
    # ---===--- Get the filename --- #
    filename = sg.popup_get_file('Filename to play')
    if filename is None:
        return
    vidFile = cv.VideoCapture(filename)
    # ---===--- Get some Stats --- #
    num_frames = vidFile.get(cv.CAP_PROP_FRAME_COUNT)
    fps = vidFile.get(cv.CAP_PROP_FPS)

    sg.theme('Black')

    # ---===--- define the window layout --- #
    layout = [[sg.Text('OpenCV Demo', size=(15, 1), font='Helvetica 20')],
              [sg.Image(filename='', key='-image-')],
              [sg.Slider(range=(0, num_frames),
                         size=(60, 10), orientation='h', key='-slider-')],
              [sg.Button('Exit', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')],
              [sg.Button('Pause', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')],
              [sg.Button('Play', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration', layout, no_titlebar=False, location=(0, 0))

    # locate the elements we'll be updating. Does the search only 1 time
    image_elem = window['-image-']
    slider_elem = window['-slider-']

    # ---===--- LOOP through video file by frame --- #
    cur_frame = 0
    while vidFile.isOpened():
        event, values = window.read(timeout=20)
        if event in ('Exit', None):
            break
        t_0 = perf_counter()
        ret, frame = vidFile.read()
        if not ret:  # if out of data stop looping
            break
        # if someone moved the slider manually, the jump to that frame
        if int(values['-slider-']) != cur_frame - 1:
            cur_frame = int(values['-slider-'])
            vidFile.set(cv.CAP_PROP_POS_FRAMES, cur_frame)
        slider_elem.update(cur_frame)
        cur_frame += 1

        imgbytes = cv.imencode('.png', frame)[1].tobytes()  # ditto
        image_elem.update(data=imgbytes)
        t_1 = perf_counter()
        print(t_1 - t_0)

        if event == 'Pause':
            while event != 'Play':
                event, values = window.read(timeout=20)

                if int(values['-slider-']) != cur_frame - 1:
                    ret, frame = vidFile.read()

                    if not ret:  # if out of data stop looping
                        break

                    cur_frame = int(values['-slider-'])
                    vidFile.set(cv.CAP_PROP_POS_FRAMES, cur_frame)

                    slider_elem.update(cur_frame)
                    cur_frame += 1

                    imgbytes = cv.imencode('.png', frame)[1].tobytes()  # ditto
                    image_elem.update(data=imgbytes)



main()


"""
print(t_1 - t_0) values
0.03816360700000043
0.035159134999999786
0.03400266099999971
0.03761172499999965
0.03897140900000018
0.036519763999999455
0.040657064000000354
0.04163844600000033"""