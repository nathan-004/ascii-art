import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

# https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html

def get_edges(image_path, threshold1=100, threshold2=200, display=False):
    """
    Utilise la méthode Canny d'Opencv pour détecter les contours
    
    Parameters
    ----------
    image_path:str
        Chemin vers l'image
    threshold1:int, threshold2:int
        gradient > thersold2 -> gardé comme bord net | thresold1 < gradient < thresold2 -> gardé si connecté à un bord net | reste est supprimé
    
    Returns
    -------
    edges:Objet Numpy Array
        Image en niveaux de gris (255 = contour, 200 = autre)
    """
    img = cv.imread('assets/sample.jpg', cv.IMREAD_GRAYSCALE)
    assert img is not None, f"{image_path} inexistant."
    edges = cv.Canny(img, threshold1, threshold2) # Numpy Array 

    if display:
        plt.subplot(121),plt.imshow(img,cmap = 'gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(edges,cmap = 'gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        
        plt.show()
    
    return edges