import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def name():
    print("ragul nolan\n")
def fav():
    print("favorite food:briyani\n")
    print("favorite movie:intersteller\n")
    print("favorite director:christopher nolan\n")
def img():
    img = mpimg.imread('20UAI039.jpeg')
    imgplot = plt.imshow(img)
    plt.show()