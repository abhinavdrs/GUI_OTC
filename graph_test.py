"""Demonstrates performace of video player when used with graph.DrawImage function """

import PySimpleGUI as sg
import cv2 as cv
from time import perf_counter

#
filename = sg.popup_get_file('Browse Filename to Play')
vidFile = cv.VideoCapture(filename)
width = vidFile.get(cv.CAP_PROP_FRAME_WIDTH)
height = vidFile.get(cv.CAP_PROP_FRAME_HEIGHT)

print("width and height of the video", width, height)

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

flag = 0

while vidFile.isOpened():
    event, values = window.read(timeout=20)
    t_0 = perf_counter()
    ret, frame = vidFile.read()

    if flag == 1:
        graph.erase()
        # graph.DeleteFigure(ret)
    # encode image
    imgbytes = cv.imencode('.png', frame)[1].tobytes()
    ret = graph.DrawImage(data=imgbytes, location=(0, height))
    flag = 1
    t_1 = perf_counter()
    # print("DrawImage returns ", ret)
    print(t_1 - t_0)

