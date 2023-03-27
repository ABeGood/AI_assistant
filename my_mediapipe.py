import mediapipe as mp

pose_solution = None
pose_detector = None

hands_solution = None
hands_detector = None

draw = None


def init_mp_draw():
    global draw
    draw = mp.solutions.drawing_utils


# MP Pose
def init_mp_pose(detect_conf, track_conf, static_img, complexity):
    global pose_solution, pose_detector

    pose_solution = mp.solutions.pose

    pose_detector = pose_solution.Pose(
        static_image_mode=static_img,
        model_complexity=complexity,
        min_detection_confidence=detect_conf,
        min_tracking_confidence=track_conf
    )


def draw_pose_landmarks(frame, landmarks):
    draw.draw_landmarks(frame, landmarks, pose_solution.POSE_CONNECTIONS)
    return frame


# MP Hands
def init_mp_hands(detect_conf, track_conf, static_img, complexity, num_of_hands):
    global hands_solution, hands_detector

    hands_solution = mp.solutions.hands

    hands_detector = hands_solution.Hands(
        static_image_mode=static_img,
        model_complexity=complexity,
        min_detection_confidence=detect_conf,
        min_tracking_confidence=track_conf,
        max_num_hands=num_of_hands
    )


def draw_both_hands_landmarks(frame, landmarks):
    if landmarks is not None:
        for hand in landmarks:
            draw.draw_landmarks(frame, hand, hands_solution.HAND_CONNECTIONS)
    return frame


def draw_one_hand_landmarks(frame, landmarks):
    if landmarks is not None:
        draw.draw_landmarks(frame, landmarks, hands_solution.HAND_CONNECTIONS)
    return frame

