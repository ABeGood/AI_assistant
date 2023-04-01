import frame_handler as fh
import my_mediapipe as mmp


mmp.init_mp_pose(detect_conf=0.5, track_conf=0.5, static_img=False, complexity=1)
mmp.init_mp_hands(detect_conf=0.5, track_conf=0.5, static_img=False, complexity=1, num_of_hands=2)
mmp.init_mp_draw()
fh.init_cv2(0)
fh.start_cv2()
