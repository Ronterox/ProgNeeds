import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np

FPS = 15
ELEMENTS = 20

np.random.seed(123)
y = np.random.randint(0, 1000, size=(ELEMENTS,))
x = np.array([i for i in range(y.size)])

fig = plt.figure(figsize=(y.size, y.size))
bars = plt.bar(x, y)
step = 0


def update(sort_step):
    global step
    for rect, height in zip(bars, sort_step):
        rect.set_height(height)
    print(f'Step {step}: {sort_step}')
    step += 1


def create_anim(sortmethod):
    global step

    sort = np.array(list(sortmethod(y.copy())))
    print(f"\nSort {sortmethod.__name__} is done")

    step = 0

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


# O(n^1.40)
def sort_insertion(y) -> object:
    yield y.copy()
    for i in range(y.size - 1):
        if y[i] > y[i + 1]:
            y[i], y[i + 1] = y[i + 1], y[i]
            j = i
            while j > 0 and y[j] < y[j - 1]:
                y[j], y[j - 1] = y[j - 1], y[j]
                j -= 1
            yield y.copy()


def quick_sort(y, low, high):
    if low < high:
        i = low
        for j in range(low, high):
            if y[j] <= y[high]:
                y[j], y[i] = y[i], y[j]
                i += 1
                yield y.copy()
        y[high], y[i] = y[i], y[high]

        for j in quick_sort(y, low, i - 1): yield j

        for j in quick_sort(y, i + 1, high): yield j


# Worst O(n^2) best O(nLog(n))
def sort_quick(y) -> object:
    yield y.copy()
    for i in quick_sort(y, 0, y.size - 1): yield i
    yield y.copy()


# O(nlog(n))
def sort_merge(y) -> object:
    if len(y) < 2: return
    yield y.copy()

    mid = len(y) // 2
    left, right = y[:mid].copy(), y[mid:].copy()

    for i in sort_merge(left):
        if len(i) == len(y):
            yield i
            break

    for i in sort_merge(right):
        if len(i) == len(y):
            yield i
            break

    i = j = k = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            y[k] = left[i]
            i += 1
        else:
            y[k] = right[j]
            j += 1
        k += 1
        yield y.copy()

    while i < len(left):
        y[k] = left[i]
        i += 1
        k += 1
        yield y.copy()

    while j < len(right):
        y[k] = right[j]
        j += 1
        k += 1
        yield y.copy()


def get_int(max):
    import random
    from time import time

    random.seed(time())
    return random.randint(0, max)


def shuffle_for(y) -> object:
    yield y.copy()
    for i in reversed(range(y.size - 1)):
        j = get_int(i)
        y[i], y[j] = y[j], y[i]
        yield y.copy()


def shuffle_probability(y, val):
    yield y.copy()
    for i in range(y.size):
        j, accumulator = 0, 0
        while accumulator < val:
            accumulator += y[j]
            j = (j + 1) % y.size
        y[i], y[j] = y[j], y[i]
        yield y.copy()


def shuffle_proportional(y) -> object:
    val = get_int((y.size - 1) * (y.sum() - 1))
    return shuffle_probability(y, val)


def shuffle_inv_proportionality(y) -> object:
    val = get_int(y.sum() - 1)
    return shuffle_probability(y, val)


create_anim(sort_bubble)
create_anim(sort_selection)
create_anim(sort_insertion)
create_anim(sort_quick)
create_anim(sort_merge)

create_anim(shuffle_for)
create_anim(shuffle_proportional)
create_anim(shuffle_inv_proportionality)
