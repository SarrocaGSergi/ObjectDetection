import os
import numpy as np
from pathlib import Path

_ROOT = Path(__file__).parents[1]


def save_file(file_bytes: bytes, name: str) -> str:
    '''
    This functions receives a bytes like information and saves it into a storage folder as a file.
    :param file_bytes: bytes information of the file to be saved
    :param name: name of the file to be saved
    :return: path of the saved file
    '''
    # Check Storage directory
    if not os.path.isdir(os.path.join(_ROOT, "storage")):
        os.mkdir(os.path.join(_ROOT, "storage"))

    out_path = os.path.join(_ROOT, f"storage/{name}")
    with open(out_path, "wb") as f:
        f.write(file_bytes)
    f.close()
    return out_path


def bbx_to_json(bbx: np.ndarray, label: int, score: float) -> dict:
    '''
    This function is used to reformat the information obtained from an object detector into a json style. This can be
    used to return the information from an API call.
    :param bbx: array, The bounding box we want to store
    :param label: int, The class of the object detected in the bounding box
    :param score: float, The confidence of the detected object
    :return: dict, Returns the dictionary containing all the information needed
    '''

    x_top, y_top, x_left, y_left = bbx
    if label == 0:
        label = "Person"
    elif label == 2:
        label = "Car"

    bbx_dict = {"label": label, "score": float(score), "x_top": int(x_top), "y_top": int(y_top), "x_left": int(x_left),
                "y_left": int(y_left)}

    return bbx_dict


def detect_objects(yolo_detector, image_path: str) -> dict:
    '''
    This function uses a object detector alreay initialized by the user and detects persons and cars in an image.
    Finally, it updates the object where we are storing our results.
    :param yolo_detector: Object detector
    :param image_path: root to the image to be processed
    '''
    # Detect object with Yolov8 nano, casting classes to Person and Car according to coco128 dataset
    detections = yolo_detector(source=image_path, conf=0.5, classes=[0, 2], verbose=False, stream=False)

    results = {"image_metadata": {"file_root": image_path}}

    for idx, image_result in enumerate(detections[0]):
        # Extract the results in xyxy format
        box_list = np.squeeze(image_result.boxes.xyxy.cpu().numpy())
        cls = int(image_result.boxes.cls.cpu().numpy()[0])
        conf = image_result.boxes.conf.cpu().numpy()[0]
        box_dict = bbx_to_json(box_list, label=cls, score=conf)
        results["image_metadata"][f"det_{idx}"] = box_dict

    return results
