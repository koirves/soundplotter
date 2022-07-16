import math
from re import S
from typing import List

class complex:

    r: float
    i: float

    def __init__(self, real: float, imaginary: float):
        
        self.r = real
        self.i = imaginary
    

    def magnitude(self) -> float:

        value = math.sqrt(self.r * self.r + self.i * self.i)

        return value

    

    def add(self, other: complex) -> complex:

        value = complex(self.r + other.r, self.i + other.i)

        return value

    

    def sub(self, other) -> complex:

        value = complex(self.r - other.r, self.i - other.i)

        return value

    

    def multiplicate(self, other) -> complex:

        value = complex(self. r * other.r - self.i * other.i, self.r * other.r + self.i * other.r)

        return value

    

    def divide(self, other: complex) -> complex:

        ac = (self.r * other.r)
        bd = (self.i * other.i)
        bc = (self.i * other.r)
        ad = (self.r * other.i)
        cc = (other.r * other.r)
        dd = (other.i * other.i)

        r = (ac + bd) / (cc + dd)
        i = (bc - ad) / (cc + dd)

        value = complex(r , i)

        return value

    

    def scale(self, scalar: float) -> complex:
        
        value = complex(scalar * self.r, scalar * self.i)

        return value
    

    def exp(self) -> complex:

        value = complex(math.exp(self.r) * math.cos(self.i), math.exp(self.r) * math.sin(self.i))

        return value
    

    def log(self) -> complex:


        value = complex(math.log(self.magnitude()), math.atan2(self.i, self.r))

        return value


class fourier:
    
    sf: float

    def __init__(self, sampling_frequency = 44100):
        
        self.sf = sampling_frequency

    def dft(self, complexSet: List[complex]) -> complex:

        """
        Note Nyquist limit sampling freq / 2: Impossible to analyze frequences above that
        """

        #Descreet Fourier Transform
        #X_k = sum(n=0 -> N-1) x_n * e^((-i*2*pi*k*n) / N)

        cDFT: List[complex] = []

        N = len(complexSet)

        for k, _ in enumerate(complexSet):

            X_k = complex(0, 0)

            for n, x_n in enumerate(complexSet):

                #Using Euler's formula
                r = math.cos(((2*math.pi)/N)*k*n)
                i = math.sin(((2*math.pi)/N)*k*n)
                X_k = X_k.add(complex(r, -i).multiplicate(x_n))

            
            print(k, X_k.r, X_k.i, X_k.magnitude())

            cDFT.append(X_k)

        ## Processing

        nyquistLimit = self.sf / 2
        sampleFreq = self.sf / N
        sampleN = int(nyquistLimit / sampleFreq)
        sFactor = N / sampleN
        print(f"Nyqist limit: {nyquistLimit}, sample frequency: {sampleFreq}, analyzing first {sampleN} samples. Using scale factor {sFactor}")
        samples: List[complex] = []

        for sample in cDFT[:sampleN]:
            samples.append(sample.scale(sFactor))

        print(samples)