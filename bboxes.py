import json
import os
import geometry as geom


path_to_bboxes = "bboxes.json"
selected_box_id = None
pointed_box_id = None
boxes_list = []
x1, y1, x2, y2 = None, None, None, None
drawing = False
max_snap_distance = 120


class Bbox:
    def __init__(self, id, x1, y1, x2, y2):
        self.id = id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.center = ((x1+x2)/2, (y1+y2)/2)

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
            # TODO catch empty file or non-json format
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


# def get_snap_distance(beam, box: Bbox):
#     box_center = ((box.x1+box.x2)/2, (box.y1+box.y2)/2)
#     closest_point = geom.closest_point_on_segment(beam.start_xy, beam.end_xy, box_center)
#     distance = int(geom.distance_point_to_point(closest_point, box_center))
#     return distance


def get_snap(beam, box: Bbox):
    box_center = (int((box.x1+box.x2)/2), int((box.y1+box.y2)/2))
    closest_point = geom.closest_point_on_segment(beam.start_xy, beam.end_xy, box_center)
    distance = int(geom.distance_point_to_point(closest_point, box_center))
    return distance, closest_point, box_center


# TODO: what if beam intersects more than one box?
def get_pointed_box_id(beam):
    global pointed_box_id
    if beam is not None:
        for box in boxes_list:
            if geom.get_line_box_intersection(beam, box):
                pointed_box_id = box.id
                return box.id
            else:
                if pointed_box_id is not None:  # TODO change this ugly check
                    snapping_dist = get_snap(beam, boxes_list[pointed_box_id])[0]
                    print(snapping_dist)
                    if snapping_dist > max_snap_distance:
                        pointed_box_id = None
                        return None
    else:
        pointed_box_id = None
        return None


