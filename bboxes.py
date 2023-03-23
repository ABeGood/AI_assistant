import cv2 as cv
import json
import os
import input_event_handler as input_handler


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


path_to_bboxes = "bboxes.json"
global selected_box_id
selected_box_id = -1
boxes_list = []
x1, y1, x2, y2 = None, None, None, None
drawing = False


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


# Load bboxes from json
def load_bboxes():
    if os.path.isfile(path_to_bboxes):
        boxes_file = open(path_to_bboxes)
        boxes_list = json.load(boxes_file, object_hook=Bbox.from_json)
        return boxes_list





# main part
# TODO move to main
cv.namedWindow('image')
cv.setMouseCallback('image', input_handler.click_recall)


while True:

    key = cv.waitKey(10)
    if key == 27:  # ESC
        jsonString = json.dumps(boxes_list, default=obj_dict)

        jsonFile = open("bboxes.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        break

    input_handler.keyboard_listener(key)
    refresh_frame()

cv.destroyAllWindows()
