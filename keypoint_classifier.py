import numpy as np
import tensorflow as tf
import csv

gesture_interpreter = None
gesture_classifier_labels = None
gesture_input_details = None
gesture_output_details = None
# model_path='models/pose_classifier.tflite'


def init_gesture_classifier():
    global gesture_interpreter, gesture_input_details, gesture_output_details, gesture_classifier_labels
    model_path = 'models/gesture_classifier.tflite'

    gesture_interpreter = tf.lite.Interpreter(model_path=model_path, num_threads=1)

    gesture_interpreter.allocate_tensors()
    input_details = gesture_interpreter.get_input_details()
    output_details = gesture_interpreter.get_output_details()

    # Here I just read labels from the .cvf file  TODO: rework this
    with open('models/gesture_classifier_label.csv',
              encoding='utf-8-sig') as f:
        gesture_classifier_labels = csv.reader(f)
        gesture_classifier_labels = [row[0] for row in gesture_classifier_labels]


def classify_gesture(landmark_list,):
    global gesture_interpreter, gesture_input_details, gesture_output_details
    input_details_tensor_index = gesture_input_details[0]['index']
    gesture_interpreter.set_tensor(input_details_tensor_index, np.array([landmark_list], dtype=np.float32))
    gesture_interpreter.invoke()
    output_details_tensor_index = gesture_output_details[0]['index']
    result = gesture_interpreter.get_tensor(output_details_tensor_index)
    result_index = np.argmax(np.squeeze(result))

    return result_index



