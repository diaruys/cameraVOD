from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse

import cv2
import urllib.request
import threading
# import numpy as np

# Create your views here.


@gzip.gzip_page
def Home(request):
    try:
        cam = videoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

    return render(request, 'index.html')


# RTSP Stream
class videoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(
            "rtsp://admin:xX533440@192.168.5.11:554/sub")
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
