Object Detector API
===================

This project aims to create an API for encoding an object detector. The API will allow users to send images or video frames and receive predictions about the objects present in the input data. The project will utilize a pre-trained object detection model to perform the inference.

Features
--------

*   Accept images. 
*   Provide predictions about the objects (cars & persons) present in the input data.
*   Support multiple object detection models.
*   Efficient and scalable architecture for handling multiple concurrent requests.
*   RESTful API endpoint for easy integration with other applications.


Installation
------------

1.  Clone the repository:

shell

```shell
git clone https://github.com/SarrocaGSergi/objectdetection.git
```

2.  Install the required dependencies:

shell

```shell
cd objectdetection
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Usage
-----

1.  Start the API server:

shell

```shell
python3 api.py
```

2.  Send a POST request to the following endpoint to perform object detection:

bash

```bash
POST /object-detector
```

3.  Include the input image or video frame in the request payload.
4.  Receive the response with the detected objects and their corresponding bounding boxes in json format.

API information
-------------

The model used was configured as follows:

*   `MODEL_NAME`: Yolov8 nano
*   `IMAGE_SIZE`: Any. 
*   `THRESHOLD`: 0.75
*   `CLASSES`: Car, Person

