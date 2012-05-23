import numpy as np

class HilbertCurves(object):

	def __init__(self, xi, yj, level=10):
		self.xi = xi
		self.yj = yj
		self.data = np.zeros((xi, yj))
		self.edges = []
		self.level = level

	def make_line(self, X, Y):
		if self.edges:
			i, j = self.edges[-1]
			xstart = int(min(i, X))
			xend = int(max(i, X))
			ystart = int(min(j, Y))
			yend = int(max(j, Y))
			if xstart == xend:
				for y in xrange(ystart, yend):
					self.data[xstart][y] = 1
			if ystart == yend:
				for x in xrange(xstart, xend):
					self.data[x][ystart] = 1

	def gen_hilbert_curve(self, xi=None, yj=None, level=-1):
		if xi is None:
			xi = self.xi

		if yj is None:
			yj = self.yj

		if level == -1:
			level = self.level

		if xi != yj:
			raise Exception("must be square.")
		
		elif (2**level >= xi):
			raise Exception("xi should be less then the power of two.")

		else:
			self.hilbert(0.0, 0.0, xi, 0.0, 0.0, yj, level)

	def hilbert(self, x0, y0, xi, xj, yi, yj, n):
		if n <= 0:
			X = x0 + (xi + yi)/2
			Y = y0 + (xj + yj)/2
			# Merge the dots
			self.make_line(X, Y)
			self.edges.append((X, Y))
		else:
			self.hilbert(x0,               y0,               yi/2, yj/2, xi/2, xj/2, n - 1)
			self.hilbert(x0 + xi/2,        y0 + xj/2,        xi/2, xj/2, yi/2, yj/2, n - 1)
			self.hilbert(x0 + xi/2 + yi/2, y0 + xj/2 + yj/2, xi/2, xj/2, yi/2, yj/2, n - 1)
			self.hilbert(x0 + xi/2 + yi,   y0 + xj/2 + yj,  -yi/2,-yj/2,-xi/2,-xj/2, n - 1)

if __name__=="__main__":
	hcurves = HilbertCurves(256, 256, 7)
	hcurves.gen_hilbert_curve()
	import pylab
	pylab.axis("off")
	pylab.gray()
	pylab.imshow(hcurves.data)
	pylab.show()
