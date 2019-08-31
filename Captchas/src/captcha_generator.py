# PraktijkOpdracht AI 2

from captcha.image import ImageCaptcha
from PIL import Image
import random
import numpy as np
import matplotlib.pylab as plt
import math
from itertools import product

import os

# PIP COMMANDS:
# python3 -m venv .venv
# source .venv/bin/activate
# python3 -m pip install numpy
# python3 -m pip install matplotlib

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
data_dir = '../data'


def get_all_possible_label_categories(nr_of_chars, number=False):
    if not number:
        labels = [''.join(i) for i in product(alphabet, repeat=nr_of_chars)]
        return labels
    else:
        labels = [''.join(i) for i in product(numbers, repeat=nr_of_chars)]
        return labels


def get_captcha(width=64, height=64, text='a', color=False):
    # Generate captcha.
    image = ImageCaptcha(width, height)
    captcha = image.generate_image(text)

    # Preprocess it into a greyscale numpy array.
    final = captcha
    data = None
    if not color:
        final = final.convert('L')
        (width, height) = final.size
        data = list(final.getdata())
        data = np.array(data)
        data = data.reshape((width, height))
    else:
        final = final.convert('RGB')
        data = list(final.getdata())
        data = np.array(data)
        data = data.reshape((width, height, 3))

    return data, text


def get_data_set(width=64, height=64, color=False, nr_of_chars=1, nr_of_captchas=100, number=False):
    labels = []
    images = []

    for i in range(nr_of_captchas):
        text = ''
        for a in range(nr_of_chars):
            if not number:
                text = text + random.choice(alphabet)
            else:
                text = text + str(random.choice(numbers))

        data, label = get_captcha(width=width, height=height, text=text, color=color)
        labels.append(label)
        images.append(data)

    return np.array(images), np.array(labels)


def main():
    # images, labels = get_data_set(color=True, nr_of_captchas=1)
    # print(labels[0])
    # print(images[0])
    # plt.imshow(images[0])
    # plt.show()
    one = get_all_possible_label_categories(1)
    two = get_all_possible_label_categories(2)
    three = get_all_possible_label_categories(3)
    print(one)
    print(two)
    print(len(two))
    print(len(three))


if __name__ == '__main__':
    main()
