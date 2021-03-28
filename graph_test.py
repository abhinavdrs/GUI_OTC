"""Demonstrates performace of video player when used with graph.DrawImage function """

import PySimpleGUI as sg
import cv2 as cv


#
filename = sg.popup_get_file('Browse Filename to Play')
vidFile = cv.VideoCapture(filename)
width = vidFile.get(cv.CAP_PROP_FRAME_WIDTH )
height = vidFile.get(cv.CAP_PROP_FRAME_HEIGHT )


layout_1 = [
    [
        sg.Graph(
            canvas_size=(width, height),
            graph_bottom_left=(0, 0),
            graph_top_right=(width, height),
            key="graph"
        )
    ]
]

layout_2 = [
    [sg.Text("Placeholder Text")]
]

layout = layout_1 + layout_2
window = sg.Window("Graph Test", layout)
# window.Finalize()

graph = window.Element("graph")




while vidFile.isOpened():
    event, values = window.read(timeout= 10)

    ret, frame = vidFile.read()
    # encode image
    imgbytes = cv.imencode('.png', frame)[1].tobytes()
    ret = graph.DrawImage(data=imgbytes, location=(0, height))
    print("DrawImage returns ", ret)
