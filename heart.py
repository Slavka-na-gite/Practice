import numpy as np
import scipy.io as sc
import scipy.signal
import matplotlib.pyplot as plt


def plot(A, a, b):
    plt.subplot(611)
    plt.plot(A[a:b])
    vectorW = [2, 3, 4, 5.5, 10]# по спектру выделил места с гармониками, по которым фильтровать
    for i in range(0,len(vectorW)):
        k = i+2
        plt.subplot(6,1,k)
        k1,k2 = scipy.signal.butter(8,vectorW[i]*2/360, btype='low')
        plt.plot(scipy.signal.filtfilt(k1,k2,A[a:b]))
    return plt.show()


def dft_map(X, Fs):
    resolution = Fs / len(X)
    Y = X
    n = np.arange(0, len(Y))
    f = n * resolution
    return f, Y


file = sc.loadmat("100mq.mat")
amplitude1 = np.array(file['val'][0])

X = np.fft.fft(amplitude1[0:1800])
Y = np.fft.fft(amplitude1[503000:504800])#участок сигнала с искажением
f,l = dft_map(Y, 360)
f,k = dft_map(X, 360)

plt.rcParams["figure.figsize"] = (14,5)
plt.figure(1)
plt.plot(f,abs(k/len(f)),f,abs(l/len(f)))#уширение спектра и увеличение квадрата амплитуда PQRST комплекса
plt.axis([0,20,0,15])
plt.show()
plt.rcParams["figure.figsize"] = (14,8)
plt.figure(2)
plot(amplitude1,0,3600)#По очереди фильтрую первые пять пиков, для определения точек PQRST комплекса
#Есь идея сглаживать определенные участки сигнала и смотреть какие пики исчезли(так должно быть точнее)
#Буду еще придумывать и пытаться реализовать идеи по нахождению других видов искажений
#Нашел минус - код не гибкий, буду исправлять
