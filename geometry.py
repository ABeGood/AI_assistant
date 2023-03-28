# Module for calculating beams from landmarks
# and calculating of intersections of bounding boxes and the beams
import math
import frame_handler as fh
import bboxes as bb


def get_beam(start, end, w, h):
    beam_start = [int(start.x * w), int(start.y * h)]
    beam_end = [int(end.x * w), int(end.y * h)]
    return [beam_start, beam_end]


def get_beam(start, end):  # TODO change arguments or create another function
    w, h = fh.get_frame_size()
    beam_start = [int(start.x * w), int(start.y * h)]
    beam_end = [int((end.x - start.x) * w * 10),  # *10 to make beam longer than the arm
                int((end.y - start.y) * h * 10)]  # *10 to make beam longer than the arm

    beam = fit_beam_end_to_rect([beam_start, beam_end], [0, 0], [w-1, h-1])
    beam_start = beam[0]
    beam_end = beam[1]
    return [beam_start, beam_end]


# line segments intersection
def get_line_line_intersection(line1, line2):
    x1, y1 = line1[0][0], line1[0][1]
    x2, y2 = line1[1][0], line1[1][1]
    x3, y3 = line2[0][0], line2[0][1]
    x4, y4 = line2[1][0], line2[1][1]
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


def get_line_rect_intersection(line, rect):
    ret_val = False
    rect_line_1 = [[rect[0]-rect[2]/2, rect[1]+rect[3]/2], [rect[0]+rect[2]/2, rect[1]+rect[3]/2]]   # lt to rt
    rect_line_2 = [[rect[0]+rect[2]/2, rect[1]+rect[3]/2], [rect[0]+rect[2]/2, rect[1]-rect[3]/2]]   # rt to rb
    rect_line_3 = [[rect[0]+rect[2]/2, rect[1]-rect[3]/2], [rect[0]-rect[2]/2, rect[1]-rect[3]/2]]   # lb to rb
    rect_line_4 = [[rect[0]-rect[2]/2, rect[1]-rect[3]/2], [rect[0]-rect[2]/2, rect[1]+rect[3]/2]]   # lb to lt

    if get_line_line_intersection(line, rect_line_1) is not None:
        ret_val = True
    if get_line_line_intersection(line, rect_line_2) is not None:
        ret_val = True
    if get_line_line_intersection(line, rect_line_3) is not None:
        ret_val = True
    if get_line_line_intersection(line, rect_line_4) is not None:
        ret_val = True

    return ret_val


def get_line_box_intersection(line, box):
    ret_val = False
    rect_line_1 = [[box.x1, box.y1], [box.x2, box.y1]]   # lt to rt
    rect_line_2 = [[box.x2, box.y1], [box.x2, box.y2]]   # rt to rb
    rect_line_3 = [[box.x2, box.y2], [box.x1, box.y2]]   # lb to rb
    rect_line_4 = [[box.x1, box.y2], [box.x1, box.y1]]   # lb to lt

    if get_line_line_intersection(line, rect_line_1) is not None:
        ret_val = True
    if get_line_line_intersection(line, rect_line_2) is not None:
        ret_val = True
    if get_line_line_intersection(line, rect_line_3) is not None:
        ret_val = True
    if get_line_line_intersection(line, rect_line_4) is not None:
        ret_val = True

    return ret_val


def fit_beam_end_to_rect(beam, top_left, bot_right):
    # Rect corners
    top_right = [bot_right[0], top_left[1]]
    bot_left = [top_left[0], bot_right[1]]

    if get_line_line_intersection(beam, [top_left, top_right]) is not None:  #  lt - rt
        beam[1] = (get_line_line_intersection(beam, [top_left, top_right]))

    if get_line_line_intersection(beam, [top_right, bot_right]) is not None:  # rt - rb
        beam[1] = (get_line_line_intersection(beam, [top_right, bot_right]))

    if get_line_line_intersection(beam, [bot_right, bot_left]) is not None:  # rb - lb
        beam[1] = (get_line_line_intersection(beam, [bot_right, bot_left]))

    if get_line_line_intersection(beam, [bot_left, top_left]) is not None:  # lb - lt
        beam[1] = (get_line_line_intersection(beam, [bot_left, top_left]))

    return beam


def closest_point_on_segment(segment_start, segment_end, point):
    segment_vector = segment_end - segment_start  # Get vector from line start to line end
    point_vector = point - segment_start  # Get vector from line start to the point
    projection_length = point_vector.dot(segment_vector) / segment_vector.dot(segment_vector)  # Get projection of point vector to segment vector

    if projection_length < 0:
        return segment_start
    elif projection_length > 1:
        return segment_end
    else:
        projection = segment_start + projection_length * segment_vector
        return projection


def distance_point_to_point(point1, point2):
    # Get distance between two points by Pythagoras
    dist = math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
    return dist
