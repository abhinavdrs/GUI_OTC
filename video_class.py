import PySimpleGUI as sg
import cv2 as cv

class VideoPlayer:
    def __init__(self):
        # Video-File specific data.
        self.filename = None
        self.vidFile = None
        self.num_frames = None
        self.fps = None

        # Layout specific details
        self.layout = [[sg.Text('OpenCV Demo', size=(15, 1), font='Helvetica 20')],
                      [sg.Image(filename='', key='-image-')],
                      [sg.Slider(range=(0, self.num_frames),
                                 size=(60, 10), orientation='h', key='-slider-')],
                      [sg.Button('Exit', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')],
                      [sg.Button('Pause', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')],
                      [sg.Button('Play', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')]]

        self.window = sg.Window('Demo Application - OpenCV Integration', self.layout, no_titlebar=False, location=(0, 0))
        self.image_elem = self.window['-image-']
        self.slider_elem = self.window['-slider-']