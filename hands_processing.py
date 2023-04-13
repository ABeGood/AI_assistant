import my_mediapipe as mmp


actual_gesture_id = 0


def get_both_hands_landmarks(frame):
    hands_results = mmp.hands_detector.process(frame)

    if hands_results is not None:
        return hands_results.multi_hand_landmarks


def get_one_hand_landmarks(frame, requested_hand_type):  # TODO Hands are inverted
    hands_results = mmp.hands_detector.process(frame)

    hand_types = []
    hand_landmarks = []

    hand_landmarks_l = None
    hand_landmarks_r = None

    if hands_results.multi_hand_landmarks is not None:
        for hand in hands_results.multi_handedness:
            hand_type = hand.classification[0].label
            hand_types.append(hand_type)

        for landmarks in hands_results.multi_hand_landmarks:
            hand_landmarks.append(landmarks)

        for hand_landmark, hand_type in zip(hand_landmarks, hand_types):
            if hand_type == "Right":
                hand_landmarks_r = hand_landmark
            if hand_type == "Left":
                hand_landmarks_l = hand_landmark

        if requested_hand_type == 'l':
            return hand_landmarks_l
        elif requested_hand_type == 'r':
            return hand_landmarks_r
        else:
            print("Wrong requested hand type.")
            return None


def update_gesture(new_gesture_id):
    # TODO add regulation
    global actual_gesture_id
    if actual_gesture_id != new_gesture_id:
        if ((actual_gesture_id == 1) or (actual_gesture_id == 2)) and new_gesture_id == 0:
            actual_gesture_id = new_gesture_id
            return 0
        if (actual_gesture_id == 0) and ((new_gesture_id == 1) or (new_gesture_id == 2)):
            actual_gesture_id = new_gesture_id
            return 1
