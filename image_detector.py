import torch
import numpy as np
import cv2
from time import time

class ObjectDetection:
    #create object and load computer vision model
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.prev_obj = False
    
    #code for keeping track/storing of large objects on screen
    def set_prev_obj(self, new_obj):
        self.prev_obj = new_obj

    def get_prev_obj(self):
        return self.prev_obj

    #takes in a webcame from the frame and returns labels w/ coordinates
    def score_frame(self, frame):
        self.model.to(self.device)
        results = self.model([frame])
        labels, cord = results.xyxyn[0][:, -1].cpu().numpy(), results.xyxyn[0][:, :-1].cpu().numpy()
        return labels, cord

    #returns the object types for integrers
    def class_to_label(self, x):
        return self.classes[int(x)]

    #Takes in frame and data and returns a frame with printed objects
    def plot_boxes(self, results, frame):
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, (self.class_to_label(labels[i]) + ": " + str(round((row[2]-row[0])*(row[3]-row[1]),4))), (x1 + 10, y1 + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
        return frame

    #Main call function that gives final frame and info back to main function
    def __call__(self, image):
        objects, locations = self.score_frame(image)
        output_data = []
        for i in range(len(objects)):
            d = {'name': self.classes[objects[i]], 'x1': locations[i][0], 'y1': locations[i][1], 'x2': locations[i][2], 'y2':locations[i][3], 'certainty':locations[i][4]}
            d['area'] = (d["x2"] - d["x1"]) * (d["y2"] - d["y1"])
            output_data.append(d)
            
        return(output_data, self.plot_boxes((objects, locations), image))