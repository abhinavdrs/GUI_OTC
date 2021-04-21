import PySimpleGUI as sg
import cv2 as cv


# %%
class VideoPlayer(sg.Frame):
    def __init__(
            self,
            title="Video player",
            # title_color=None,
            # background_color=None,
            # title_location=None,
            # relief=None,
            # size=(None, None),
            # font=None,
            # pad=None,
            # border_width=None,
            # key=None,
            # k=None,
            # tooltip=None,
            # right_click_menu=None,
            # visible=None,
            # element_justification=None,
            # vertical_alignment=None,
            # metadata=None,

    ):
        # Initialize with a static layout instead of forcing to pass a custom layout

        self.num_frames = 50
        # removed init_layout() by setting self.layout to empty list
        # self.init_layout()

        # Add some VideoPlayer specific attributes
        self.play = False
        self.vidframe_no = 0
        self.layout = []

        self.height = 100
        self.width = 100

        # Store all possible events of Video player in this list
        self.event_list =["button_play", "button_pause", "slider_vidframe" ]

        # Inherit instantiation from parent class
        super().__init__(
            title,
            layout=self.layout,
            # title_color=title_color,
            # background_color=background_color,
            # title_location=title_location,
            # relief=relief,
            # size=size,
            # font=font,
            # pad=pad,
            # border_width=border_width,
            # key=key,
            # k=k,
            # tooltip=tooltip,
            # right_click_menu=right_click_menu,
            # visible=visible,
            # element_justification=element_justification,
            # vertical_alignment=vertical_alignment,
            # metadata=metadata,
        )

        # getter and setter for width and height

    def set_height_width(self, width, height):
        self.width = int(width)
        self.height = int(height)

        return True

    def get_height_width(self):
        width = self.width
        height = self.height
        return int(width), int(height)

    def get_graph_layout(self):
        width, height = self.get_height_width()
        print("from init layout", width, height)
        self.graph_vidframe = sg.Graph(
            canvas_size=(width, height),
            graph_bottom_left=(0, 0),
            graph_top_right=(width, height),
            key="graph_vidframe",
            visible=True
        )
        return self.graph_vidframe

    def init_layout(self):
        """Static VideoPlayer layout for initialization"""
        # self.set_height_width(200, 200)
        # width, height = self.get_height_width()
        # print("from init layout", width, height)
        # self.graph_vidframe = sg.Graph(
        #     canvas_size=(width, height),
        #     graph_bottom_left=(0, 0),
        #     graph_top_right=(width, height),
        #     key="graph_vidframe",
        # )

        self.graph_vidframe = self.get_graph_layout()
        self.button_play = sg.B(
            "Play", key="button_play"
        )
        self.button_pause = sg.B(
            "Pause", key="button_pause"
        )
        # size was set to (self.width,10) which was the cause of the extreme width of the window.
        # set enable_events = True: Slider move now generates an event.
        self.slider_vidframe = sg.Slider(range=(0, self.num_frames),enable_events=True,
                                         orientation="h", size=(60, 10), key="slider_vidframe"
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
            :param shape_mode:
            :param shapes:
            :param event:
            :param values:
            :param windows: <class 'PySimpleGUI.PySimpleGUI.Window'>

        """
        # print("Hi from inside video player event loop!")
        if event == "button_play":
            self.play = True
            while self.play:
                # This is required to display image on the graph
                event, values = window.read(timeout=20)

                # Extract graph element
                self.graph = window.Element("graph_vidframe")



                # Read next frame
                ret, frame = self.vidFile.read()

                # Convert image to bytes
                imgbytes = cv.imencode('.png', frame)[1].tobytes()

                # Draw image on graph object
                figure_id = self.graph.DrawImage(data=imgbytes, location=(0, self.height))
                deleted_figure_id = self.graph.DeleteFigure(figure_id - 1)
                # print("DrawImage returned", figure_id)
                # print("Deleted Figure ID", deleted_figure_id)
                # Ensures when Pause is pressed the control is returned to main function
                self.events(event=event, values=values, window=window, shapes=None, shape_mode=None)


        # Pause the video before pressing any external button
        elif event == "button_pause":
            self.play = False
            print('You pressed pause :  Event Loop')
            # exit()
            # self.play = False

            print("Button from main layout called. Breaking the loop")

        elif event == "slider_vidframe":
            print("slider moved")
        #     self.vidframe_no = values["slider_vidframe"]
        #     print("Jump to frame {​}​".format(self.vidframe_no))
        # if self.play and not event == "slider_vidframe":
        #     self.vidframe_no += 1
        #     print("Play next frame {​}​".format(self.vidframe_no))

        return 0

    def draw_shapes(self):
        pass

    def show_new_frame(self):
        pass


# Create instance of VideoPlayer class
MyVideoPlayer = VideoPlayer("My embedded video player")

# Browse Video
MyVideoPlayer.browse_video()

# Populate video paramaters and set width and height
MyVideoPlayer.load_video()

# Initialize video player layout
vid_layout = MyVideoPlayer.init_layout()

# Layout to embed vide player in
external_layout = [
    [sg.Text("Some stuff above video player")],
    [sg.Text("Some other stuff below video player")],
    [sg.Button("External_button", key="button_external")]
]

# Add both layouts
window_layout = external_layout + vid_layout

# Create the window
window = sg.Window(title="My window with embedded video player", layout=window_layout)

while True:
    event, values = window.read(timeout=5)
    if event == "button_play":
        print('You pressed Play :  MAIN Loop')
    if event == "button_pause":
        print('You pressed pause :  MAIN Loop')
    if event == "button_external":
        print("external button pressed from main")
    # Window-related events
    if event == sg.WINDOW_CLOSED or event == "Quit":
        break
    # VideoPlayer related events
    MyVideoPlayer.events(event=event, values=values, window=window)
    # print("broke out from event loop")
# Close window
window.close()
#
# Is VideoPlayer is subclass of sg.Frame and MyVideoPlayer is instance of VideoPlayer?
print(issubclass(VideoPlayer, sg.Frame))
print(isinstance(MyVideoPlayer, VideoPlayer))
