import torch
import uvicorn
from tools import save_file, detect_objects
from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks


app = FastAPI()
detector = YOLO("yolov8n.pt")
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class MyDetections:
    def __init__(self, results: dict):
        self.results = results

    def update_detections(self, new_dict: dict):
        self.results=new_dict


@app.post("/object-detector", status_code=202, summary="Image object detector endpoint")
async def process_image(file: UploadFile = File(...), background_tasks=BackgroundTasks):

    # Read the uploaded file
    file_bytes = await file.read()
    file_root = save_file(file_bytes=file_bytes, name=file.filename)
    storage_object = MyDetections(results={})
    try:
        background_tasks(detect_objects(detector, storage_object, file_root))
        return storage_object.results
    except Exception as err:
        raise HTTPException(status_code=404, detail=f"Error while object detection with image {file.filename}")


if __name__ == "__main__":
    uvicorn.run("api:app", host="10.62.50.11", port=5000, reload=True)
