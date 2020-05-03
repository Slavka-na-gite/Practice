import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

class QRS():
    def __init__(self,signal):
        self.signal = signal

    def diff(A, i):
        dif = 0
        for k in range(-3, 4):
            if k < 0:
                dif = dif - A[i + k]
            elif k > 0:
                dif = dif + A[i + k]
            else:
                continue
        return abs(dif)

    def maximum(y):
        Y1 = list()
        Y = list()
        for i in range(0, len(y) - 9):
            if i <= 8:
                Y1.append(y[i])
                Y.append(max(Y1))
            else:
                z = list()
                for k in range(-9, 9):
                    z.append(y[k + i])
                Y.append(max(z))
        return Y

    def QRS1(Y,A,a):
        k = 0
        l = -1
        amplitude1 = []
        for i in range(0, len(Y)):
            if Y[i] > A[i] + a:
                if k == 0:
                    l += 1
                    amplitude1.append([])
                k += 1
                amplitude1[l].append(i)
            else:
                k = 0
                continue
        return amplitude1
    def matrix(self):
        signal = 216000  # 10 минут сигнала
        amplitude = np.array(self)
        f = range(0, signal)
        y = []
        for i in range(0, signal - 3):
            if i <= 2:
                y.append(f[i])
            else:
                y.append(QRS.diff(amplitude, i))

        Y = QRS.maximum(y)  # Максимум производной в интервале 0,1с

        k1, k2 = scipy.signal.butter(2, 0.2 * 2 / 360, btype='low')  # Нахожу изолинию
        A = scipy.signal.filtfilt(k1, k2, Y)

        N = 5400
        a = 0.05 * (Y[0] / 2) * (N - 1) / N  # Порог
        for i in range(1, len(Y)):
            a = 0.95 * a + 0.05 * (Y[i] / 2)
            a = a * (N - 1) / N
        a *=2
        amplitude1 = QRS.QRS1(Y,A,a)  # матрица с номером QRS комплекса и индексы его семплов в оригинальном сигнале

        return amplitude1


    def plot(self,index):
        A = QRS.matrix(self)[index]
        amplitude = np.array(self)
        plt.rcParams["figure.figsize"] = (1,4)
        plt.plot(amplitude[A[0]:A[len(A)-1]])
        plt.show()


    def norma(self):
        A = QRS.matrix(self)
        amplitude = np.array(self)
        for i in range(0,len(A)):
            if len(A[i]) > 50:
                plt.rcParams["figure.figsize"] = (1, 4)
                plt.plot(amplitude[A[i][0]:A[i][len(A[i]) - 1]])
                plt.show()
                print(round(A[i][0]/360,1))
            elif len(A[i]) < 21:
                plt.rcParams["figure.figsize"] = (1, 4)
                plt.plot(amplitude[A[i][0]-10:A[i][len(A[i]) - 1]]+10)
                plt.show()
                print(round(A[i][0] / 360, 1))


