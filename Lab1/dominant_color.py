# Source: Kmeans clustering dominant color tutorial

import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    # img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    x,y,w,h = 400, 150, 500, 400
    # crop image to isolate central rectangle
    cropped_img = img[150:550, 400:900]
    # represent as row*column,channel number
    cropped_img = cropped_img.reshape((cropped_img.shape[0] * cropped_img.shape[1],3))
    clt = KMeans(n_clusters=3) #cluster number
    clt.fit(cropped_img)

    hist = find_histogram(clt)
    bar = plot_colors2(hist, clt.cluster_centers_)

    plt.axis("off")
    cv2.imshow('bar', bar)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),thickness=2)
    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
