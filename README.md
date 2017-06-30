# Fast Fourier Series

## Abstract
The Fourier Series is frequently used in solutions to partial
 differential equations such as the heat equation and the wave
 equation.  One of the defining characteristics is that given
 an infinite number of wave frequencies, any function that
 is piecewise smooth can be replicated exactly.  Having said that,
 it is an excellent tool for approximating a discrete function in
 continuous space.  Furthermore, another useful application of the
 Fourier Series is in digital signal processing; specifically in the
 realm of eliminating noise from a signal.  Having said that, the
 periodic nature of Fourier Series results in some discrete functions
 to be very difficult to represent continuously with a finite number
 of wave frequencies.  The purpose of this study is to provide a
 methodology for which any discrete function to
 be accurately represented in continuous space while eliminating
 noise from the signal using the Fast Fourier Transform.


## Overview
#### Fourier Series Fundamentals
Consider a piecewise smooth function, f(x), defined on the region

![alt text](images/equations/x_range.gif)

f(x) can be represented by the Fourier Series, s(x), as follows:

![alt text](images/equations/fourier_series_def.gif)

Where

![alt text](images/equations/L_def.gif)

#### Fourier Series from the Discrete Fourier Transform
Before the manner in which a Fourier Series is generated from the Discrete
Fourier Transform is described, the necessary input variables must be discussed.  Two vectors,
x and y, of length, N, are required to generate the Fourier Series.  The vector, x,
must be defined such that x[n] < x[n+1] for 0 <= n < N.  If xa = x[0] and xb = x[N-1],
then the span of x, L, is given by xb - xa as in the equation above.  The only restriction
on y is that its elements are real numbers.  The Fourier Coefficients a0, an, and bn
shown in the expression for s(x) above will be obtained by applying the Discrete
Fourier Transform to y.  It should be noted that the Fourier Series generated from
the Discrete Fourier Transform is an approximation, unlike the expression for s(x),
so the summation will go from 1 to N/2 rather than 1 to infinity.

The Discrete Fourier Transform used here is the Fast Fourier Transform from the
[scipy fftpack](https://docs.scipy.org/doc/scipy/reference/fftpack.html).  The fft function applied to y will
yield a complex vector, yt, of length N.  yt is then used to obtain the N/2 Fourier Series
coefficients.  The first element of yt, yt[0], is used to obtain the zero frequency
Fourier Series Coefficient, a0, which is equal to 2*yt[0]/N.  The first and second
halves of the remaining elements of yt are complex conjugates of one another.  In
other words yt[1:N/2+1] and yt[N/2+1:] are complex conjugates.  As such, the remaining
Fourier Series Coefficients are obtained from yt[1:N/2+1]. Letting c = 2*yt[:N/2+1]/N,
the nth element of c, cn, is then equal to an - bn*i.  Inserting a0, an, and bn
into the expression for s(x) shown above will then yield the Fourier Series approximation
for any x* value such that xa <= x* <= xb.

#### Fourier Series Padding
#### Eliminating Noise Using Fourier Analysis

## Fourier Series Fundamentals

## Fourier Series from the Discrete Fourier Transform

## Fourier Series Padding

## Eliminating Noise Using Fourier Analysis
