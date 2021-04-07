# fixing the layout specified has already being used
# https://github.com/PySimpleGUI/PySimpleGUI/issues/2957
# %%
# Draw image using graph object:
# https://stackoverflow.com/questions/57191494/draw-rectangle-on-image-in-pysimplegui
import PySimpleGUI as sg
import cv2 as cv



# %%
class VideoPlayer(sg.Frame):
    def __init__(
            self,
            title="Video player",
            title_color=None,
            background_color=None,
            title_location=None,
            relief=None,
            size=(None, None),
            font=None,
            pad=None,
            border_width=None,
            key=None,
            k=None,
            tooltip=None,
            right_click_menu=None,
            visible=None,
            element_justification=None,
            vertical_alignment=None,
            metadata=None,

    ):
        # Initialize with a static layout instead of forcing to pass a custom layout

        self.num_frames = 50
        # removed init_layout() by setting self.layout to empty list
        # self.init_layout()

        # Add some VideoPlayer specific attributes
        self.play = False
        self.vidframe_no = 0
        self.layout = []

        # self.height = 100
        # self.width = 100

        # Inherit instantiation from parent class
        super().__init__(
            title,
            layout=self.layout,
            title_color=title_color,
            background_color=background_color,
            title_location=title_location,
            relief=relief,
            size=size,
            font=font,
            pad=pad,
            border_width=border_width,
            key=key,
            k=k,
            tooltip=tooltip,
            right_click_menu=right_click_menu,
            visible=visible,
            element_justification=element_justification,
            vertical_alignment=vertical_alignment,
            metadata=metadata,
        )

        # getter and setter for width and height

    def set_height_width(self, width, height):
        self.height = height
        self.width = width
        return True

    def get_height_width(self):
        width = self.width
        height = self.height
        return width, height

    def init_layout(self):
        """Static VideoPlayer layout for initialization"""
        # self.set_height_width(200, 200)
        width, height = self.get_height_width()
        print("from init layout", width, height)
        self.graph_vidframe = sg.Graph(
            canvas_size=(width, height),
            graph_bottom_left=(0, 0),
            graph_top_right=(width, height),
            key="graph_vidframe",
        )

        self.button_play = sg.B(
            "Play", key="button_play"
        )
        self.button_pause = sg.B(
            "Pause", key="button_pause"
        )
        self.slider_vidframe = sg.Slider(range=(0, self.num_frames),
                                         orientation="h", size=(self.width, 10), key="slider_vidframe"
                                         )
        self.layout = [
            [self.graph_vidframe],
            [self.button_play, self.button_pause],
            [self.slider_vidframe],
        ]
        return self.layout

    # Initialize the video
    def browse_video(self):
        self.filename = sg.popup_get_file(' Browse Filename to Play')

    # Load video
    def load_video(self):
        # Open video capture object
        self.vidFile = cv.VideoCapture(self.filename)

        # Populate video paramaters
        self.num_frames = self.vidFile.get(cv.CAP_PROP_FRAME_COUNT)
        self.fps = self.vidFile.get(cv.CAP_PROP_FPS)
        width = self.vidFile.get(cv.CAP_PROP_FRAME_WIDTH)
        height = self.vidFile.get(cv.CAP_PROP_FRAME_HEIGHT)
        # set self.width and self.height >> To be fixed! why massive GUI ?
        self.set_height_width(width, height)
        return [self.vidFile, self.num_frames, self.fps]

    def events(self, event, values, window, shapes=None, shape_mode=None):
        """Video Player events to handle when called from the event loop of the window
        where VideoPlayer is embedded.
        Args:
            event ([type]): [description]
            values ([type]): [description]
            shapes ([type], optional): [description]. Defaults to None.
            shape_mode ([type], optional): [description]. Defaults to None.
            :param window: <class 'PySimpleGUI.PySimpleGUI.Window'>
        """
        print("Hi from inside video player event loop!")
        if True:
            while True:
                graph = window.Element("graph_vidframe")
                ret, frame = self.vidFile.read()
                imgbytes = cv.imencode('.png', frame)[1].tobytes()
                figure_id = graph.DrawImage(data=imgbytes, location=(0, self.height))
                print("DrawImage returned", figure_id)
                self.play = True
        elif event == "button_pause":
            self.play = False
        elif event == "slider_vidframe":
            self.vidframe_no = values["slider_vidframe"]
            print("Jump to frame {​}​".format(self.vidframe_no))
        if self.play and not event == "slider_vidframe":
            self.vidframe_no += 1
            print("Play next frame {​}​".format(self.vidframe_no))

    def draw_shapes(self):
        pass

    def show_new_frame(self):
        pass


# %%
# Create a window and embed the video player element
# Create instance of VideoPlayer class
MyVideoPlayer = VideoPlayer("My embedded video player", key="my_video_player")

# Browse Video
MyVideoPlayer.browse_video()

# Populate video paramaters and set width and height
MyVideoPlayer.load_video()

# Initialize layout
vid_layout = MyVideoPlayer.init_layout()

# Define layout including that instance of VideoPlayer class
# window_layout_1 = [
#     [sg.Text("Some stuff above video player")],
#     [sg.Text("Some other stuff below video player")]
# ]

# Add both layouts
# window_layout = vid_layout + window_layout_1
window_layout = vid_layout

# Create the window
window = sg.Window(title="My window with embedded video player", layout=window_layout)

# Enter event loop
while True:
    event, values = window.read(timeout=10)
    # Window-related events
    if event == sg.WINDOW_CLOSED or event == "Quit":
        break
    # VideoPlayer related events
    MyVideoPlayer.events(event=event, values=values, window=window)
# Close window
window.close()
#
# Is VideoPlayer is subclass of sg.Frame and MyVideoPlayer is instance of VideoPlayer?
print(issubclass(VideoPlayer, sg.Frame))
print(isinstance(MyVideoPlayer, VideoPlayer))

# use graph object to show image
# display them
#
