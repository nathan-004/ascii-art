import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

# https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html

def resize_with_aspect_ratio(image, width=None, height=None):
    # Get the original image dimensions
    h, w = image.shape[:2]

    # Calculate the aspect ratio
    aspect_ratio = w / h

    if width is None:
        # Calculate height based on the specified width
        new_height = int(height / aspect_ratio)
        resized_image = cv.resize(image, (height, new_height))
    else:
        # Calculate width based on the specified height
        new_width = int(width * aspect_ratio)
        resized_image = cv.resize(image, (new_width, width))

    return resized_image

def get_edges(image_path, threshold1=100, threshold2=200, resize_width=None, resize_height=None, display=False):
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
    img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    assert img is not None, f"{image_path} inexistant."
    if resize_width is not None or resize_height is not None:
        img = resize_with_aspect_ratio(img, width=resize_width, height=resize_height)
    edges = cv.Canny(img, threshold1, threshold2) # Numpy Array 

    if display:
        plt.subplot(121),plt.imshow(img,cmap = 'gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(edges,cmap = 'gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        
        plt.show()
    print(len(edges[0]), len(edges))
    return edges

def get_edges_directions(image_path=None, edges=None):
    """
    Retourne les pixels avec des contours sous forme de direction

    Parameters
    ----------
    image_path:str
    edges:Numpy Array
        Image en niveaux de gris avec 255 étant un contour

    Returns
    -------
    liste contenant la position de chaque pixels considéré comme un contour et leurs directions
    """
    assert image_path is not None or edges is not None, "Aucun argument donné."

    if edges is None:
        edges = get_edges(image_path)
    
    def get_direction(x,y):
        """Retourne la liste des pixels voisins qui sont des contours"""
        neighbors = []
        for y_modif in range(-1, 2, 1):
            for x_modif in range(-1, 2, 1):
                if y_modif == 0 and x_modif == 0:
                    continue
                if 0 <= y + y_modif < edges.shape[0] and 0 <= x + x_modif < edges.shape[1]:
                    if edges[y + y_modif][x + x_modif] > 0:
                        neighbors.append((y_modif, x_modif))
        return neighbors
    
    pixels = []
    for y, line in enumerate(edges):
        for x, color in enumerate(line):
            if color > 0:
                pixels.append(((x,y), get_direction(x,y)))
    
    return pixels