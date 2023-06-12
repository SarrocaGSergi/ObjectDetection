import torch
import uvicorn
from utils import save_file, detect_objects
from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File, HTTPException


app = FastAPI()
detector = YOLO("src/yolov8n.pt")
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


@app.post("/object-detector", status_code=202, summary="Image object detector endpoint")
async def process_image(file: UploadFile = File(...)):

    # Read the uploaded file
    file_bytes = await file.read()
    file_root = save_file(file_bytes=file_bytes, name=file.filename)

    try:
        results = detect_objects(detector, file_root)
        return results
    except Exception as err:
        raise HTTPException(status_code=404, detail=f"Error while object detection with image {file.filename}")


if __name__ == "__main__":
    uvicorn.run("api:app", host="10.62.50.11", port=5000, reload=True)