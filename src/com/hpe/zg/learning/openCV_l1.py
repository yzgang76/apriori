import cv2

if __name__ == '__main__':
    # 脸
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face_cascade.load('C:\\Product\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml')

    # 眼睛
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    eye_cascade.load('C:\\Product\\opencv\\sources\\data\\haarcascades\\haarcascade_eye_tree_eyeglasses.xml')
    # 嘴巴
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
    mouth_cascade.load('C:\\Product\\opencv\\sources\\data\\haarcascades\\haarcascade_mcs_mouth.xml')
    # 鼻子
    nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
    nose_cascade.load('C:\\Product\\opencv\\sources\\data\\haarcascades\\haarcascade_mcs_nose.xml')
    # 耳朵
    leftear_cascade = cv2.CascadeClassifier('haarcascade_mcs_leftear.xml')
    leftear_cascade.load('C:\\Product\\opencv\\sources\\data\\haarcascades\\haarcascade_mcs_leftear.xml')
    rightear_cascade = cv2.CascadeClassifier('haarcascade_mcs_rightear.xml')
    rightear_cascade.load('C:\\Product\\opencv\\sources\\data\\haarcascades\\haarcascade_mcs_rightear.xml')

    # face_cascade = cv2.CascadeClassifier("../../opencv-2.4.9/data/haarcascades/haarcascade_frontalface_default.xml")
    # eye_cascade = cv2.CascadeClassifier('../../opencv-2.4.9/data/haarcascades/haarcascade_eye.xml')

    img = cv2.imread('C:\\p1.jpg')
    if img is None:
        print("Load Image file failed")
        exit(-1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 脸
    faces = face_cascade.detectMultiScale(gray, 1.2, 3)
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        # 眼睛
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, 3)
        print(eyes[0])
        # for (ex, ey, ew, eh) in eyes:
        #     cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        cv2.rectangle(roi_color, (eyes[0][0], eyes[0][1]), (eyes[0][0] + eyes[0][2], eyes[0][1] + eyes[0][3]),
                      (0, 255, 0), 2)
        cv2.rectangle(roi_color, (eyes[1][0], eyes[1][1]), (eyes[1][0] + eyes[1][2], eyes[1][1] + eyes[1][3]),
                      (0, 255, 0), 2)

        # 嘴巴
        # mouth = mouth_cascade.detectMultiScale(roi_gray, 1.5, 5)
        # for (mx, my, mw, mh) in mouth:
        #     cv2.rectangle(roi_color, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)
        # 鼻子
        # nose = nose_cascade.detectMultiScale(roi_gray, 1.2, 5)
        # for (nx, ny, nw, nh) in nose:
        #     cv2.rectangle(roi_color, (nx, ny), (nx + nw, ny + nh), (255, 0, 255), 2)

        # 耳朵
        # leftear = leftear_cascade.detectMultiScale(roi_gray, 1.01, 2)
        # for (lx, ly, lw, lh) in leftear:
        #     cv2.rectangle(roi_color, (lx, ly), (lx + lw, ly + lh), (0, 0, 0), 2)
        #
        # rightear = rightear_cascade.detectMultiScale(roi_gray, 1.01, 2)
        # for (rx, ry, rw, rh) in rightear:
        #     cv2.rectangle(roi_color, (rx, ry), (rx + rw, ry + rh), (0, 0, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
