import numpy as np
import cv2
import pickle
import os

def img_to_encoding(image_path, model):
    img1 = cv2.imread(image_path, 1)
    print("original:", img1.shape)
    img1 = cv2.resize(img1, (160,160))
    x_train = np.array([img1])
    embedding = model.predict_on_batch(x_train)
    return embedding

# loads and resizes an image
def resize_img(image_path, save_path):
    img = cv2.imread(image_path, 1)
    # img = cv2.resize(img, (96, 96)) # skipping for facenet model
    img = cv2.resize(img, (160, 160))
    cv2.imwrite(image_path, img)


input_shape = (3, 160, 160)

faces = []

images = {}


def batch_generator(batch_size=16):
    y_val = np.zeros((batch_size, 2, 1))
    anchors = np.zeros((batch_size, input_shape[0], input_shape[1], input_shape[2]))
    positives = np.zeros((batch_size, input_shape[0], input_shape[1], input_shape[2]))
    negatives = np.zeros((batch_size, input_shape[0], input_shape[1], input_shape[2]))

    while True:
        for i in range(batch_size):
            positiveFace = faces[np.random.randint(len(faces))]
            negativeFace = faces[np.random.randint(len(faces))]
            while positiveFace == negativeFace:
                negativeFace = faces[np.random.randint(len(faces))]

            positives[i] = images[positiveFace][np.random.randint(len(images[positiveFace]))]
            anchors[i] = images[positiveFace][np.random.randint(len(images[positiveFace]))]
            negatives[i] = images[negativeFace][np.random.randint(len(images[negativeFace]))]

        x_data = {'anchor': anchors,
                  'anchorPositive': positives,
                  'anchorNegative': negatives
                  }

        yield (x_data, [y_val, y_val, y_val])

if __name__ == '__main__':

    batch_generator()