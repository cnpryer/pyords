import matplotlib.pyplot as plt
import logging

class BasicKMeansHelper:
    def __init__(self):
        plt.ion() # interactive mode
        self.x1 = []
        self.y1 = []
        self.x2 = []
        self.y2 = []
        self.fig = plt.figure()
        self.axis = self.fig.add_subplot(211)
        x = list(self.x1) + list(self.x2)
        y = list(self.y1) + list(self.y2)
        colors = ['blue']*len(self.x1) + ['red']*len(self.x2)
        self.axis.scatter(x, y, color=colors)
        self.fig.canvas.draw()

    def update(self, x2, y2):
        self.x2 = x2
        self.y2 = y2
        x = list(self.x1) + list(self.x2)
        y = list(self.y1) + list(self.y2)
        colors = ['blue']*len(self.x1) + ['red']*len(self.x2)
        self.axis.clear()
        self.axis.scatter(x, y, color=colors)
        self.fig.canvas.draw()

class BasicDBSCANHelper:
    def __init__(self):
        plt.ion() # interactive mode
        self.x = []
        self.y = []
        self.colors = []
        self.fig = plt.figure()
        self.axis = self.fig.add_subplot(211)
        self.axis.scatter(self.x, self.y)
        self.fig.canvas.draw()

    def update(self, labels):
        self.axis.clear()
        self.axis.scatter(self.x, self.y, c=labels)
        self.fig.canvas.draw()
