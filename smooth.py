import numpy as np
import json
import functools
from matplotlib import pyplot as plt
from matplotlib import animation
import skeleton


# one more thing: concentrate on the single people!
# sometimes there will be more than one people in the video
filename_base = './output_3/new_00000000{:0>4d}_keypoints.json'

def read():
    res = []
    for i in range(279):
        filename = filename_base.format(i)
        with open(filename, 'r') as f:
            res.append(json.load(f))
    return res


def get_keypoints(dct):
    try:
        l = dct['people'][0]  # assume only one person here
        l = l['pose_keypoints_2d']
    except:
        print("warning: no person")
        l = [0] * 54
    assert len(l) % 3 == 0
    res = []
    for i in range(len(l) // 3):
        res.append(tuple(l[3*i:3*i+3]))
    return np.array(res)


def smooth_by(lst, n, weight=None):
    # it will decrease the total length
    # how to deal with point that not in the graph
    res = []
    if not weight:
        weight = np.ones(n)
    for i in range(len(lst) - n + 1):
        num = sum(lst[i:i+n] * weight) / n
        res.append(num)
    assert len(res) == len(lst) - n + 1
    return res


def to_skeleton(points):
    mask = [0, 1, 2, 3, 4,
     3, 2, 1,
     5, 6, 7,
     6, 5, 1,
     8, 9, 10,
     9, 8, 1,
     11, 12, 13]
    return points[mask]


def render_to_video(matrix):
    def get_xy(frame):
        points = matrix[frame]
        points = to_skeleton(points)
        x = [points[i][0] for i in range(len(points))]
        y = [680 - points[i][1] for i in range(len(points))]
        return x, y

    def animate(i):
        x, y = get_xy(i)
        plot.set_xdata(x)
        plot.set_ydata(y)
        return plot

    def init():
        animate(0)
        return plot

    print(matrix.shape)
    print(matrix)
    fig, ax = plt.subplots()
    x, y = get_xy(0)
    plot, = ax.plot(x, y, 'o-')
    plt.xlim([0, 1208])
    plt.ylim([0, 679])
    ani = animation.FuncAnimation(fig=fig,
                                  func=animate,
                                  frames=1000,
                                  init_func=init,
                                  interval=20,
                                  blit=False)
    plt.show()



def construct_skeleton_list(smooth_factor):
    list_of_json = read()
    list_of_keypoints = np.array(list(map(get_keypoints, list_of_json)))
    smoothed = np.apply_along_axis(smooth_by, 0, list_of_keypoints, smooth_factor)
    skeleton_list = skeleton.create_skeleton_list(smoothed)
    return skeleton_list


def main(smooth_factor):
    list_of_json = read()
    list_of_keypoints = np.array(list(map(get_keypoints, list_of_json)))
    smoothed = np.apply_along_axis(smooth_by, 0, list_of_keypoints, smooth_factor)
    render_to_video(smoothed)

if __name__ == "__main__":
    #main(3)
    l = construct_skeleton_list(1)
    print(l[0])

