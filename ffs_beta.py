import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft

class FFS(object):
    '''
    Description

    ATTRIBUTES:
        - x: x-coordinates (ndarray)
        - y: y-coordinates (ndarray)
        - pad: number of data points to pad the x, y vectors with (int)
        - thresh: threshold used for noise removal.  must be a number
        between 0 and 1.  (float)
    '''
    def __init__(self, x, y, pad = 0, thresh = 0):
        '''
        INPUT:
            - x: x-coordinates (ndarray)
            - y: y-coordinates (ndarray)
            - pad: number of data points to pad the x, y vectors with (int)
            - thresh: threshold used for noise removal (float)
        OUTPUT: None
        '''
        if thresh > 0 and thresh < 1:
            y = self.remove_noise(y, thresh)
        if pad > 0:
            x, y = self.fourier_pad(x, y, pad)
        self.x = x
        self.y = y
        self.n = len(x) # length of x, y
        self.xa = x[0] # min of x
        self.xb = x[-1] # max of x
        L = x[-1] - x[0]
        self.h = 1.*L/(self.n - 1) # increment size of x
        self.L = L + self.h # span of x + h

        yt = fft(y) # fourier transformation of y
        # only use first half of yt for Fourier Series coeffcients
        self.m = int(np.ceil(self.n/2))

        # define a0
        self.a0 = yt[0].real/self.n
        # set c equal to first half of Fourier Coefficients
        self.c = 2*yt[1:self.m]/self.n
        # a = cosine coefficients
        self.a = self.c.real
        # b = sine coefficients
        self.b = -self.c.imag

    def remove_noise(self, y, thresh):
        yt = fft(y)
        yt0 = yt[0]
        yt = yt[1:]
        yt_abs = np.absolute(yt)
        yt_max = np.max(yt_abs)
        indices = np.where(yt_abs < thresh*yt_max)[0]
        yt[indices] = np.complex(0,0)
        return ifft(np.hstack((yt0, yt)))

    def fourier_pad(self, x, y, p):
        n = len(x)
        xa = x[0]
        xb = x[-1]
        L = xb - xa
        h = L/(n-1)
        m = n + p
        xc = xa + m*h

        xpad = xb + h*np.arange(1,p+1)

        # set values used for splines
        x1, x2, x3, x4 = x[-2], x[-1], xc, xc + h
        y1, y2, y3, y4 = y[-2], y[-1], y[0], y[1]

        # linear splines
        s12_1 = ((x2 - xpad)*y1 + (xpad - x1)*y2) / (x2 - x1)
        s23_1 = ((x3 - xpad)*y2 + (xpad - x2)*y3) / (x3 - x2)
        s34_1 = ((x4 - xpad)*y3 + (xpad - x3)*y4) / (x4 - x3)

        # quadratic splines
        s13_2 = ((x3 - xpad)*s12_1 + (xpad - x1)*s23_1) / (x3 - x1)
        s24_2 = ((x4 - xpad)*s23_1 + (xpad - x2)*s34_1) / (x4 - x2)

        # cubic spline
        s14_3 = ((x4 - xpad)*s13_2 + (xpad - x1)*s24_2) / (x4 - x1)

        # add padding to original x and y vectors
        xx = np.hstack((x, xpad))
        yy = np.hstack((y, s14_3))

        return xx, yy

    def evaluate(self, x, N = None, deriv = 0):
        # if x not an ndarray cast it as one
        if type(x) in [float, int, np.float64]:
            x = np.array([x])
        # initalize y as a0
        # transform x to be in range of xa to xb
        omega = 2*np.pi/self.L
        # x = 2*np.pi*(x - self.xa)/self.L
        x = omega*(x-self.xa)
        # set N, order of Fourier Series
        if N == None:
            N = self.m - 1
        else:
            N = np.min([N - 1, self.m - 1])
        # calculate y over order N Fourier Series
        if deriv == 0:
            y = self.a0*np.ones(len(x))
            for k in xrange(0, N):
                y += self.a[k]*np.cos(x*(k+1)) + self.b[k]*np.sin(x*(k+1))
        elif deriv == 1:
            y = np.zeros(len(x))
            for k in xrange(0, N):
                y += (k+1)*(-self.a[k]*np.sin(x*(k+1)) + self.b[k]*np.cos(x*(k+1)))
            y *= omega
        elif deriv == 2:
            y = np.zeros(len(x))
            for k in xrange(0, N):
                y += ((k+1)**2)*(-self.a[k]*np.cos(x*(k+1)) - self.b[k]*np.sin(x*(k+1)))
            y *= omega**2
        return y


if __name__ == '__main__':
    x = np.linspace(-2,2,50)
    y = np.exp(-x**2)

    # xx, yy = fourier_pad(x,y,200)

    # plt.plot(x,y)
    # plt.show()

    f = FFS(x,y,0)
    # xx, yy = f.fourier_pad(x,y,50)
    ypred = f.evaluate(x)
    # plt.plot(y, 'r')
    # plt.plot(ypred, 'b')
    # plt.show()


    # xright = np.linspace(6,14,100)
    plt.plot(x,y,'b', linewidth = 5)
    plt.plot(x,ypred,'r')
    # plt.plot(xright, f.eval(xright), 'g')
    plt.show()
