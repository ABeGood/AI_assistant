import cv2 as cv
import numpy as np
import bboxes as bb
import input_event_handler as ieh


bb.load_bboxes()
cam = None


# Function to init cv2 video input
def init_cv2(input_source):
    # return cv.VideoCapture
    global cam
    cam = cv.VideoCapture(input_source)
    cv.namedWindow('image')
    cv.setMouseCallback('image', ieh.click_recall)


def update_bboxes_on_frame(frame):
    for box in bb.boxes_list:
        if box.id == bb.selected_box_id:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        cv.rectangle(frame, (box.x1, box.y1), (box.x2, box.y2,), color, 2)
    return frame


# function to refresh frame to dynamically update bboxes and texts
def refresh_frame(frame):
    output_img = frame.copy()

    # TODO Decide if I need this here
    # height = output_img.shape[0]
    # width = output_img.shape[1]

    output_img = update_bboxes_on_frame(output_img)

    cv.putText(output_img, "Mode: {}".format(ieh.current_mode), (2, 12), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (0, 255, 0), 1, cv.LINE_AA)

    cv.imshow('image', output_img)


# Function that starts cv2 loop
def start_cv2():
    # TODO Check if cam != None, throw exception
    while cam.isOpened():
        cam_ret, frame = cam.read()

        # TODO give the frame to hands and pose processor

        # # Process image
        # frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # frame.flags.writeable = False
        #
        # frame.flags.writeable = True
        # frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        input_key = cv.waitKey(10)  # Argument must be "10" to not freeze on first frame

        if input_key == 27:  # ESC
            break

        ieh.keyboard_listener(input_key)
        refresh_frame(frame)

    cam.release()
    cv.destroyAllWindows()