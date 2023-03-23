import mediapipe as mp


def init_mp_draw():
    return mp.solutions.drawing_utils


def init_mp_pose(detect_conf, track_conf, static_img, complexity):
    pose_solution = mp.solutions.pose

    pose_detector = pose_solution.Pose(
        static_image_mode=static_img,
        model_complexity=complexity,
        min_detection_confidence=detect_conf,
        min_tracking_confidence=track_conf
    )

    return pose_solution, pose_detector
