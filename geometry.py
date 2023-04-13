# Module for calculating beams from landmarks
# and calculating of intersections of bounding boxes and the beams
import math
import frame_handler as fh
import numpy as np


class Beam:
    def __init__(self, start, end):
        self.start_xy = start
        self.end_xy = end
        self.start_x = start[0]
        self.start_y = start[1]
        self.end_x = end[0]
        self.end_y = end[1]


class Frame:
    def __init__(self, x1, y1, x2, y2):
        self.id = id
        self.top_left = (x1, y1)
        self.top_right = (x2, y1)
        self.bot_left = (x1, y2)
        self.bot_right = (x2, y2)


def get_beam(start, end):
    w, h = fh.get_frame_size()
    frame = Frame(0, 0, w, h)
    beam_start = int(start[0]*w), int(start[1]*h)
    beam_end = int((end[0]-start[0])*1000)*w, int((end[1]-start[1])*1000)*h
    beam = Beam(beam_start, beam_end)

    beam = fit_beam_end_to_frame(beam, frame)
    return beam


# line segments intersection
def get_beam_line_intersection(beam: Beam, line):
    x1, y1 = beam.start_x, beam.start_y
    x2, y2 = beam.end_x, beam.end_y
    x3, y3 = line[0][0], line[0][1]
    x4, y4 = line[1][0], line[1][1]
    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denom == 0:  # parallel
        return None
    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    if ua < 0 or ua > 1:  # out of range
        return None
    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    if ub < 0 or ub > 1:  # out of range
        return None
    x = int(x1 + ua * (x2-x1))
    y = int(y1 + ua * (y2-y1))
    return x, y


def get_beam_rect_intersection(beam, rect):
    ret_val = False
    rect_line_1 = [[rect[0]-rect[2]/2, rect[1]+rect[3]/2], [rect[0]+rect[2]/2, rect[1]+rect[3]/2]]   # lt to rt
    rect_line_2 = [[rect[0]+rect[2]/2, rect[1]+rect[3]/2], [rect[0]+rect[2]/2, rect[1]-rect[3]/2]]   # rt to rb
    rect_line_3 = [[rect[0]+rect[2]/2, rect[1]-rect[3]/2], [rect[0]-rect[2]/2, rect[1]-rect[3]/2]]   # lb to rb
    rect_line_4 = [[rect[0]-rect[2]/2, rect[1]-rect[3]/2], [rect[0]-rect[2]/2, rect[1]+rect[3]/2]]   # lb to lt

    if get_beam_line_intersection(beam, rect_line_1) is not None:
        ret_val = True
    if get_beam_line_intersection(beam, rect_line_2) is not None:
        ret_val = True
    if get_beam_line_intersection(beam, rect_line_3) is not None:
        ret_val = True
    if get_beam_line_intersection(beam, rect_line_4) is not None:
        ret_val = True

    return ret_val


def get_line_box_intersection(line, box):
    ret_val = False
    rect_line_1 = [[box.x1, box.y1], [box.x2, box.y1]]   # lt to rt
    rect_line_2 = [[box.x2, box.y1], [box.x2, box.y2]]   # rt to rb
    rect_line_3 = [[box.x2, box.y2], [box.x1, box.y2]]   # lb to rb
    rect_line_4 = [[box.x1, box.y2], [box.x1, box.y1]]   # lb to lt

    if get_beam_line_intersection(line, rect_line_1) is not None:
        ret_val = True
    if get_beam_line_intersection(line, rect_line_2) is not None:
        ret_val = True
    if get_beam_line_intersection(line, rect_line_3) is not None:
        ret_val = True
    if get_beam_line_intersection(line, rect_line_4) is not None:
        ret_val = True

    return ret_val


def fit_beam_end_to_frame(beam: Beam, frame: Frame):
    if get_beam_line_intersection(beam, (frame.top_left, frame.top_right)) is not None:  # tl - tr
        beam.end_xy = (get_beam_line_intersection(beam, (frame.top_left, frame.top_right)))

    if get_beam_line_intersection(beam, (frame.top_right, frame.bot_right)) is not None:  # tr - br
        beam.end_xy = (get_beam_line_intersection(beam, (frame.top_right, frame.bot_right)))

    if get_beam_line_intersection(beam, (frame.bot_right, frame.bot_left)) is not None:  # br - bl
        beam.end_xy = (get_beam_line_intersection(beam, (frame.bot_right, frame.bot_left)))

    if get_beam_line_intersection(beam, (frame.bot_left, frame.top_left)) is not None:  # bl - tl
        beam.end_xy = (get_beam_line_intersection(beam, (frame.bot_left, frame.top_left)))
    return beam


def closest_point_on_segment(segment_start, segment_end, point):
    segment_start = np.array(segment_start)
    segment_end = np.array(segment_end)
    point = np.array(point)

    segment_vector = segment_end - segment_start  # Get vector from line start to line end
    point_vector = point - segment_start  # Get vector from line start to the point
    projection_length = point_vector.dot(segment_vector) / segment_vector.dot(segment_vector)  # Get projection of point vector to segment vector

    if projection_length < 0:
        return segment_start
    elif projection_length > 1:
        return segment_end
    else:
        projection = segment_start + projection_length * segment_vector
        return tuple(map(int, projection))


def distance_point_to_point(point1, point2):
    # Get distance between two points by Pythagoras
    dist = math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
    return dist
