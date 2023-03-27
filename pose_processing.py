import my_mediapipe as mmp
import geometry as geom

min_visibility = 0.5


def get_pose_landmarks(frame):
    pose_results = mmp.pose_detector.process(frame)

    if pose_results is not None:
        return pose_results.pose_landmarks


def get_right_beam(pose_landmarks):
    if (pose_landmarks.landmark[13].visibility > min_visibility) and (pose_landmarks.landmark[15].visibility > min_visibility):
        return geom.get_beam(pose_landmarks.landmark[13], pose_landmarks.landmark[15])


def get_right_beam(pose_landmarks):
    if (pose_landmarks.landmark[14].visibility > min_visibility) and (pose_landmarks.landmark[16].visibility > min_visibility):
        return geom.get_beam(pose_landmarks.landmark[14], pose_landmarks.landmark[16])






# h = frame.shape[0]
# w = frame.shape[1]

# pose_results = pose_detector.process(frame)

# Get pose landmarks
        # Draw landmarks
        # if pose_results.pose_landmarks != None:
        #     mp_draw.draw_landmarks(frame, pose_results.pose_landmarks, pose_solution.POSE_CONNECTIONS)
        #
        # if pose_results.pose_landmarks:
        #     # Left hand
        #     if (pose_results.pose_landmarks.landmark[14].visibility > 0.5) and (
        #             pose_results.pose_landmarks.landmark[16].visibility > 0.5):
        #         # Get beam
        #         beam_left = geom.get_beam(pose_results.pose_landmarks.landmark[14],
        #                                   pose_results.pose_landmarks.landmark[16],
        #                                   w, h, 50)
        #         # Draw beam
        #         cv2.line(frame, (beam_left[0][0], beam_left[0][1]), (beam_left[1][0], beam_left[1][1]),
        #                  (255, 0, 0), 2)
        #
        #     # Right hand
        #     if (pose_results.pose_landmarks.landmark[13].visibility > 0.5 and
        #             pose_results.pose_landmarks.landmark[15].visibility > 0.5):
        #
        #         # Get beam
        #         beam_right = geom.get_beam(pose_results.pose_landmarks.landmark[13],
        #                                    pose_results.pose_landmarks.landmark[15],
        #                                    w, h, 50)
        #
        #         cv2.line(frame, (beam_right[0][0], beam_right[0][1]), (beam_right[1][0], beam_right[1][1]),
        #                  (0, 0, 255), 2)
        #
        #         cv2.circle(frame, (beam_right_start[0], beam_right_start[1]), 5, (0, 0, 255), 3)
        #         cv2.circle(frame, (beam_right_end[0], beam_right_start[1]), 5, (0, 0, 255), 3)
        #
        #         if geom.get_line_rect_intersection(beam_right, rect):
        #             bulb_selected = True
        #             rect_color = (0, 255, 0)
        #         else:
        #             if dist > 80:
        #                 bulb_selected = False
        #                 rect_color = (0, 0, 255)
        #
        #         if bulb_selected:
        #             beam_r_start = np.array(beam_right[0])
        #             beam_r_end = np.array(beam_right[1])
        #             rect_c = np.array(rect_center)
        #
        #             cp = tuple(map(int, geom.closest_point_on_segment(beam_r_start, beam_r_end, rect_c)))
        #             dist = geom.distance_point_to_point(cp, rect_c)
        #             cv2.line(frame, cp, rect_c, (0, 255, 0), int(80 / dist) + 1)
        #
        #     cv2.rectangle(frame, (int(rect[0] + rect[2] / 2),
        #                           int(rect[1] + rect[3] / 2)),
        #                   (int(rect[0] - rect[2] / 2),
        #                    int(rect[1] - rect[3] / 2)), rect_color, 2)