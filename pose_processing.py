import my_mediapipe as mmp
import geometry as geom

min_visibility = 0.5


def get_pose_landmarks(frame):
    pose_results = mmp.pose_detector.process(frame)

    if pose_results is not None:
        return pose_results.pose_landmarks


def landmark_to_tuple(landmark):
    x = landmark.x
    y = landmark.y
    return x, y


def get_right_beam(pose_landmarks):
    if pose_landmarks is not None:
        if (pose_landmarks.landmark[13].visibility > min_visibility) and (pose_landmarks.landmark[15].visibility > min_visibility):
            return geom.get_beam(landmark_to_tuple(pose_landmarks.landmark[13]), landmark_to_tuple(pose_landmarks.landmark[15]))


def get_left_beam(pose_landmarks):
    if pose_landmarks is not None:
        if (pose_landmarks.landmark[14].visibility > min_visibility) and (pose_landmarks.landmark[16].visibility > min_visibility):
            return geom.get_beam(landmark_to_tuple(pose_landmarks.landmark[14]), landmark_to_tuple(pose_landmarks.landmark[16]))
