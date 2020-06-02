import matplotlib.pyplot as plt

class BasicAlgoHelper:
    def __init__(self):
        plt.ion() # interactive mode
        self.best_scores = []
        self.fig = plt.figure()
        self.axis = self.fig.add_subplot(211)
        self.axis.plot([0], [0])
        self.fig.canvas.draw()

    def update(self, val):
        self.best_scores.append(val)
        self.axis.clear()
        x = list(range(len(self.best_scores)))
        self.axis.plot(x, self.best_scores)
        self.fig.canvas.draw()
