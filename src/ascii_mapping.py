# Déterminer quelles caractères ASCII utiliser #
# -------------------------------------------- #
import cv2 as cv

from edge_detection import get_edges_directions, get_edges, resize_with_aspect_ratio

class AsciiCharacters:
    """Caractères ascii pour chaque croisements"""
    default = " "
    vertical = "|"
    horizontal = "─"
    diagonal_bl_tr = "/"
    diagonal_br_tl = '\\'

    # Coins
    corner_bl = "└"

    ascii_chars = [' ', '.', '\'', '`', '^', '"', ',', ':', ';', '!', '~',
                '-', '_', '+', '<', '>', 'i', 'l', '?', '1', '(', ')',
                '[', ']', '{', '}', '/', '\\', '|', 't', 'f', 'j', 'r',
                'x', 'n', 'u', 'v', 'c', 'z', 'X', 'Y', 'U', 'J', 'C',
                'L', 'Q', '0', 'O', 'Z', 'm', 'w', 'q', 'p', 'd', 'b',
                'k', 'h', 'a', 'o', '*', '#', 'M', 'W', '&', '8', '%',
                'B', '@', '$']

class bcolors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    INVERT = '\033[7m'
    HIDDEN = '\033[8m'

class AsciiMapping:
    def __init__(self, edges, image_size):
        """
        Parameters
        ----------
        edges:list
            Liste sous forme [(x,y), [(x_voisin, y_voisin)]]
        image_size:tuple
            (largeur, longueur)
        """
        self.width = image_size[1]
        self.height = image_size[0]
        self.ascii_result = self.generate(edges)
    
    def generate(self, edges):
        """Créé une image consituée de texte à partir des contours"""
        
        image = [[AsciiCharacters.default for x in range(self.width)] for y in range(self.height)]

        for pixel in edges:
            coord, neighbors = pixel[0], pixel[1]
            if (-1,1) in neighbors and (1,0) in neighbors:
                image[coord[1]][coord[0]] = AsciiCharacters.corner_bl
            elif (0,1) in neighbors or (0,-1) in neighbors:
                image[coord[1]][coord[0]] = AsciiCharacters.vertical
            elif (1,0) in neighbors or (-1, 0) in neighbors:
                image[coord[1]][coord[0]] = AsciiCharacters.horizontal
            elif (-1,-1) in neighbors and (1,1) in neighbors:
                image[coord[1]][coord[0]] = AsciiCharacters.diagonal_bl_tr
            elif (1,-1) in neighbors and (-1,1) in neighbors:
                image[coord[1]][coord[0]] = AsciiCharacters.diagonal_br_tl
        return image
    
    def fill(self, image_path, resize_width=None, resize_height=None):
        """Utiliser des caractères pour simuler si un pixel est sombre ou pas"""
        img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
        if resize_width is not None or resize_height is not None:
            img = resize_with_aspect_ratio(img, width=resize_width, height=resize_height)

        for y, line in enumerate(self.ascii_result):
            for x, ascii_pixel in enumerate(line):
                if ascii_pixel == ' ':
                    self.ascii_result[y][x] = AsciiCharacters.ascii_chars[int(img[y][x] / 255 * (len(AsciiCharacters.ascii_chars) - 1))]

    def print(self):
        """Print the ascii image in the terminal"""
        result = ""
        for line in self.ascii_result:
            result += "".join(line) + "\n"

        print(result)

        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(result)

img_path = "assets/sample2.jpg"

edges_img = get_edges(img_path, threshold1=100, threshold2=200, resize_width=750, display=True)
edges = get_edges_directions(edges=edges_img)
ascii = AsciiMapping(edges, (edges_img.shape[:2]))
ascii.fill(img_path, resize_width=750)
ascii.print()