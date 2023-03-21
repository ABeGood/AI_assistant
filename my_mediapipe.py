import mediapipe as mp


def init_mp_draw():
    mp_drawing = mp.solutions.drawing_utils
    return mp_drawing




def init_mp_pose(detect_conf, track_conf, static_img, complexity):
    mp_pose = mp.solutions.pose

    pose = mp_pose.Pose(
        static_image_mode=static_img,
        model_complexity=complexity,
        min_detection_confidence=detect_conf,
        min_tracking_confidence=track_conf
    )

    return mp_pose, pose
