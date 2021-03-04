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
        self.layout = None

        self.window = None
        self.image_elem = None
        self.slider_elem = None
        self.theme = sg.theme('Black')

        # logic variables
        self.cur_frame = 0

    def browse_video(self):
        self.filename = sg.popup_get_file(' Browse Filename to Play')

    # Initialize the openCV VideoCapture function and populate video statistics
    def get_video(self):
        self.vidFile = cv.VideoCapture(self.filename)
        self.num_frames = self.vidFile.get(cv.CAP_PROP_FRAME_COUNT)
        self.fps = self.vidFile.get(cv.CAP_PROP_FPS)
        return [self.vidFile, self.num_frames, self.fps]

    def video_layout(self):
        self.layout = [[sg.Text('OpenCV Demo', size=(15, 1), font='Helvetica 20')],
                       [sg.Image(filename='', key='-image-')],
                       [sg.Slider(range=(0, self.num_frames),
                                  size=(60, 10), orientation='h', key='-slider-')],
                       [sg.Button('Exit', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')],
                       [sg.Button('Pause', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')],
                       [sg.Button('Play', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')]]
        return self.layout

    def video_window(self):
        self.window = sg.Window('Demo Application - OpenCV Integration', self.layout, no_titlebar=False,
                                location=(0, 0))
        self.image_elem = self.window['-image-']
        self.slider_elem = self.window['-slider-']

    def show_video(self):
        while self.vidFile.isOpened():
            event, values = self.window.read(timeout=20)
            if event in ('Exit', None):
                break
            ret, frame = self.vidFile.read()
            if not ret:  # if out of data stop looping
                break
            # if someone moved the slider manually, the jump to that frame
            if int(values['-slider-']) != self.cur_frame - 1:
                self.cur_frame = int(values['-slider-'])
                self.vidFile.set(cv.CAP_PROP_POS_FRAMES, self.cur_frame)
            self.slider_elem.update(self.cur_frame)
            self.cur_frame += 1

            imgbytes = cv.imencode('.png', frame)[1].tobytes()  # ditto
            self.image_elem.update(data=imgbytes)

            if event == 'Pause':
                while event != 'Play':
                    event, values = self.window.read(timeout=20)

                    if event in ('Exit', None):
                        exit()

                    if int(values['-slider-']) != self.cur_frame - 1:
                        ret, frame = self.vidFile.read()

                        if not ret:  # if out of data stop looping
                            break

                        self.cur_frame = int(values['-slider-'])
                        self.vidFile.set(cv.CAP_PROP_POS_FRAMES, self.cur_frame)

                        self.slider_elem.update(self.cur_frame)
                        self.cur_frame += 1

                        imgbytes = cv.imencode('.png', frame)[1].tobytes()  # ditto
                        self.image_elem.update(data=imgbytes)
