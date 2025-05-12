import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

import pandas as pd
import os
import math

plt.rcParams['savefig.dpi'] = 600
plt.rcParams["font.sans-serif"] = ["Taipei Sans TC Beta"]

# Settings
#############################################################################
sex = 0 # 0: men, 1: women

isPoseMode = False # if true, the origin point is pose, otherwise origin point is ground point
playerRealHeight = [[1.8, 1.76, 1.84],  # 男甲
                    [1.77, 1.68, 1.78], # 男乙
                    [1.72, 1.74, 1.61], # 女甲
                    [1.55, 1.60, 1.58]] # 女乙
# Unit: meter (m)

people_amount_in_group = 3 # how many people in group

startBall, ballAmount_get = 30, 20 # how many ball amount want to get
# if don't limit amount, setting to -1 (or any negative number)

lang = 1 # language, 0: TW, 1: EN

videoW, videoH = 1920, 1080
#############################################################################

file_path = [[[f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男甲\正拍_男甲1-1",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男甲\正拍_男甲1-2",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男甲\正拍_男甲1-3"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男甲\正拍_男甲2-1",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男甲\正拍_男甲2-2",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男甲\正拍_男甲2-3"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男甲\正拍_男甲3-1",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男甲\正拍_男甲3-2",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男甲\正拍_男甲3-3"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男甲\反拍_男甲1-1",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男甲\反拍_男甲1-2",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男甲\反拍_男甲1-3"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男甲\反拍_男甲2-1",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男甲\反拍_男甲2-2",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男甲\反拍_男甲2-3"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男甲\反拍_男甲3-1",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男甲\反拍_男甲3-2",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男甲\反拍_男甲3-3"]],
             [[f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男乙\正拍_男乙1-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男乙\正拍_男乙1-2",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男乙\正拍_男乙1-3"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男乙\正拍_男乙2-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男乙\正拍_男乙2-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男乙\正拍_男乙3-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\男乙\正拍_男乙3-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男乙\反拍_男乙1-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男乙\反拍_男乙1-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男乙\反拍_男乙2-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男乙\反拍_男乙2-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男乙\反拍_男乙3-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\男乙\反拍_男乙3-2"]],
             [[f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\女甲\正拍_女甲1-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\女甲\正拍_女甲1-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\女甲\正拍_女甲2-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\女甲\正拍_女甲2-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\女甲\正拍_女甲3-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\女甲\正拍_女甲3-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\女甲\反拍_女甲1-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\女甲\反拍_女甲1-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\女甲\反拍_女甲2-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\女甲\反拍_女甲2-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\女甲\反拍_女甲3-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\女甲\反拍_女甲3-2"]],
             [[f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\女乙\正拍_女乙1-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\女乙\正拍_女乙1-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\女乙\正拍_女乙2-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\女乙\正拍_女乙2-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\女乙\正拍_女乙3-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\正拍\女乙\正拍_女乙3-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\女乙\反拍_女乙1-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\女乙\反拍_女乙1-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\女乙\反拍_女乙2-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\女乙\反拍_女乙2-2"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\女乙\反拍_女乙3-1",
             f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材\球員分析\反拍\女乙\反拍_女乙3-2"]]]

method = [0, 1] # 0: 正拍, 1:反拍

# whether show vertical box plot. if True, show horizontal
isVert = True

boxplot_title = ""

match lang:
    case 0: # TW
        legend_labels = ["正拍", "反拍"]
        labels_name = ["男甲", "男乙", "女甲", "女乙"]
    case 1: # EN
        legend_labels = ["Forehand", "Backhand"]
        labels_name = ["Men Group A", "Men Group B", "Women Group A", "Women Group B"]

# figure x-y scale
xscale, yscale = 0.5, 0.25
xlim, ylim = 8, 2

# IMPOSSIBLE to convert pixel to distance using single camera, it must have number error.
# so here use averaging to estimate real world.
# 第2次素材（室外場地）
# 1 pixel ~= 0.0132 m (5.5m / 417 pixel, 使用最遠離鏡頭的雙人場地邊線換算)
# 1 pixel ~= 0.0126 m (5.5m / 436 pixel, 使用最遠離鏡頭的單人場地邊線換算)
# 1 pixel ~= 0.0086 m (5.5m / 642 pixel, 使用中線換算)
# 1 pixel ~= 0.0040 m (5.5m / 1371 pixel, 使用最靠近鏡頭的單人場地邊線換算)
# 1 pixel ~= 0.0025 m (5.5m / 2244 pixel, 使用最靠近鏡頭的雙人場地邊線換算)
#pixel2real = (0.0132 + 0.0126 + 0.0086 + 0.0040 + 0.0025) / 5
# 第3次素材（室內場地）
# 1 pixel ~= 0.01425 m (5.5m / 386 pixel, 使用最遠離鏡頭的雙人場地邊線換算)
# 1 pixel ~= 0.01285 m (5.5m / 428 pixel, 使用最遠離鏡頭的單人場地邊線換算)
# 1 pixel ~= 0.00835 m (5.5m / 659 pixel, 使用中線換算)
# 1 pixel ~= 0.00418 m (5.5m / 1316 pixel, 使用最靠近鏡頭的單人場地邊線換算)
# 1 pixel ~= 0.00286 m (5.5m / 1920 pixel, 使用最靠近鏡頭的雙人場地邊線換算)
# Maybe the camera distance is wrong, I don't know why the height transform is wrong. (real height is too high)
# So height changing to refer player height to transfer
pixel2real_w = (0.00835 * 0.2 + 0.00418 * 0.55 + 0.00286 * 0.25) # distance changing to refer origin method, but only using half fleid and add weight reference
playerPixelH = [[273, 290, 281, 238, 271, 282], # 男甲
                [301, 312, 290, 251, 231, 238], # 男乙
                [251, 261, 201, 221, 261, 192], # 女甲
                [186, 207, 193, 196, 203, 197]] # 女乙
pixel2real_h = [[0, 0, 0, 0, 0, 0], # 男甲
                [0, 0, 0, 0, 0, 0], # 男乙
                [0, 0, 0, 0, 0, 0], # 女甲
                [0, 0, 0, 0, 0, 0]] # 女乙
for i in range(4):
    for j in range(6):
        pixel2real_h[i][j] = (playerRealHeight[i][j % 3] - 0.1) / playerPixelH[i][j]

def NormalizeCoord(g_list, h_list, k_list, t):
    for i in range(len(g_list)):
        g_list[i] = (g_list[i][0], abs(g_list[i][1] - videoH))
        h_list[i] = (h_list[i][0], abs(h_list[i][1] - videoH))
        k_list[i] = (k_list[i][0], abs(k_list[i][1] - videoH))

    if method[t] == 0:
        for i in range(len(g_list)):
            h_list[i] = (h_list[i][0] - g_list[i][0], h_list[i][1] - g_list[i][1])
            k_list[i] = (k_list[i][0] - g_list[i][0], k_list[i][1] - g_list[i][1])
            g_list[i] = (0, 0)
    else:
        for i in range(len(g_list)):
            h_list[i] = (h_list[i][0] - g_list[i][0], h_list[i][1] - g_list[i][1])
            k_list[i] = (k_list[i][0] - g_list[i][0], k_list[i][1] - g_list[i][1])
            g_list[i] = (0, 0)

    return g_list, h_list, k_list

def GetDist(p1, p2):
    distance = math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2)
    distance = math.sqrt(distance)
    return distance

ground_list, highest_list, hit_list = [], [], []
disturbed_balls = []

people_count = 0
for groups_file in file_path:
    for files in groups_file:
        ground_list.append([]); highest_list.append([]); hit_list.append([])
        disturbed_balls.append([])
        for f in files:
            file_name = f.split("\\")[-1]
            print("File:", file_name)
            # reading from a existing csv
            if os.path.exists(f + "/" + file_name + ".csv"):
                data = pd.read_csv(f + "/" + file_name + ".csv")
                # print(data[["Index", "Time"
                #            , "StartFrame", "EndFrame"
                #            , "GroundPoint", "HightestPoint", "HitPoint"
                #            , "IsDistrubed"]].to_string(index=False))

                for ground_point in data["GroundPoint"]:
                    point = ground_point.replace("(", "").replace(")", "").split(",")
                    ground_list[people_count].append((int(point[0]), int(point[1])))

                for highest_point in data["HightestPoint"]:
                    point = highest_point.replace("(", "").replace(")", "").split(",")
                    highest_list[people_count].append((int(point[0]), int(point[1])))

                for hit_point in data["HitPoint"]:
                    point = hit_point.replace("(", "").replace(")", "").split(",")
                    hit_list[people_count].append((int(point[0]), int(point[1])))

                for is_disturbed in data["IsDistrubed"]:
                    if is_disturbed: disturbed_balls[people_count].append(True)
                    else: disturbed_balls[people_count].append(False)
        people_count += 1

new_hit_list_x, new_hit_list_y = [], []
new_highest_list = []

for i in range(people_count):
    ground_list[i], highest_list[i], hit_list[i] = NormalizeCoord(ground_list[i], highest_list[i], hit_list[i], i % 2)

    if i % people_amount_in_group  == 0:
        new_hit_list_x.append([])
        new_hit_list_y.append([])
        new_highest_list.append([])

    people_ball_count = 0
    for j in range(len(ground_list[i])):
        if people_ball_count < startBall + ballAmount_get or ballAmount_get < 0:
            # convert pixel to real world distance
            hit_list[i][j] = (hit_list[i][j][0] * pixel2real_w, hit_list[i][j][1] * pixel2real_h[i // 6][i % 6])
            highest_list[i][j] = (highest_list[i][j][0] * pixel2real_w, highest_list[i][j][1] * pixel2real_h[i // 6][i % 6])

            # let some omit unreasonable label to distrubed
            if hit_list[i][j][1] < ground_list[i][j][1] or hit_list[i][j][1] > highest_list[i][j][1]:
                disturbed_balls[i][j] = True

            if not disturbed_balls[i][j]:
                new_hit_list_x[-1].append(abs(hit_list[i][j][0]))
                new_hit_list_y[-1].append(abs(hit_list[i][j][1]))
                new_highest_list[-1].append((abs(highest_list[i][j][0]), abs(highest_list[i][j][1])))
                people_ball_count += 1
        
        if people_ball_count == startBall:
            new_hit_list_x[-1], new_hit_list_y[-1], new_highest_list[-1] = [], [], []

plt.figure(figsize=(12, 6))
ax = plt.gca()

if isVert:
    plt.grid(axis="y", ls="--", alpha=0.8)
    y_major_locator = MultipleLocator(yscale)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.ylim(0, ylim)
    plt.ylabel("Height (m)")
    new_hit_list = new_hit_list_y
else:
    plt.grid(axis="x", ls="--", alpha=0.8)
    x_major_locator = MultipleLocator(xscale)
    ax.xaxis.set_major_locator(x_major_locator)
    plt.xlim(0, xlim)
    plt.xlabel("Distance (m)")
    new_hit_list = new_hit_list_x

# calculate highest and hit's distance
dist_list = []
for j, new_list in enumerate(new_hit_list):
    dist_list.append([])
    for i in range(len(new_list)):
        d = GetDist((new_hit_list_x[j][i], new_hit_list_y[j][i]), new_highest_list[j][i])
        dist_list[-1].append(d)

box = [[], []]
# box[0] = [dist_list[0], dist_list[2], dist_list[4], dist_list[6]] # 正拍
# box[1] = [dist_list[1], dist_list[3], dist_list[5], dist_list[7]] # 反拍
box[0] = [new_hit_list[0], new_hit_list[2], new_hit_list[4], new_hit_list[6]] # 正拍
box[1] = [new_hit_list[1], new_hit_list[3], new_hit_list[5], new_hit_list[7]] # 反拍

# 甲組 / 正拍
box1 = plt.boxplot(box[0], positions=[1, 2.5, 4, 5.5], widths=0.2, 
                   patch_artist=True, vert=isVert, showfliers=False, showmeans=True, whis=[0, 100], 
                   boxprops={"facecolor": "lightcoral",
                             "edgecolor": "grey",
                             "linewidth": 1},
                   medianprops={"color": "k", "linewidth": 1.5},
                   meanprops={"marker":"o", 
                              "markerfacecolor" : "w",
                              "markeredgecolor" : "k",
                              "markersize" : 5} )

# 乙組 / 反拍
box2 = plt.boxplot(box[1] , positions=[1.5, 3, 4.5, 6], widths=0.2,
                   patch_artist=True, vert=isVert, showfliers=False, showmeans=True, whis=[0, 100],
                   boxprops={"facecolor": "lightblue",
                             "edgecolor": "grey",
                             "linewidth": 1},
                   medianprops={"color": "k", "linewidth": 1.5},
                   meanprops={"marker":"o",
                              "markerfacecolor" : "w",
                              "markeredgecolor" : "k", 
                              "markersize" : 5} )

# show values
for i in range(len(new_hit_list)):
    if i % 2 == 0: # box1
        medians = [median.get_ydata() for median in box1["medians"]]
        whiskers = [whiskers.get_ydata() for whiskers in box1["whiskers"]]
        means = [means.get_ydata() for means in box1["means"]]
        print("Medians: ", medians)
        print("Whiskers: ", whiskers)
        print("Mean: ", means)

        # 男甲
        plt.annotate(format(whiskers[0][1], ".3f"), xy=(1-0.35, whiskers[0][1])) # min
        plt.annotate(format(whiskers[1][1], ".3f"), xy=(1-0.35, whiskers[1][1])) # max
        plt.annotate(format(whiskers[0][0], ".3f"), xy=(1-0.35, whiskers[0][0])) # q1
        plt.annotate(format(whiskers[1][0], ".3f"), xy=(1-0.35, whiskers[1][0])) # q3
        plt.annotate(format(medians[0][0], ".3f"), xy=(1-0.35, medians[0][0])) # median
        plt.annotate("Mean = " + format(means[0][0], ".3f"), xy=(1-0.35, whiskers[1][1]+0.1)) # means

        # 男乙
        plt.annotate(format(whiskers[2][1], ".3f"), xy=(2.5-0.35, whiskers[2][1])) # min
        plt.annotate(format(whiskers[3][1], ".3f"), xy=(2.5-0.35, whiskers[3][1])) # max
        plt.annotate(format(whiskers[2][0], ".3f"), xy=(2.5-0.35, whiskers[2][0])) # q1
        plt.annotate(format(whiskers[3][0], ".3f"), xy=(2.5-0.35, whiskers[3][0])) # q3
        plt.annotate(format(medians[1][0], ".3f"), xy=(2.5-0.35, medians[1][0])) # median
        plt.annotate("Mean = " + format(means[1][0], ".3f"), xy=(2.5-0.35, whiskers[3][1]+0.1)) # means

        # 女甲
        plt.annotate(format(whiskers[4][1], ".3f"), xy=(4-0.35, whiskers[4][1])) # min
        plt.annotate(format(whiskers[5][1], ".3f"), xy=(4-0.35, whiskers[5][1])) # max
        plt.annotate(format(whiskers[4][0], ".3f"), xy=(4-0.35, whiskers[4][0])) # q1
        plt.annotate(format(whiskers[5][0], ".3f"), xy=(4-0.35, whiskers[5][0])) # q3
        plt.annotate(format(medians[2][0], ".3f"), xy=(4-0.35, medians[2][0])) # median
        plt.annotate("Mean = " + format(means[2][0], ".3f"), xy=(4-0.35, whiskers[5][1]+0.1)) # means

        # 女乙
        plt.annotate(format(whiskers[6][1], ".3f"), xy=(5.5-0.35, whiskers[6][1])) # min
        plt.annotate(format(whiskers[7][1], ".3f"), xy=(5.5-0.35, whiskers[7][1])) # max
        plt.annotate(format(whiskers[6][0], ".3f"), xy=(5.5-0.35, whiskers[6][0])) # q1
        plt.annotate(format(whiskers[7][0], ".3f"), xy=(5.5-0.35, whiskers[7][0])) # q3
        plt.annotate(format(medians[3][0], ".3f"), xy=(5.5-0.35, medians[3][0])) # median
        plt.annotate("Mean = " + format(means[3][0], ".3f"), xy=(5.5-0.35, whiskers[7][1]+0.1)) # means

    else: # box2
        medians = [median.get_ydata() for median in box2["medians"]]
        whiskers = [whiskers.get_ydata() for whiskers in box2["whiskers"]]
        means = [means.get_ydata() for means in box2["means"]]
        print("Medians: ", medians)
        print("Whiskers: ", whiskers)
        print("Mean: ", means)

        # 男甲
        plt.annotate(format(whiskers[0][1], ".3f"), xy=(1.5+0.15, whiskers[0][1])) # min
        plt.annotate(format(whiskers[1][1], ".3f"), xy=(1.5+0.15, whiskers[1][1])) # max
        plt.annotate(format(whiskers[0][0], ".3f"), xy=(1.5+0.15, whiskers[0][0])) # q1
        plt.annotate(format(whiskers[1][0], ".3f"), xy=(1.5+0.15, whiskers[1][0])) # q3
        plt.annotate(format(medians[0][0], ".3f"), xy=(1.5+0.15, medians[0][0])) # median
        plt.annotate("Mean = " + format(means[0][0], ".3f"), xy=(1.5-0.1, whiskers[1][1]+0.1)) # means

        # 男乙
        plt.annotate(format(whiskers[2][1], ".3f"), xy=(3+0.15, whiskers[2][1])) # min
        plt.annotate(format(whiskers[3][1], ".3f"), xy=(3+0.15, whiskers[3][1])) # max
        plt.annotate(format(whiskers[2][0], ".3f"), xy=(3+0.15, whiskers[2][0])) # q1
        plt.annotate(format(whiskers[3][0], ".3f"), xy=(3+0.15, whiskers[3][0])) # q3
        plt.annotate(format(medians[1][0], ".3f"), xy=(3+0.15, medians[1][0])) # median
        plt.annotate("Mean = " + format(means[1][0], ".3f"), xy=(3-0.1, whiskers[3][1]+0.1)) # means

        # 女甲
        plt.annotate(format(whiskers[4][1], ".3f"), xy=(4.5+0.15, whiskers[4][1])) # min
        plt.annotate(format(whiskers[5][1], ".3f"), xy=(4.5+0.15, whiskers[5][1])) # max
        plt.annotate(format(whiskers[4][0], ".3f"), xy=(4.5+0.15, whiskers[4][0])) # q1
        plt.annotate(format(whiskers[5][0], ".3f"), xy=(4.5+0.15, whiskers[5][0])) # q3
        plt.annotate(format(medians[2][0], ".3f"), xy=(4.5+0.15, medians[2][0])) # median
        plt.annotate("Mean = " + format(means[2][0], ".3f"), xy=(4.5-0.1, whiskers[5][1]+0.1)) # means

        # 女乙
        plt.annotate(format(whiskers[6][1], ".3f"), xy=(6+0.15, whiskers[6][1])) # min
        plt.annotate(format(whiskers[7][1], ".3f"), xy=(6+0.15, whiskers[7][1])) # max
        plt.annotate(format(whiskers[6][0], ".3f"), xy=(6+0.15, whiskers[6][0])) # q1
        plt.annotate(format(whiskers[7][0], ".3f"), xy=(6+0.15, whiskers[7][0])) # q3
        plt.annotate(format(medians[3][0], ".3f"), xy=(6+0.15, medians[3][0])) # median
        plt.annotate("Mean = " + format(means[3][0], ".3f"), xy=(6-0.1, whiskers[7][1]+0.1)) # means

if isVert:  plt.xticks([1.3, 2.8, 4.3, 5.8], fontsize=12, labels=labels_name)
else:       plt.yticks([1.3, 2.8, 4.3, 5.8], fontsize=12, labels=labels_name)

plt.legend(handles=[box1["boxes"][0], box2["boxes"][0]], bbox_to_anchor=(1.01, 0), loc="lower left", labels=legend_labels)
plt.title(boxplot_title, fontsize=16)
plt.tight_layout()
plt.show()