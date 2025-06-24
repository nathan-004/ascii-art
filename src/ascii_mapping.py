# Déterminer quelles caractères ASCII utiliser #
# -------------------------------------------- #

from edge_detection import get_edges_directions

class AsciiCharacters:
    """Caractères ascii pour chaque croisements"""
    default = " "
    vertical = "|"
    horizontal = "─"

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
        self.width = image_size[0]
        self.height = image_size[1]
        self.ascii_result = self.generate(edges)
    
    def generate(self, edges):
        """Créé une image consituée de texte à partir des contours"""
        
        image = [[AsciiCharacters.default for x in range(self.width)] for y in range(self.height)]

        for pixel in edges:
            coord, neighbors = pixel[0], pixel[1]
            
            if len(neighbors) == 2 or len(neighbors) == 1:
                if (0,1) in neighbors or (0,-1) in neighbors:
                    image[coord[1]][coord[0]] = AsciiCharacters.vertical
                if (1,0) in neighbors or (-1, 0) in neighbors:
                    image[coord[1]][coord[0]] = AsciiCharacters.horizontal

        return image
    
    def print(self):
        """Print the ascii image in the terminal"""
        result = ""
        for line in self.ascii_result:
            result += "".join(line) + "\n"

        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(result)

ascii = AsciiMapping(get_edges_directions("assets/sample.jpg"), (749, 1280))
ascii.print()