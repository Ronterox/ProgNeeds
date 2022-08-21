import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np

FPS = 15
NUMBERS = 10

np.random.seed(123)
y = np.random.randint(0, 1000, size=(NUMBERS,))
x = np.array([i for i in range(y.size)])

fig = plt.figure(figsize=(y.size, y.size))
bars = plt.bar(x, y)


def update(sort_step):
    for rect, height in zip(bars, sort_step):
        rect.set_height(height)
    print(sort_step)


def create_anim(sortmethod):
    sort = np.array(list(sortmethod(y.copy())))
    print("Sort's done")

    animation = anim.FuncAnimation(fig, update, frames=sort, repeat=False)
    animation.save(f'{sortmethod.__name__}.mp4', writer=anim.FFMpegWriter(fps=FPS))


# O(n^2), O(n) sometimes if break
def sort_bubble(y) -> object:
    yield y.copy()
    for i in range(y.size):
        swapped = True
        for j in range(y.size - 1):
            if y[j] > y[j + 1]:
                y[j], y[j + 1] = y[j + 1], y[j]
                swapped = False
                yield np.copy(y)

        if swapped: break


# O(n^1.5)
def sort_selection(y) -> object:
    yield y.copy()
    for i in range(y.size):
        minval = i
        for j in range(i + 1, y.size):
            if y[j] < y[minval]: minval = j
        y[i], y[minval] = y[minval], y[i]
        yield np.copy(y)


# O(n^1.25)
def sort_insertion(y) -> object:
    yield y.copy()
    for i in range(y.size - 1):
        if y[i] > y[i + 1]:
            y[i], y[i + 1] = y[i + 1], y[i]
            while i > 0 and y[i] < y[i - 1]:
                y[i], y[i - 1] = y[i - 1], y[i]
                i -= 1
            yield y.copy()


create_anim(sort_bubble)
create_anim(sort_selection)
create_anim(sort_insertion)
