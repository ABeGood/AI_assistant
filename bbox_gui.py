import numpy as np
import cv2 as cv
import json
import os


class Bbox:
    def __init__(self, id, x1, y1, x2, y2):
        self.id = id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    # function to deserialize json to list of Bbox objects
    def from_json(json_dict):
        return Bbox(json_dict['id'],
                    json_dict['x1'], json_dict['y1'],
                    json_dict['x2'], json_dict['y2'])


# function to convert Bbox object to dictionary
def obj_dict(obj):
    return obj.__dict__


# function to select check if mouse click was inside bbox
def check_box_selection(x, y):
    for box in boxes_list:
        event_inside_x = False
        event_inside_y = False

        if (x > box.x1) and (x < box.x2):
            event_inside_x = True
        if (y > box.y1) and (y < box.y2):
            event_inside_y = True

        if event_inside_x and event_inside_y:
            return box.id
    return -1


# function to draw boxes
def add_box(x1_coord, y1_coord, x2_coord, y2_coord):
    if x1_coord > x2_coord:
        temp_x = x1_coord
        x1_coord = x2_coord
        x2_coord = temp_x

    if y1_coord > y2_coord:
        temp_y = y1_coord
        y1_coord = y2_coord
        y2_coord = temp_y

    boxes_list.append(Bbox(len(boxes_list), x1_coord, y1_coord, x2_coord, y2_coord))


# function to delete boxes
def delete_box(box_id):
    i = 0
    for box in boxes_list:
        if box.id == box_id:
            boxes_list.remove(box)
            break
        i += 1

    for k in range(i, len(boxes_list)):
        boxes_list[k].id = k


# function to process keyboard operations
def keyboard_listener(key_input):
    global selected_box_id
    if (mode == 2) and (key_input == 114):  # delete key
        delete_box(selected_box_id)
        selected_box_id = -1
    else:
        select_mode(key_input)


# function to select modes (None/Draw/Remove)
def select_mode(mode_key):
    global selected_box_id, mode
    if mode_key == 110:  # n None
        mode = 0
        selected_box_id = -1
    if mode_key == 100:  # d  Draw
        mode = 1
        selected_box_id = -1
    if mode_key == 114:  # r Remove
        mode = 2


# function to refresh frame to dynamically update bboxes and texts
def refresh_frame():
    img = np.zeros((360, 512, 3), np.uint8)
    output_img = img.copy()
    for box in boxes_list:
        if box.id == selected_box_id:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        cv.rectangle(output_img, (box.x1, box.y1), (box.x2, box.y2,), color, 2)

    cv.putText(output_img, "Mode: {}".format(mode), (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                       cv.LINE_AA)
    cv.imshow('image', output_img)


mode = 0
selected_box_id = -1
boxes_list = []
x1, y1, x2, y2 = None, None, None, None
drawing = False

# mouse callback function
def click_recall(event, x, y, flags, param):
    global mode, selected_box_id, x1, y1, x2, y2, drawing

    if mode == 1:
        # if the left mouse button was clicked, record the starting and set the drawing flag to True
        if event == cv.EVENT_LBUTTONDOWN:
            drawing = True
            x1, y1 = x, y

        # mouse is being moved, draw rectangle
        elif event == cv.EVENT_MOUSEMOVE:
            if drawing == True:
                x2, y2 = x, y

        # if the left mouse button was released, set the drawing flag to False
        elif event == cv.EVENT_LBUTTONUP:
            drawing = False
            add_box(x1, y1, x2, y2)



    elif mode == 2:
        if event == cv.EVENT_LBUTTONDOWN:
            # if the left mouse button was clicked iterate trough bboxes_list and check is click event coords
            # are inside bbox borders
            selected_box_id = check_box_selection(x, y)



# main part

# Load bboxes from json
path = "bboxes.json"
if os.path.isfile(path):
    boxes_file = open(path)
    boxes_list = json.load(boxes_file, object_hook=Bbox.from_json)

cv.namedWindow('image')
cv.setMouseCallback('image', click_recall)


while True:

    key = cv.waitKey(10)
    if key == 27:  # ESC
        jsonString = json.dumps(boxes_list, default=obj_dict)

        jsonFile = open("bboxes.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        break

    keyboard_listener(key)
    refresh_frame()

cv.destroyAllWindows()
