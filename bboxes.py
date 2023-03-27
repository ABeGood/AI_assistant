import json
import os


path_to_bboxes = "bboxes.json"
selected_box_id = None
boxes_list = []
x1, y1, x2, y2 = None, None, None, None
drawing = False


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
        else:
            return None


# function to draw boxes
def add_box(x1_coord, y1_coord, x2_coord, y2_coord):
    global x1, y1, x2, y2

    if x1_coord > x2_coord:
        temp_x = x1_coord
        x1_coord = x2_coord
        x2_coord = temp_x

    if y1_coord > y2_coord:
        temp_y = y1_coord
        y1_coord = y2_coord
        y2_coord = temp_y

    x1, y1, x2, y2 = None, None, None, None

    boxes_list.append(Bbox(len(boxes_list), x1_coord, y1_coord, x2_coord, y2_coord))
    save_bboxes()


# function to delete boxes
def delete_box(box_id):
    global selected_box_id

    i = 0
    for box in boxes_list:
        if box.id == box_id:
            boxes_list.remove(box)
            selected_box_id = None
            break
        i += 1

    for k in range(i, len(boxes_list)):
        boxes_list[k].id = k

    save_bboxes()


def get_bboxes():
    return boxes_list


# Load bboxes from json
def load_bboxes():
    global boxes_list
    if os.path.isfile(path_to_bboxes):
        if os.stat(path_to_bboxes).st_size != 0:
            boxes_file = open(path_to_bboxes)
            # TODO catch empty file or non-jsom format
            boxes_list = json.load(boxes_file, object_hook=Bbox.from_json)
            return boxes_list
        else:
            print("\033[33mbboxes.json is empty.\033[0m")
    else:
        print("\033[33mbboxes.json does not exist.\033[0m")


def save_bboxes():
    json_string = json.dumps(boxes_list, default=obj_dict)

    json_file = open("bboxes.json", "w")
    json_file.write(json_string)
    json_file.close()

