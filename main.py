import cv2
import geometry as geom
import numpy as np
import my_mediapipe as mmp


rect = [320, 115, 40, 40]
rect_center = [rect[0], rect[1]]
rect_color = (255, 0, 0)
beam_left_start = [0, 0]
beam_left_end = [0, 0]
#
beam_right_start = [0, 0]
beam_right_end = [0, 0]

bulb_selected = False
dist = 0
snap_dist = 100;

pose_solution, pose = mmp.init_mp_pose(detect_conf=0.4, track_conf=0.4, static_img=False, complexity=1)
mp_draw = mmp.init_mp_draw()

cam = cv2.VideoCapture(0)

while cam.isOpened():
    cam_ret, frame = cam.read()

    #frame = cv2.resize(frame, (640, 480))

    h = frame.shape[0]
    w = frame.shape[1]

    # Process image
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame.flags.writeable = False
    pose_results = pose.process(frame)
    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Get pose landmarks
    # Draw landmarks
    if pose_results.pose_landmarks != None:
        mp_draw.draw_landmarks(frame, pose_results.pose_landmarks, pose_solution.POSE_CONNECTIONS)

    if pose_results.pose_landmarks:
        # Left hand
        if (pose_results.pose_landmarks.landmark[14].visibility > 0.5) and (
                pose_results.pose_landmarks.landmark[16].visibility > 0.5):

            # Get beam
            beam_left = geom.get_beam(pose_results.pose_landmarks.landmark[14],
                                      pose_results.pose_landmarks.landmark[16],
                                        w, h, 50)
            # Draw beam
            cv2.line(frame, (beam_left[0][0], beam_left[0][1]), (beam_left[1][0], beam_left[1][1]),
                     (255, 0, 0), 2)

        # Right hand
        if (pose_results.pose_landmarks.landmark[13].visibility > 0.5 and
                pose_results.pose_landmarks.landmark[15].visibility > 0.5):

            # Get beam
            beam_right = geom.get_beam(pose_results.pose_landmarks.landmark[13],
                                       pose_results.pose_landmarks.landmark[15],
                                       w, h, 50)

            cv2.line(frame, (beam_right[0][0], beam_right[0][1]), (beam_right[1][0], beam_right[1][1]),
                     (0, 0, 255), 2)

            cv2.circle(frame, (beam_right_start[0], beam_right_start[1]), 5, (0, 0, 255), 3)
            cv2.circle(frame, (beam_right_end[0], beam_right_start[1]), 5, (0, 0, 255), 3)

            if geom.get_line_rect_intersection(beam_right, rect):
                bulb_selected = True
                rect_color = (0, 255, 0)
            else:
                if dist > 80:
                    bulb_selected = False
                    rect_color = (0, 0, 255)

            if bulb_selected:
                beam_r_start = np.array(beam_right[0])
                beam_r_end = np.array(beam_right[1])
                rect_c = np.array(rect_center)

                cp = tuple(map(int, geom.closest_point_on_segment(beam_r_start, beam_r_end, rect_c)))
                dist = geom.distance_point_to_point(cp, rect_c)
                cv2.line(frame, cp, rect_c, (0, 255, 0), int(80/dist)+1)



        cv2.rectangle(frame, (int(rect[0] + rect[2] / 2),
                              int(rect[1] + rect[3] / 2)),
                      (int(rect[0] - rect[2] / 2),
                       int(rect[1] - rect[3] / 2)), rect_color, 2)

    cv2.imshow('Output', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
