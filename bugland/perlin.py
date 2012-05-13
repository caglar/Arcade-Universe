from __future__ import division

import Image, ImageDraw
import numpy as np

#This is a perlin noise generating script
class PerlinNoiseGenerator(object):
	def __init__(self, w, h, size=64, rnd=12312):
		self.w = w
		self.h = h
		self.rnd = rnd
		self.size = size
		self.rng = np.random.RandomState(self.rnd)

	def generate_noise(self):
		noise = np.array(np.zeros(self.w*self.h))
		noise = noise.reshape((self.w,self.h))
		for x in xrange(self.w):
			for y in xrange(self.h):
				noise[x][y] = (self.rng.random_integers(0, 32768) / 32768)
		return noise

	def smoothnoise(self, x, y, noise):
		x_i = int(x)
		y_i = int(y)
		fract_x = x - x_i
		fract_y = y - y_i

		x1 = (x_i + self.w) % self.w
		y1 = (y_i + self.h) % self.h

		#Neighbour Values
		x2 = (x1 + self.w - 1) % self.w
		y2 = (y1 + self.h - 1) % self.h

		#smooth the noise with bilinear interpolation
		val = 0.0
		val += fract_x * fract_y * noise[x1][y1]
		val += fract_x * (1 - fract_y) * noise[x1][y2]
		val += (1 - fract_x) * fract_y * noise[x2][y1]
		val += (1 - fract_x) * (1 - fract_y) * noise[x2][y2]
		return val

	def turbulence(self, x, y, noise, size=0):
		val = 0.0
		if size == 0:
			size = self.size
		init_size = size
		while(size>=1):
			val += self.smoothnoise(x/size, y/size, noise) * size
			size /= 2.0
		
		return (128 * val/init_size)

	def gen_img(self):
		img = Image.new("RGB", (self.w, self.h), "#FFFFFF")
		draw = ImageDraw.Draw(img)
		noise = self.generate_noise()
		for x in xrange(self.w):
			for y in xrange(self.h):
				r = g = b = int(self.turbulence(x, y, noise))
				draw.point((x, y) , fill=(r, g, b))
		img.save("out.png", "PNG")

if __name__=="__main__":
	perl = PerlinNoiseGenerator(32, 32, size=32)
	perl.gen_img()
