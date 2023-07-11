from flask import Flask, render_template, request
import base64
from viewport import Viewport
from math import log
import PIL.Image as Image
import numpy as np

class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0

    def __init__(self, max_iterations, escape_radius):
        self.max_iterations = max_iterations 
        self.escape_radius = escape_radius

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1
    
    def stability(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.escape_count(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value
    
    def escape_count(self, c: complex, smooth=False) -> float:
        z = 0
        for iteration in range(self.max_iterations):
            z = z ** 2 + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iteration + 1 - log(log(abs(z))) / log(2)
                return iteration
        return self.max_iterations


def paint(mandelbrot_set, viewport, mapping, smooth, iterations):
    for pixel in viewport:
        stability = mandelbrot_set.stability(complex(pixel), smooth)
        layer = stability*iterations
        pixel.color = (0, 0, 0) if stability == 1 else mapping[int(layer % 16)]

mapping = [(66, 30, 15), (25, 7, 26), (9, 1, 47), (4, 4, 73), (0, 7, 100), (12, 44, 138), (24, 82, 177), (57, 125, 209), (134, 181, 229), (211, 236, 248), (241, 233, 191), (248, 201, 95), (255, 170, 0), (204, 128, 0), (153, 87, 0), (106, 52, 3)] 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/calculate', methods=["POST"])
def calculate():
    real = float(request.json["real"])
    imaginary = float(request.json["imaginary"])
    zoom = 3 * (1 - 1/(2**3))**int(request.json["zoom"])
    iterations = int(request.json["iterations"])

    
    #function to generate await
    mandelbrot_set = MandelbrotSet(max_iterations=int(iterations), escape_radius=1000)
    width, height = 512*2, 512*2
    center = complex(real, imaginary)
    image = Image.new(mode="RGB", size=(width, height))
    viewport = Viewport(image, center=center, width=zoom)
    paint(mandelbrot_set, viewport, mapping, True, iterations)
    image.save("image.png")
    base = base64.encodebytes(open("image.png", "rb").read())
    return base

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')