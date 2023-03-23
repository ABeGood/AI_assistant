import numpy as np

# function to refresh frame to dynamically update bboxes and texts
def refresh_frame(boxes_list, mode):
    img = np.zeros((360, 512, 3), np.uint8)
    output_img = img.copy()
    for box in boxes_list:
        if box.id == selected_box_id:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        cv.rectangle(output_img, (box.x1, box.y1), (box.x2, box.y2,), color, 2)

    cv.putText(output_img, "Mode: {}".format(mode), (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                       cv.LINE_AA)
    cv.imshow('image', output_img)