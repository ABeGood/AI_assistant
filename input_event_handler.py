from enum import Enum
import bboxes as bb
import cv2


class Mode(Enum):
    NONE = 0
    DRAWING = 1
    REMOVE = 2


current_mode = Mode.NONE


# function to select modes (None/Draw/Remove)
def set_mode(new_mode: Mode):  # Takes enum Mode as argument
    global current_mode
    if new_mode != Mode.REMOVE:
        bb.selected_box_id = None

    current_mode = new_mode


def keyboard_listener(key_input):

    if key_input == 110:  # n None
        set_mode(Mode.NONE)

    elif key_input == 100:  # d  Draw
        set_mode(Mode.DRAWING)

    elif key_input == 114:  # r Remove
        if current_mode == Mode.REMOVE:  # delete key
            bb.delete_box(bb.selected_box_id)
        else:
            set_mode(Mode.REMOVE)


# mouse callback function
def click_recall(event, x, y, flags, param):
    global current_mode

    if current_mode == Mode.DRAWING:
        # if the left mouse button was clicked, record the starting and set the drawing flag to True
        if event == cv2.EVENT_LBUTTONDOWN:
            bb.drawing = True
            bb.x1, bb.y1 = x, y

        # mouse is being moved, draw rectangle
        if event == cv2.EVENT_MOUSEMOVE:
            if bb.drawing:
                bb.x2, bb.y2 = x, y

        # if the left mouse button was released, set the drawing flag to False
        if event == cv2.EVENT_LBUTTONUP:
            bb.drawing = False
            bb.add_box(bb.x1, bb.y1, bb.x2, bb.y2)

    elif current_mode == Mode.REMOVE:
        if event == cv2.EVENT_LBUTTONDOWN:
            # if the left mouse button was clicked iterate trough bboxes_list and check is click event coords
            # are inside bbox borders
            bb.selected_box_id = bb.check_box_selection(x, y)

