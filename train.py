from ultralytics import YOLO

if __name__ == '__main__':
	model = YOLO('yolov8n.pt')
	results = model.train(data='./cube.yaml', epochs=100, imgsz=640)