import numpy as np
import json
from matplotlib import pyplot as plt
from matplotlib import animation
import skeleton
import argparse
import os
# one more thing: concentrate on the single people!
# sometimes there will be more than one people in the video



def read(path):
    file_list = []
    res = []
    for filename in os.listdir(path):
        if filename.endswith("keypoints.json"):
            file_list.append(filename)
    file_list.sort()

    for filename in file_list:
        with open(os.path.join(path, filename), 'r') as f:
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
        y = [height - points[i][1] for i in range(len(points))]
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
    fig, ax = plt.subplots()
    x, y = get_xy(0)
    plot, = ax.plot(x, y, 'o-')
    plt.xlim([0, width])
    plt.ylim([0, height])
    ani = animation.FuncAnimation(fig=fig,
                                  func=animate,
                                  frames=matrix.shape[0],
                                  init_func=init,
                                  interval=20,
                                  blit=False)
    plt.show()



def construct_skeleton_list(path, smooth_factor, skip_factor=1):
    list_of_json = read(path)
    list_of_keypoints = np.array(list(map(get_keypoints, list_of_json)))
    smoothed = np.apply_along_axis(smooth_by, 0, list_of_keypoints, smooth_factor)
    skeleton_list = skeleton.create_skeleton_list(smoothed[::skip_factor])
    return skeleton_list


def main(path, smooth_factor):
    list_of_json = read(path)
    list_of_keypoints = np.array(list(map(get_keypoints, list_of_json)))
    smoothed = np.apply_along_axis(smooth_by, 0, list_of_keypoints, smooth_factor)
    render_to_video(smoothed[::skip_factor])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str,
                        help='the dir of the json files')
    parser.add_argument('-s', '--smooth', type=int, default=1,
                        help="smooth factor")
    parser.add_argument('--skip', type=int, default=1,
                        help="skip factor")
    parser.add_argument("--height", type=int, default=1000,
                        help="height of video")
    parser.add_argument("--width", type=int, default=1000,
                        help="width of video")

    args = parser.parse_args()
    path = args.filepath
    smooth_factor = args.smooth
    height, width = args.height, args.width
    skip_factor = args.skip

    main(path, smooth_factor)
    #l = construct_skeleton_list(path, smooth_factor)
    #print(l[0])

