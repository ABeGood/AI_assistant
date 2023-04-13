import cv2 as cv
import bboxes as bb
import input_event_handler as ieh
import pose_processing as pose_proc
import hands_processing as hands_proc
import my_mediapipe as mmp
import numpy as np
import preprocessing as pre
import keypoint_classifier as kpc
import bulb


# class Frame:
#     def __init__(self, x1, y1, x2, y2):
#         self.id = id
#         self.top_left = (x1, y1)
#         self.top_right = (x2, y1)
#         self.bot_left = (x1, y2)
#         self.bot_right = (x2, y2)


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


# function from kazuhito  TODO: rework it
def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


def draw_bounding_rect(image, brect):
    cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                 (0, 0, 0), 1)
    return image


def draw_info_text(image, brect, hand_sign_text):
    cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                 (0, 0, 0), -1)

    if hand_sign_text != "":
        info_text =  hand_sign_text
    cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)

    return image


# Function that starts cv2 loop
def start_cv2():
    # TODO Check if cam != None, throw exception
    while cam.isOpened():
        cam_ret, frame = cam.read()

        # Process image for pose
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame.flags.writeable = False
        pose_landmarks = pose_proc.get_pose_landmarks(frame)
        hands_landmarks = hands_proc.get_both_hands_landmarks(frame)
        # hands_landmarks = hands_proc.get_one_hand_landmarks(frame, 'r')
        frame.flags.writeable = True
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        frame = mmp.draw_pose_landmarks(frame, pose_landmarks)
        frame = mmp.draw_both_hands_landmarks(frame, hands_landmarks)

        if pose_landmarks is not None:
            pre_processed_pose_lms = pre.pose_preprocess_to_base_point_xy(pre.calc_landmark_list(pose_landmarks.landmark))
            pose_id = kpc.classify_pointing(pre_processed_pose_lms)
            pose_brect = calc_bounding_rect(frame, pose_landmarks.landmark)
            frame = draw_bounding_rect(frame, pose_brect)
            frame = draw_info_text(frame, pose_brect, kpc.pointing_classifier_labels[pose_id])

            if pose_id == 1:
                # TODO move beams somewhere else
                beam_r = pose_proc.get_right_beam(pose_landmarks)
                beam_l = pose_proc.get_left_beam(pose_landmarks)
                if beam_r is not None:
                    cv.line(frame, beam_r.start_xy, beam_r.end_xy, (0, 0, 255), 4)
                    bb.get_pointed_box_id(beam_r)
                    if bb.pointed_box_id is not None:
                        snap_dist, closest_point, box_center = bb.get_snap(beam_r, bb.boxes_list[bb.pointed_box_id])
                        cv.line(frame, np.array(box_center), closest_point, (255, 255, 255), 2)

                # mmp.draw_one_hand_landmarks(frame, hands_landmarks)
                if hands_landmarks is not None:
                    for landmarks in hands_landmarks:
                        pre_processed_landmark_list = pre.hands_preprocess_to_base_point_xy(pre.calc_landmark_list(landmarks.landmark))

                        gesture_id = kpc.classify_gesture(pre_processed_landmark_list)
                        # print(hand_sign_id)

                        # TODO move this somewhere and refactor
                        brect = calc_bounding_rect(frame, landmarks.landmark)
                        frame = draw_bounding_rect(frame, brect)
                        frame = draw_info_text(
                            frame,
                            brect,
                            kpc.gesture_classifier_labels[gesture_id],
                        )
                        action = hands_proc.update_gesture(gesture_id)
                        if bb.pointed_box_id == 0 and action == 1:
                            bulb.switch_on()
                        if bb.pointed_box_id == 0 and action == 0:
                            bulb.switch_off()

        input_key = cv.waitKey(10)  # Argument must be "10" to not freeze on the first frame

        if input_key == 27:  # ESC
            break

        ieh.keyboard_listener(input_key)
        refresh_frame(frame)

    cam.release()
    cv.destroyAllWindows()