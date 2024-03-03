import torch
import numpy as np
import cv2
from time import time
from sort import sort

class ObjectDetection:
    # 
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.object_tracker = sort.Sort()

    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        self.model.to(self.device)
        results = self.model([frame])
        tracked_objects = self.object_tracker.update(results.xyxyn[0].cpu())
        labels, cord = results.xyxyn[0][:, -1].cpu().numpy(), results.xyxyn[0][:, :-1].cpu().numpy()
        print(labels)
        print(tracked_objects)
        return labels, cord, tracked_objects

    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]

    def plot_boxes(self, results, frame, track):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, (self.class_to_label(labels[i]) + ": " + str(round((row[2]-row[0])*(row[3]-row[1]),4))) + ", " + str(track[i][4] if i < len(track) else ''), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        return frame

    def __call__(self, image):
        objects, locations, tracked_objects = self.score_frame(image)
        output_data = []
        for i in range(len(objects)):
            d = {'name': self.classes[objects[i]], 'x1': locations[i][0], 'y1': locations[i][1], 'x2': locations[i][2], 'y2':locations[i][3], 'certainty':locations[i][4]}
            d['area'] = (d["x2"] - d["x1"]) * (d["y2"] - d["y1"])
            if i < len(tracked_objects):
                d['id'] = tracked_objects[i][4]
            output_data.append(d)
            
        return(output_data, self.plot_boxes((objects, locations), image, tracked_objects))