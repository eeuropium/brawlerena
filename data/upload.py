from data.constants import *

def r(relative_path): #resource path
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def Image(image_path, *dimensions):
    if len(dimensions) != 0:
        width, height = dimensions[0], dimensions[1]
        image = pygame.image.load(r(image_path)).convert()
        image = pygame.transform.smoothscale(image, (width, height))
    else:
        image = pygame.image.load(r(image_path)).convert()
    return image
