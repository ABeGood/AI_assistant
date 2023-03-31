import cv2 as cv
import bboxes as bb
import input_event_handler as ieh
import pose_processing as pose_proc
import hands_processing as hands_proc
import my_mediapipe as mmp
import geometry as geom
import numpy as np


bb.load_bboxes()
cam = None


# Function to init cv2 video input
def init_cv2(input_source):
    # return cv.VideoCapture
    global cam
    cam = cv.VideoCapture(input_source)
    cv.namedWindow('image')
    cv.setMouseCallback('image', ieh.click_recall)


def get_frame_size():
    cam_ret, frame = cam.read()
    width = frame.shape[1]
    height = frame.shape[0]
    return width, height


def update_bboxes_on_frame(frame):
    for box in bb.boxes_list:
        if box.id == bb.selected_box_id:
            color = (0, 0, 255)
        elif box.id == bb.pointed_box_id:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        cv.rectangle(frame, (box.x1, box.y1), (box.x2, box.y2,), color, 2)
    return frame


# function to refresh frame to dynamically update bboxes and texts
def refresh_frame(frame):
    output_img = frame.copy()
    output_img = update_bboxes_on_frame(output_img)

    cv.putText(output_img, "Mode: {}".format(ieh.current_mode), (2, 12), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (0, 255, 0), 1, cv.LINE_AA)

    cv.imshow('image', output_img)


# Function that starts cv2 loop
def start_cv2():
    # TODO Check if cam != None, throw exception
    while cam.isOpened():
        cam_ret, frame = cam.read()

        # Process image for pose
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame.flags.writeable = False
        pose_landmarks = pose_proc.get_pose_landmarks(frame)
        # hands_landmarks = hands_proc.get_both_hands_landmarks(frame)
        hands_landmarks = hands_proc.get_one_hand_landmarks(frame, 'r')
        frame.flags.writeable = True
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        # TODO move beams somewhere else
        beam_r = pose_proc.get_right_beam(pose_landmarks)
        if beam_r is not None:
            cv.line(frame, (beam_r[0][0], beam_r[0][1]), (beam_r[1][0], beam_r[1][1]),
                    (0, 0, 255), 2)
        bb.get_pointed_box_id(beam_r)
        if bb.pointed_box_id is not None:
            # TODO rework this ugly snapping
            box_center = (int((bb.boxes_list[bb.pointed_box_id].x1 + bb.boxes_list[bb.pointed_box_id].x2) / 2),
                          int((bb.boxes_list[bb.pointed_box_id].y1 + bb.boxes_list[bb.pointed_box_id].y2) / 2))
            closest_point = tuple(map(int, geom.closest_point_on_segment(np.array(beam_r[0]), np.array(beam_r[1]), np.array(box_center))))
            cv.line(frame, np.array(box_center), closest_point, (255, 255, 255), 2)

        frame = mmp.draw_pose_landmarks(frame, pose_landmarks)
        # frame = mmp.draw_both_hands_landmarks(frame, hands_landmarks)
        mmp.draw_one_hand_landmarks(frame, hands_landmarks)

        input_key = cv.waitKey(10)  # Argument must be "10" to not freeze on first frame

        if input_key == 27:  # ESC
            break

        ieh.keyboard_listener(input_key)
        refresh_frame(frame)

    cam.release()
    cv.destroyAllWindows()