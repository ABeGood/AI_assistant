import numpy as np
import tensorflow as tf
import csv

gesture_interpreter = None
gesture_classifier_labels = None
gesture_input_details = None
gesture_output_details = None

pointing_interpreter = None
pointing_classifier_labels = None
pointing_input_details = None
pointing_output_details = None
# model_path='models/pose_classifier.tflite'


def init_gesture_classifier():
    global gesture_interpreter, gesture_input_details, gesture_output_details, gesture_classifier_labels
    model_path = 'models/gesture_classifier.tflite'

    gesture_interpreter = tf.lite.Interpreter(model_path=model_path, num_threads=1)

    gesture_interpreter.allocate_tensors()
    gesture_input_details = gesture_interpreter.get_input_details()
    gesture_output_details = gesture_interpreter.get_output_details()

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


# TODO: Merge pointing and unusual pose
def init_pointing_classifier():
    global pointing_interpreter, pointing_input_details, pointing_output_details, pointing_classifier_labels
    model_path = 'models/pointing_classifier.tflite'

    pointing_interpreter = tf.lite.Interpreter(model_path=model_path, num_threads=1)

    pointing_interpreter.allocate_tensors()
    pointing_input_details = pointing_interpreter.get_input_details()
    pointing_output_details = pointing_interpreter.get_output_details()

    # Here I just read labels from the .cvf file  TODO: rework this
    with open('models/pointing_classifier_label.csv',
              encoding='utf-8-sig') as f:
        pointing_classifier_labels = csv.reader(f)
        pointing_classifier_labels = [row[0] for row in pointing_classifier_labels]


def classify_pointing(landmark_list,):
    global pointing_interpreter, pointing_input_details, pointing_output_details
    input_details_tensor_index = pointing_input_details[0]['index']
    pointing_interpreter.set_tensor(input_details_tensor_index, np.array([landmark_list], dtype=np.float32))
    pointing_interpreter.invoke()
    output_details_tensor_index = pointing_output_details[0]['index']
    result = pointing_interpreter.get_tensor(output_details_tensor_index)
    result_index = np.argmax(np.squeeze(result))

    return result_index



