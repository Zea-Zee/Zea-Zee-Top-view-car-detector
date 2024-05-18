from ultralytics import YOLO
import torch
print(torch.cuda.is_available())
print(torch.cuda.device_count())


model = YOLO('yolov8n.yaml')  # build a new model from YAML
model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)
model = YOLO('yolov8n.yaml').load('yolov8n.pt')  # build from YAML and transfer weights

# Train the model
results = model.train(data='coco8.yaml', epochs=100, imgsz=640)
