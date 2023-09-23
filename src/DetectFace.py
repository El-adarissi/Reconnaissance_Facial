from tkinter import messagebox

import cv2.cv2 as cv
import face_recognition

face_image_encoding = None
face_exist = 0
message = 0


def detectFaceImage(image_path):
    global face_image_encoding
    face = face_recognition.load_image_file(image_path)
    rgb_face = face[:, :, ::-1]
    location = face_recognition.face_locations(face)
    face_image_encoding = face_recognition.face_encodings(face)
    for (top, right, bottom, left) in location:
        cv.rectangle(face, (left, top), (right, bottom), (255, 0, 0), 2)
    return face


def resetFaceEncoding():
    global face_image_encoding
    face_image_encoding = None


def detectFaceVideo(cap):
    ret, frame = cap.read()
    if cap.isOpened():
        frame, mess, num_faces, sim, nonsim = createRectangle(frame)
        return ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB), mess, num_faces, sim, nonsim
    else:
        return None, None, None, None, None, None


def createRectangle(frame):
    resized_frame = cv.resize(frame, [0, 0], fx=1 / 3, fy=1 / 3)
    rgb_resized_frame = resized_frame[:, :, ::-1]
    face_localisation = face_recognition.face_locations(rgb_resized_frame)
    video_encoding = face_recognition.face_encodings(rgb_resized_frame)
    frame, mess, sim, nonsim = compareFaces(frame, face_image_encoding, video_encoding, face_localisation)
    return frame, mess, len(face_localisation), sim, nonsim


def compareFaces(frame, image_encoding, video_encoding, face_locations):
    global face_exist, message, similarfaces, nonsimilarfaces
    try:
        if image_encoding:
            similarfaces, nonsimilarfaces = 0, 0
            matches = []
            for i in range(len(face_locations)):
                res = face_recognition.compare_faces(image_encoding, video_encoding[i])
                matches.append(*res)
            for i in range(len(matches)):
                for top, right, bottom, left in [face_locations[i]]:
                    cv.rectangle(frame, (left * 3, top * 3), (right * 3, bottom * 3), (0, 0, 255), 3)
                    face_exist += 1
                    similarfaces = 1
                    if not matches[i]:
                        cv.rectangle(frame, (left * 3, top * 3), (right * 3, bottom * 3), (255, 0, 0), 3)
                        face_exist = 0
                        nonsimilarfaces = 0
                        if len(face_locations) > 1:
                            nonsimilarfaces = len(face_locations) - 1
            message = face_exist
        return frame, message, similarfaces, nonsimilarfaces
    except:
        messagebox.showwarning("no image", "insert image first!")
        return frame, 0, 0, 0
