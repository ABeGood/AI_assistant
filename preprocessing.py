import copy
import itertools
import math


def normalize(flatten_landmark_list):
    # find max value of the list for normalization
    max_value = max(list(map(abs, flatten_landmark_list)))

    normalized_landmark_list = []

    for element in flatten_landmark_list:
        normalized_landmark_list.append(element / max_value)

    return normalized_landmark_list


def preprocess_to_base_point_xy(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            # set landmark 0 as base point
            base_x, base_y = landmark_point[0], landmark_point[1]

        # for each other landmark calculate it's
        # distance from base point
        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # flatten landmark list (make it 1D)
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    temp_landmark_list = normalize(temp_landmark_list)
    # return list of normalized distances of landmarks from base point
    return temp_landmark_list


# TODO: Check if landmark is present
def preprocess_all_combinations_xy(landmark_list):
    # copy list without landmarks 1-10
    temp_landmark_list = []
    temp_landmark_list.append(landmark_list.landmark[0])
    temp_landmark_list = temp_landmark_list + landmark_list.landmark[11:25]
    reduced_landmark_list = copy.deepcopy(temp_landmark_list)

    distance_list = []
    for lm_combo in itertools.combinations(reduced_landmark_list, 2):
        combo_distance = math.sqrt((lm_combo[0].x - lm_combo[1].x) ** 2 + (lm_combo[0].y - lm_combo[1].y) ** 2)
        distance_list.append(combo_distance)

    distance_list = normalize(distance_list)
    return distance_list


# TODO: check if z coordinate is present
def preprocess_all_combinations_xyz(landmark_list):
    # copy list without landmarks 1-10
    temp_landmark_list = []
    temp_landmark_list.append(landmark_list.landmark[0])
    temp_landmark_list = temp_landmark_list + landmark_list.landmark[11:25]
    reduced_landmark_list = copy.deepcopy(temp_landmark_list)

    distance_list = []
    for lm_combo in itertools.combinations(reduced_landmark_list, 2):
        combo_distance_xy = math.sqrt((lm_combo[0].x - lm_combo[1].x) ** 2 + (lm_combo[0].y - lm_combo[1].y) ** 2)
        combo_distance_xyz = math.sqrt(combo_distance_xy ** 2 + (lm_combo[0].z - lm_combo[1].z) ** 2)
        distance_list.append(combo_distance_xyz)

    distance_list = normalize(distance_list)
    return distance_list


# transform landmark list to [x0, y0, x1, y1, x2, ...]
def flatten_landmark_list_xy(landmark_l):
    flat_lm_list = []
    for index, landmark_point in enumerate(landmark_l):
        flat_lm_list.append(landmark_l[index].x)
        flat_lm_list.append(landmark_l[index].y)

    return flat_lm_list


# transform landmark list to [x0, y0, z0, x1, y1, z1, ...]
def flatten_landmark_list_xyz(landmark_l):
    flat_lm_list = []
    for index, landmark_point in enumerate(landmark_l):
        flat_lm_list.append(landmark_l[index].x)
        flat_lm_list.append(landmark_l[index].y)
        flat_lm_list.append(landmark_l[index].z)

    return flat_lm_list
