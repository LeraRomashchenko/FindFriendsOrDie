#!/usr/bin/env python2
import logging
from logging import config
import urllib
import time
import os
import openface
import cv2
import numpy as np
from people_sqlite import PeopleSqlite

# noinspection PyUnresolvedReferences

logging.config.fileConfig('log.ini')
log = logging.getLogger('recognizer')

log.info("starting")


class PhotoRecognizer:
    def __init__(self, image_dim, openface_models_dir):
        face_predictor = os.path.join(openface_models_dir, 'dlib/shape_predictor_68_face_landmarks.dat')
        network_model = os.path.join(openface_models_dir, 'openface/nn4.small2.v1.t7')
        self.align = openface.AlignDlib(face_predictor)
        self.net = openface.TorchNeuralNet(network_model, image_dim)
        self.image_dir = image_dim

    def _extract_features(self, image):
        bounding_boxes = self.align.getAllFaceBoundingBoxes(image)
        self._log_boxes(bounding_boxes)
        aligned_faces = (
            self.align.align(self.image_dir, image, bb)
            for bb in bounding_boxes
        )
        return [self.net.forward(f) for f in aligned_faces]

    def _to_cv_image(self, image_bytes):
        image_bytes = np.asarray(bytearray(image_bytes), dtype="uint8")
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def _log_boxes(self, bounding_boxes):
        boxes = [box for box in bounding_boxes]
        log.info("Bounding boxes: %s" % boxes)

    def _load_images(self, urls):
        log.info("Loading %i images" % len(urls))
        resps = (urllib.urlopen(url) for url in urls)
        return (response.read() for response in resps)

    def recognize_all(self, remain):
        with PeopleSqlite("people.db", log) as db:
            while True:
                image_dtos = list(db.get_unrecognized_images(20))

                if len(image_dtos) == 0:
                    log.info("No unrecognized images found in DB")
                    if remain:
                        time.sleep(5)
                        continue
                    else:
                        break

                ids = [img_id for (img_id, _) in image_dtos]
                urls = [url for (_, url) in image_dtos]
                images_bytes = self._load_images(urls)

                for (img_id, image_bytes, url) in zip(ids, images_bytes, urls):
                    if image_bytes is None:
                        log.error("Couldn't load image '%s'" % url)
                    else:
                        log.info("Extracting features of '%s'" % url)
                        image = self._to_cv_image(image_bytes)
                        features = self._extract_features(image)
                        db.add_faces(img_id, features)

                time.sleep(1)  # don't load too frequently


file_dir = os.path.dirname(os.path.realpath(__file__))
openface_models_dir = os.path.join(file_dir, '../openface/models')

PhotoRecognizer(96, openface_models_dir).recognize_all(remain=True)
