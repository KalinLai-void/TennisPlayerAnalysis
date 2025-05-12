import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib.lines import Line2D

import pandas as pd
import os
import math

plt.rcParams['savefig.dpi'] = 600
plt.rcParams["font.sans-serif"] = ["Taipei Sans TC Beta"]

# Settings
#############################################################################
method = 1            # 0: 正拍, 1:反拍
isShowDistrub = False # whether show distrubed ball

isPoseMode = False # if true, the origin point is pose, otherwise origin point is ground point
playerRealHeight = [1.77, 1.68, 1.78] # Unit: meter (m)

isShow2TypeHand = True # 正拍、反拍同時顯示在圖上
isShowNum = False # whether show ball's count
isShowHightest = True # whether show highest ball
isShowNumOnLengend = True # whether show count on lengend

startBall, ballAmount_get = 30, 20 # how many ball amount want to get
# if don't limit amount, setting to -1 (or any negative number)

lang = 1 # language, 0: TW, 1: EN

videoW, videoH = 1920, 1080
#############################################################################

file_path = [[f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\正拍\男乙\正拍_男乙1-1",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\正拍\男乙\正拍_男乙1-2",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\正拍\男乙\正拍_男乙1-3"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\正拍\男乙\正拍_男乙2-1",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\正拍\男乙\正拍_男乙2-2",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\正拍\男乙\正拍_男乙2-3"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\正拍\男乙\正拍_男乙3-1",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\正拍\男乙\正拍_男乙3-2",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\正拍\男乙\正拍_男乙3-3"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\反拍\男乙\反拍_男乙1-1",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\反拍\男乙\反拍_男乙1-2",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\反拍\男乙\反拍_男乙1-3"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\反拍\男乙\反拍_男乙2-1",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\反拍\男乙\反拍_男乙2-2",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\反拍\男乙\反拍_男乙2-3"],
             [f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\反拍\男乙\反拍_男乙3-1",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\反拍\男乙\反拍_男乙3-2",
              f"E:\Project\Capstone Project\Tennins Simulator\網球素材\第3次素材(20230611)\球員分析\反拍\男乙\反拍_男乙3-3"]]

# scatter title
scatter_title  = ""

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
playerPixelH = [301, 312, 290, 251, 231, 238]
pixel2real_h = [0, 0, 0, 0, 0, 0]
for i in range(6):
    pixel2real_h[i] = (playerRealHeight[i % 3] - 0.1) / playerPixelH[i]

# figure x-y scale
xscale, yscale = 0.5, 0.25
xlim, ylim = 6, 2

# language settings
match lang:
    case 0: # TW
        legend_label = ["落地點", "最高點", "擊球點", "擊球點(在最高點擊球)"
                        , "最高點(受干擾)", "擊球點(受干擾)", "擊球點(在最高點擊球)(受干擾)"]
        xlabel = "距離 (公尺)"
        ylabel = "高度 (公尺)"
        subplot_title = ["正拍", "反拍"]
    case 1: # EN
        legend_label = ["Ground", "Highest", "Hit", "Hit (On Highest)"
                        , "Hight (Distrubed)", "Hit (Distrubed)", "Hit (On Highest) (Distrubed)"]
        xlabel = "Distance (m)"
        ylabel = "Height (m)"
        subplot_title = ["Forehand", "Backhand"]

# color settings
if isShowNum:
    point_alpha = 0.8
    ground_facecolor = "#777777" # gray
    hit_on_highest_facecolor = "#009100" # green
    hit_facecolor = "#FF5151" # red
    highest_facecolor = "#2828FF" # blue
    edgecolor = None
else:
    point_alpha = 0.6
    ground_facecolor = "#777777" # gray
    hit_on_highest_facecolor = "#EAC100" # yellow
    hit_facecolor = "#FF359A" # pink
    highest_facecolor = "#2828FF" # blue
    edgecolor = "#000000" # black

def NormalizeCoord(g_list, h_list, k_list):
    for i in range(len(g_list)):
        g_list[i] = (g_list[i][0], abs(g_list[i][1] - videoH))
        h_list[i] = (h_list[i][0], abs(h_list[i][1] - videoH))
        k_list[i] = (k_list[i][0], abs(k_list[i][1] - videoH))

    if method == 0:
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
fin_ground_list, fin_highest_list, fin_hit_list = [], [], []
people_list = []
disturbed_balls = []
fin_disturbed_balls = []

people_count = 0
for files in file_path:
    ground_list.append([]); highest_list.append([]); hit_list.append([])
    disturbed_balls.append([])

    file_name = None
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

    people_list.append(file_name[0:-2])
    people_count += 1

print(people_count)

if isPoseMode:
    pass
else:
    for i in range(people_count):
        ground_list[i], highest_list[i], hit_list[i] = NormalizeCoord(ground_list[i], highest_list[i], hit_list[i])

vaild_normal_ball, vaild_hit_on_height_ball = 0, 0
invaild_normal_ball, invaild_hit_on_height_ball = 0, 0
total_ball = 0

# record hit and highest distance and hit on highest amount [max, min, avg, amount]
dist_hit_highest_table = [[0, 999, 0, 0], [0, 999, 0, 0]]

if not isShow2TypeHand:
    plt.figure(figsize=(12, 6))
else:
    fig, axs = plt.subplots(1, 2, figsize=(20, 6))

for j in range(people_count):

    if isShow2TypeHand:
        if hit_list[j][0][0] < 0:
            ax = axs[0]
        else: ax = axs[1]
    else: ax = plt

    # annotate ground point
    ax.scatter(ground_list[j][0][0], ground_list[j][0][1], s=80, facecolors=ground_facecolor, edgecolors=edgecolor, alpha=1, label=legend_label[0])
    ax.annotate("·", (ground_list[j][0][0], ground_list[j][0][1]), c="#000000", fontsize=6, horizontalalignment="center", verticalalignment="center") 

    people_ball_count = 0
    for i in range(len(ground_list[j])):
        if people_ball_count < startBall + ballAmount_get or ballAmount_get < 0:

            canDraw = False
            if people_ball_count >= startBall:
                canDraw = True

            # convert pixel to real world distance
            hit_list[j][i] = (hit_list[j][i][0] * pixel2real_w, hit_list[j][i][1] * pixel2real_h[j])
            highest_list[j][i] = (highest_list[j][i][0] * pixel2real_w, highest_list[j][i][1] * pixel2real_h[j])

            # ignore some point that vertical coordinate too high and horizontal coordinate too low 
            if abs(hit_list[j][i][0] - highest_list[j][i][0]) <= 0.5 and abs(hit_list[j][i][1] - highest_list[j][i][1]) >= 0.5:
                continue

            if canDraw:
                # let some omit unreasonable label to distrubed
                if hit_list[j][i][1] < ground_list[j][i][1] or hit_list[j][i][1] > highest_list[j][i][1]:
                    disturbed_balls[j][i] = True

                if (highest_list[j][i][0], highest_list[j][i][1]) == (hit_list[j][i][0], hit_list[j][i][1]):
                    # if hit point == highest point
                    hit_color = hit_on_highest_facecolor

                    # annotate hit point (same as highest point)
                    if disturbed_balls[j][i]: 
                        if isShowDistrub:
                            ax.scatter(hit_list[j][i][0], hit_list[j][i][1], s=80, facecolors=edgecolor, edgecolors=hit_color, alpha=1, label=legend_label[6])
                            
                            fin_disturbed_balls.append(disturbed_balls[j][i])
                            fin_ground_list.append(ground_list[j][i])
                            fin_highest_list.append((round(highest_list[j][i][0], 3), round(highest_list[j][i][1], 3)))
                            fin_hit_list.append((round(hit_list[j][i][0], 3), round(hit_list[j][i][1], 3)))

                            if isShowNum:
                                ax.annotate(total_ball + 1, (hit_list[j][i][0], hit_list[j][i][1]), c=hit_color, fontsize=5.5
                                            , horizontalalignment="center", verticalalignment="center")
                                
                        invaild_hit_on_height_ball += 1
                    else: 
                        ax.scatter(hit_list[j][i][0], hit_list[j][i][1], s=80, facecolors=hit_color, edgecolors=edgecolor, alpha=point_alpha, label=legend_label[3])

                        fin_disturbed_balls.append(disturbed_balls[j][i])
                        fin_ground_list.append(ground_list[j][i])
                        fin_highest_list.append((round(highest_list[j][i][0], 3), round(highest_list[j][i][1], 3)))
                        fin_hit_list.append((round(hit_list[j][i][0], 3), round(hit_list[j][i][1], 3)))

                        if isShowNum:
                            ax.annotate(total_ball + 1, (hit_list[j][i][0], hit_list[j][i][1]), c="white", fontsize=5.5
                                        , horizontalalignment="center", verticalalignment="center")
                            
                        vaild_hit_on_height_ball += 1
                else:
                    highest_color = highest_facecolor
                    hit_color = hit_facecolor

                    if disturbed_balls[j][i]: # if disturbed
                        if isShowDistrub:
                            # annotate highest point
                            if isShowHightest:
                                ax.scatter(highest_list[j][i][0], highest_list[j][i][1]
                                            , s=80, facecolors="none", edgecolors=highest_color, alpha=1, label=legend_label[4])
                        
                                if isShowNum:
                                    ax.annotate(total_ball + 1, (highest_list[j][i][0], highest_list[j][i][1]), c=highest_color, fontsize=5.5
                                            , horizontalalignment="center", verticalalignment="center")
                            
                            # annotate hit point
                            ax.scatter(hit_list[j][i][0], hit_list[j][i][1], s=80, facecolors="none", edgecolors=hit_color, alpha=1, label=legend_label[5])
                            
                            fin_disturbed_balls.append(disturbed_balls[j][i])
                            fin_ground_list.append(ground_list[j][i])
                            fin_highest_list.append((round(highest_list[j][i][0], 3), round(highest_list[j][i][1], 3)))
                            fin_hit_list.append((round(hit_list[j][i][0], 3), round(hit_list[j][i][1], 3)))

                            if isShowNum:
                                plt.annotate(total_ball + 1, (hit_list[j][i][0], hit_list[j][i][1]), c=hit_color, fontsize=5.5
                                        , horizontalalignment="center", verticalalignment="center") 

                        invaild_normal_ball += 1
                    else:
                        # annotate highest point
                        if isShowHightest:
                            ax.scatter(highest_list[j][i][0], highest_list[j][i][1]
                                        , s=80, facecolors=highest_color, edgecolors=edgecolor, alpha=point_alpha, label=legend_label[1])
                        
                            if isShowNum:
                                ax.annotate(total_ball + 1, (highest_list[j][i][0], highest_list[j][i][1]), c="white", fontsize=5.5
                                        , horizontalalignment="center", verticalalignment="center")
                        
                        # annotate hit point
                        ax.scatter(hit_list[j][i][0], hit_list[j][i][1], s=80, facecolors=hit_color, edgecolors=edgecolor, alpha=point_alpha, label=legend_label[2])
                        
                        fin_disturbed_balls.append(disturbed_balls[j][i])
                        fin_ground_list.append(ground_list[j][i])
                        fin_highest_list.append((round(highest_list[j][i][0], 3), round(highest_list[j][i][1], 3)))
                        fin_hit_list.append((round(hit_list[j][i][0], 3), round(hit_list[j][i][1], 3)))

                        if isShowNum:
                            ax.annotate(total_ball + 1, (hit_list[j][i][0], hit_list[j][i][1]), c="white", fontsize=5.5
                                        , horizontalalignment="center", verticalalignment="center") 
                        
                        vaild_normal_ball += 1

                if not disturbed_balls[j][i]:
                    dist = GetDist(hit_list[j][i], highest_list[j][i])
                    if dist > dist_hit_highest_table[0 if j < 3 else 1][0]: dist_hit_highest_table[0 if j < 3 else 1][0] = dist # max
                    if dist < dist_hit_highest_table[0 if j < 3 else 1][1]: dist_hit_highest_table[0 if j < 3 else 1][1] = dist # min
                    dist_hit_highest_table[0 if j < 3 else 1][2] += dist # sum, to get avgerage later

                    if dist == 0: dist_hit_highest_table[0 if j < 3 else 1][3] += 1 # hit on highest amount

            total_ball += 1; people_ball_count += 1
            if not isShowDistrub and disturbed_balls[j][i]: total_ball -= 1; people_ball_count -= 1
            if not canDraw: total_ball -= 1

    if isShowDistrub:
        if isShowHightest:
            label_list = legend_label
        else:
            label_list = [legend_label[0], legend_label[2], legend_label[3], legend_label[5], legend_label[6]]

        for label in label_list:
            num = 0
            if label == legend_label[1] or label == legend_label[2]: # is highest or hit, vaild
                num = vaild_normal_ball
            elif label == legend_label[3]: # is hit (on highest), vaild
                num = vaild_hit_on_height_ball
            elif label == legend_label[4] or label == legend_label[5]: # is highest or hit, and distrubed, invaild
                num = invaild_normal_ball
            elif label == legend_label[6]: # is hit (on highest), and distrubed, invaild
                num = invaild_hit_on_height_ball
            else: continue

            if isShowNumOnLengend:
                label_list[label_list.index(label)] += "　" + str(num) + " / {:3}".format(str(total_ball))

        if isShowHightest:
            legend_handles = [
                Line2D([0], [0], marker="o", markersize=11, alpha=1, color="w", markerfacecolor=ground_facecolor, label=label_list[0])
                , Line2D([0], [0], marker="o", markersize=11, alpha=point_alpha, color="w", markerfacecolor=highest_facecolor, markeredgecolor=edgecolor, label=label_list[1])
                , Line2D([0], [0], marker="o", markersize=11, alpha=point_alpha, color="w", markerfacecolor=hit_facecolor, markeredgecolor=edgecolor, label=label_list[2])
                , Line2D([0], [0], marker="o", markersize=11, alpha=point_alpha, color="w", markerfacecolor=hit_on_highest_facecolor, markeredgecolor=edgecolor, label=label_list[3])
                , Line2D([0], [0], marker="o", markersize=10, alpha=1, color="w", markerfacecolor="none", markeredgecolor=highest_facecolor, label=label_list[4])
                , Line2D([0], [0], marker="o", markersize=10, alpha=1, color="w", markerfacecolor="none", markeredgecolor=hit_facecolor, label=label_list[5])
                , Line2D([0], [0], marker="o", markersize=10, alpha=1, color="w", markerfacecolor="none", markeredgecolor=hit_on_highest_facecolor, label=label_list[6])
            ]
        else:
            legend_handles = [
                Line2D([0], [0], marker="o", markersize=11, alpha=1, color="w", markerfacecolor=ground_facecolor, markeredgecolor=edgecolor, label=label_list[0])
                , Line2D([0], [0], marker="o", markersize=11, alpha=point_alpha, color="w", markerfacecolor=hit_facecolor, markeredgecolor=edgecolor, label=label_list[1])
                , Line2D([0], [0], marker="o", markersize=11, alpha=point_alpha, color="w", markerfacecolor=hit_on_highest_facecolor, markeredgecolor=edgecolor, label=label_list[2])
                , Line2D([0], [0], marker="o", markersize=10, alpha=1, color="w", markerfacecolor="none", markeredgecolor=hit_facecolor, label=label_list[3])
                , Line2D([0], [0], marker="o", markersize=10, alpha=1, color="w", markerfacecolor="none", markeredgecolor=hit_on_highest_facecolor, label=label_list[4])
            ]
    else:
        if isShowHightest:
            label_list = [legend_label[0], legend_label[1], legend_label[2], legend_label[3]]
        else:
            label_list = [legend_label[0], legend_label[2], legend_label[3]]

        for label in label_list:
            num = 0
            if label == legend_label[1] or label == legend_label[2]:  # is highest or hit, vaild
                num = vaild_normal_ball
            elif label == legend_label[3]: # is hit (on highest), vaild
                num = vaild_hit_on_height_ball
            else: continue

            if isShowNumOnLengend:
                label_list[label_list.index(label)] += "　" + str(num) + " / {:3}".format(str(total_ball))

        if isShowHightest:
            legend_handles = [
                Line2D([0], [0], marker="o", markersize=11, alpha=1, color="w", markerfacecolor=ground_facecolor, markeredgecolor=edgecolor, label=label_list[0])
                , Line2D([0], [0], marker="o", markersize=11, alpha=point_alpha, color="w", markerfacecolor=highest_facecolor, markeredgecolor=edgecolor, label=label_list[1])
                , Line2D([0], [0], marker="o", markersize=11, alpha=point_alpha, color="w", markerfacecolor=hit_facecolor, markeredgecolor=edgecolor, label=label_list[2])
                , Line2D([0], [0], marker="o", markersize=11, alpha=point_alpha, color="w", markerfacecolor=hit_on_highest_facecolor, markeredgecolor=edgecolor, label=label_list[3])
            ]
        else:
            legend_handles = [
                Line2D([0], [0], marker="o", markersize=11, alpha=1, color="w", markerfacecolor=ground_facecolor, markeredgecolor=edgecolor, label=label_list[0])
                , Line2D([0], [0], marker="o", markersize=11, alpha=point_alpha, color="w", markerfacecolor=hit_facecolor, markeredgecolor=edgecolor, label=label_list[1])
                , Line2D([0], [0], marker="o", markersize=11, alpha=point_alpha, color="w", markerfacecolor=hit_on_highest_facecolor, markeredgecolor=edgecolor, label=label_list[2])
            ]

if not isShow2TypeHand:
    # set figure x-y scale
    x_major_locator = MultipleLocator(xscale)
    y_major_locator = MultipleLocator(yscale)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)

    plt.xlim(-xlim, 0.3) if method == 0 else plt.xlim(-0.3, xlim)
    plt.ylim(-0.1, ylim)
    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.title(scatter_title, fontsize=16)
    plt.legend(handles=legend_handles, bbox_to_anchor=(1.01, 0), loc="lower left", borderaxespad=0)

    plt.tight_layout()
    plt.subplots_adjust(top=0.95, bottom=0.05, right=0.85, left=0.05)
    plt.get_current_fig_manager().full_screen_toggle()

else: 
    axs[0].set_xlim([-xlim, 0.3])
    axs[1].set_xlim([-0.3, xlim])

    axs[0].yaxis.set_ticks_position("right")
    axs[0].yaxis.set_label_position("right")

    for i, ax in enumerate(axs):
        axs[i].set_ylim([-0.1, ylim])
        
        # set figure x-y scale
        x_major_locator = MultipleLocator(xscale)
        y_major_locator = MultipleLocator(yscale)
        ax.xaxis.set_major_locator(x_major_locator)
        ax.yaxis.set_major_locator(y_major_locator)
        
        axs[i].grid(True)
        axs[i].set_xlabel(xlabel)
        axs[i].set_title(subplot_title[i], fontsize=16)

    axs[0].set_ylabel(ylabel, rotation=-90, labelpad=16)
    axs[1].set_ylabel(ylabel)

    plt.legend(handles=legend_handles, bbox_to_anchor=(-0.1, -0.2), loc="lower center", borderaxespad=0, ncol=7)
    plt.subplots_adjust(top=0.9, bottom=0.2, right=0.95, left=0.05, wspace=0.2)

plt.show()

for table in dist_hit_highest_table:
    table[2] /= ballAmount_get * 3 # getting average, 3 is people amount
    print(table)

# --------------------------------------------------------------------------------

fin_index, fin_people_list = [], []
for i in range(total_ball):
    fin_index.append(i + 1)
    fin_people_list.append(people_list[i // ballAmount_get])

data_dict = {
    "Index": fin_index,
    "ClipSource": fin_people_list,
    "GroundPoint": fin_ground_list,
    "HightestPoint": fin_highest_list,
    "HitPoint": fin_hit_list,
    "IsDisturbed": fin_disturbed_balls
}
df = pd.DataFrame(data_dict)
print(df.to_string(index=False, header=False))

csv_path = f"E:/Project/Capstone Project/Tennins Simulator/網球素材/第3次素材(20230611)/球員分析/資料集/High Approximately/Mix/31~50 (Paper 2 - Hit Height)/男乙.csv"
df.to_csv(csv_path, mode="a", index=False, header=not os.path.exists(csv_path), encoding="utf-8-sig")
