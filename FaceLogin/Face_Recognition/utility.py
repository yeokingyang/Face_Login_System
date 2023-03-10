# for taking images from webcam
import cv2
from . import webcam_utility

def detect_face(user_db, FRmodel):
    save_loc = r'FaceLogin/Face_Recognition/saved_image/UserGenerated.jpg'
    capture_obj = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    capture_obj.set(3, 640)  # WIDTH
    capture_obj.set(4, 480)  # HEIGHT

    face_cascade = cv2.CascadeClassifier(
        r'FaceLogin/Face_Recognition/haarcascades/haarcascade_frontalface_default.xml')
    
    # whether there was any face found or not
    face_found = False
    
    if capture_obj.isOpened():
        while(True):
        # capture_object frame-by-frame
            ret, frame = capture_obj.read()
            if ret:
                # mirror the frame
                frame = cv2.flip(frame, 1, 0)

                # Our operations on the frame come here
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # detect face
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        
                # Display the resulting frame
                for (x, y, w, h) in faces:
                    # required region for the face
                    roi_color = frame[y-90:y+h+70, x-50:x+w+50]
                    # save the detected face
                    cv2.imwrite(save_loc, roi_color)
                    # draw a rectangle bounding the face
                    cv2.rectangle(frame, (x-10, y-70),
                          (x+w+20, y+h+40), (15, 175, 61), 4)

                # display the frame with bounding rectangle
                cv2.imshow('Press q to capture', frame)
                # close the webcam when 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        # release the capture_object
        capture_obj.release
    cv2.destroyAllWindows()

    img = cv2.imread(save_loc)
    if img is not None:
        face_found = True
    else:
        face_found = False

    return face_found
    
