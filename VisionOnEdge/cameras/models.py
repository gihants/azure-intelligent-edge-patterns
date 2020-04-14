import datetime

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
import cv2

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, Region

from vision_on_edge.settings import TRAINING_KEY, ENDPOINT
trainer = CustomVisionTrainingClient(TRAINING_KEY, endpoint=ENDPOINT)

is_trainer_valid = True

try:
    obj_detection_domain = next(domain for domain in trainer.get_domains() if domain.type == "ObjectDetection" and domain.name == "General")
except:
    is_trainer_valid = False



# Create your models here.
class Part(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    coordinates = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Camera(models.Model):
    name = models.CharField(max_length=200)
    rtsp = models.CharField(max_length=1000)
    model_name = models.CharField(max_length=200)

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    labels = models.CharField(max_length=1000, null=True)

class Annotation(models.Model):
    image = models.OneToOneField(Image, on_delete=models.CASCADE)
    labels = models.CharField(max_length=1000, null=True)

class Project(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    parts = models.ManyToManyField(
                Part, related_name='part')
    customvision_project_id = models.CharField(max_length=200)
    customvision_project_name = models.CharField(max_length=200)

    @staticmethod
    def pre_save(sender, instance, **kwargs):
        print('[INFO] Creating Project on Custom Vision')
        name = 'VisionOnEdge-' + datetime.datetime.utcnow().isoformat()
        instance.customvision_project_name = name

        if is_trainer_valid:
            project = trainer.create_project(name, domain_id=obj_detection_domain.id)
            instance.customvision_project_id = project.id
        else:
            instance.customvision_project_id = 'DUMMY-PROJECT-ID'

pre_save.connect(Project.pre_save, Project, dispatch_uid='Project')



# FIXME consider move this out of models.py
class Stream(object):
    def __init__(self, rtsp, part_id=None):
        if rtsp == '0': self.rtsp = 0
        elif rtsp == '1': self.rtsp = 1
        else: self.rtsp = rtsp
        self.part_id = part_id

        #self.last_active = datetime.datetime.now()
        self.status = 'init'
        self.last_img = None
        self.id = id(self)

    def gen(self):
        self.status = 'running'
        print('[INFO] start streaming with', self.rtsp)
        self.cap = cv2.VideoCapture(self.rtsp)
        while self.status == 'running':
            t, img = self.cap.read()
            img = cv2.resize(img, None, fx=0.5, fy=0.5)
            self.last_img = img
            yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', img)[1].tobytes() + b'\r\n')
        self.cap.release()


    def get_frame(self):
        print('[INFO] get frame', self)
        b, img = self.cap.read()
        if b: return cv2.imencode('.jpg', img)[1].tobytes()
        else : return None


    def close(self):
        self.status = 'stopped'
        print('[INFO] release', self)