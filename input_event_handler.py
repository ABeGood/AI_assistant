import bboxes as bb
import cv2


# function to select modes (None/Draw/Remove)
def select_mode(new_mode):
    global selected_box_id, mode
    mode = new_mode


# function to process keyboard operations
def keyboard_listener(key_input, current_mode):
    global selected_box_id
    new_mode = -1

    if key_input == 110:  # n None
        new_mode = 0
        selected_box_id = -1
    elif key_input == 100:  # d  Draw
        new_mode = 1
        selected_box_id = -1

    elif key_input == 114:  # r Remove
        if current_mode == 2:  # delete key
            bb.delete_box(selected_box_id)
            selected_box_id = -1
        else:
            new_mode = 2
            select_mode(new_mode)


# mouse callback function
def click_recall(event, x, y, flags, param):
    global mode, selected_box_id, x1, y1, x2, y2, drawing

    if mode == 1:
        # if the left mouse button was clicked, record the starting and set the drawing flag to True
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            x1, y1 = x, y

        # mouse is being moved, draw rectangle
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                x2, y2 = x, y

        # if the left mouse button was released, set the drawing flag to False
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            bb.add_box(x1, y1, x2, y2)

    elif mode == 2:
        if event == cv2.EVENT_LBUTTONDOWN:
            # if the left mouse button was clicked iterate trough bboxes_list and check is click event coords
            # are inside bbox borders
            selected_box_id = bb.check_box_selection(x, y)