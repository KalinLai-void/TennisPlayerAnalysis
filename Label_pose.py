import cv2
from PIL import Image
import numpy as np
import math
from imutils import perspective
from imutils import contours

import pandas as pd

import os
import sys
from sys import platform

# Settings
#############################################################################
file_path = f"D:\Lab\# 素材\第4次素材(20240414)\王品瑀\正拍"
is_mutiple_files = True 
# if has mutiple files, the file path only set to directory.
# Otherwise, it must include file name (no extension),
# for example, file name is "test.mp4" and path is "D:/Lab/", just set "D:/Lab/test"

# OpenPose path settings
openpose_path = f"D:/Lab/Project/openpose-1.7.0/build/python/openpose/Release"
openpose_model_path = f"D:/Lab/Project/openpose-1.7.0/models/"

method = 0  # 0: 正拍, 1:反拍

# set examining line is at percentage in screen width (0~1)
examining_line_percentage_W = 0.85

screenW, screenH = 540, 303

# To save each round's video
is_save_video = True

# When get trajectory image, whether get complete trajectory
# complete trajectory: from ball enter screen to ball exit screen (True)
# incomplete trajectory: from ball enter screen to ball hit back (False)
is_get_complete_trajectory = False

# To run program whether automatic
is_auto = False
#############################################################################
pressA, pressS, pressD = False, False, False
has_pressA = False

origin_video_out = None # each round's video path (origin)
result_video_out = None # each round's video path (result)
is_video_saving = False

# Import Openpose (Windows/Ubuntu/OSX)
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(openpose_path)
        #os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

# init OpenPose
params = dict()
params["model_folder"] = openpose_model_path
opWrapper, datum = op.WrapperPython(), op.Datum()
opWrapper.configure(params)
opWrapper.start()

if is_mutiple_files:
    items = os.listdir(file_path)
    
    files = []
    for item in items:
        item_path = os.path.join(file_path, item)
        if os.path.isfile(item_path):
            files.append(item_path)
else: cap = cv2.VideoCapture(file_path + ".MP4")

def GetMidPoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def FilterHSV(img):
    # convert BGR to HSV
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # the range of tennis' color
    #lower_color = (30,120,130)
    #upper_color = (60,255,255)
    lower_color = (30, 60, 200)
    upper_color = (70, 255, 255)

    # find color
    mask_img = cv2.inRange(hsv_img, lower_color, upper_color)
    return mask_img

def GetMask(hsv_mask, fg_mask):
    mask1 = hsv_mask == 255
    mask2 = fg_mask == 255
    out = np.zeros(hsv_mask.shape)
    out[mask1 & mask2] = 255
    out = np.array(out, np.uint8)
    return out

def DilateImg(img, times=1):
    tmp = img.copy()
    for i in range(times):
        tmp = cv2.dilate(tmp, None, iterations=2)
    return tmp

def ErodeImg(img, times=1):
    tmp = img.copy()
    for i in range(times):
        tmp = cv2.erode(tmp, None, iterations=2)
    return tmp

def GetDist(p1, p2):
    distance = math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2)
    distance = math.sqrt(distance)
    return distance

pre_target_point, pre_pre_target_point = (0, 0), (0, 0)
is_tracking, pre_is_tracking = False, False
def GetTennis(mask): # remove other similar color object (e.g. racket)
    global pre_target_point, pre_pre_target_point
    global examining_line_x
    global is_tracking, pre_is_tracking, method
    global pressA, pressS, pressD

    num_labels, labels_im, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=4)
    
    # get top-right label (usually top-right label field is target)
    leftest_label_x, rightest_label_x = videoW, 0
    label_x, topmost_label_y, target_label = 0, videoH, 0
    for i in range(1, len(centroids)):
        centroids_list = list(centroids[i])
        if method == 0: # 正拍
            if centroids_list[0] > rightest_label_x:
                rightest_label_x, topmost_label_y = centroids_list[0], centroids_list[1]
                target_label = i
        else: # 反拍
            if centroids_list[0] < leftest_label_x:
                leftest_label_x, topmost_label_y = centroids_list[0], centroids_list[1]
                target_label = i
    origin_labels_im = labels_im
    labels_im[labels_im!=target_label] = 0 # remove other label

    labeled_img = np.zeros_like(mask)

    VAILD_DIFF_RANGE = 0.5
    VAILD_DIST = videoW * 0.2

    if method == 0: # 正拍
        # from right to left
        if ((rightest_label_x <= examining_line_x and pre_target_point[0] > examining_line_x) 
            and (rightest_label_x - pre_target_point[0] < -VAILD_DIFF_RANGE and pre_target_point[0] - pre_pre_target_point[0] < -VAILD_DIFF_RANGE)):
            distance = GetDist((examining_line_x, topmost_label_y), (rightest_label_x, topmost_label_y))
            if distance < VAILD_DIST:
                is_tracking = True
                pressA = True
        # from left to right
        else:
            if not is_get_complete_trajectory:
                if ((rightest_label_x > examining_line_x and pre_target_point[0] <= examining_line_x)
                    or (rightest_label_x < examining_line_x and pre_target_point[0] < examining_line_x and pre_pre_target_point[0] < examining_line_x 
                        and rightest_label_x > pre_target_point[0] and pre_target_point[0] > pre_pre_target_point[0])
                    or (rightest_label_x - pre_target_point[0] > VAILD_DIFF_RANGE and pre_target_point[0] - pre_pre_target_point[0] < -VAILD_DIFF_RANGE)):
                    #if pre_is_tracking: pressS = True
                    is_tracking = False
            else:
                if ((rightest_label_x > examining_line_x and pre_target_point[0] <= examining_line_x)
                    and (rightest_label_x - pre_target_point[0] > VAILD_DIFF_RANGE and pre_target_point[0] - pre_pre_target_point[0] > VAILD_DIFF_RANGE)):
                    #if pre_is_tracking: pressS = True
                    is_tracking = False

        label_x = rightest_label_x
    else: # 反拍
        if ((leftest_label_x > examining_line_x and pre_target_point[0] <= examining_line_x) 
            and (leftest_label_x - pre_target_point[0] > VAILD_DIFF_RANGE and pre_target_point[0] - pre_pre_target_point[0] > VAILD_DIFF_RANGE)):
            distance = GetDist((examining_line_x, topmost_label_y), (leftest_label_x, topmost_label_y))
            if distance < VAILD_DIST:
                is_tracking = True
                pressA = True
        # from left to right
        else:
            if not is_get_complete_trajectory:
                if ((leftest_label_x < examining_line_x and pre_target_point[0] >= examining_line_x)
                    or (leftest_label_x > examining_line_x and pre_target_point[0] > examining_line_x and pre_pre_target_point[0] > examining_line_x 
                        and leftest_label_x < pre_target_point[0] and pre_target_point[0] < pre_pre_target_point[0])
                    or (leftest_label_x - pre_target_point[0] < -VAILD_DIFF_RANGE and pre_target_point[0] - pre_pre_target_point[0] > VAILD_DIFF_RANGE)):
                    #if pre_is_tracking: pressS = True
                    is_tracking = False
            else:
                if ((leftest_label_x < examining_line_x and pre_target_point[0] >= examining_line_x)
                    and (leftest_label_x - pre_target_point[0] < -VAILD_DIFF_RANGE and pre_target_point[0] - pre_pre_target_point[0] < -VAILD_DIFF_RANGE)):
                    #if pre_is_tracking: pressS = True
                    is_tracking = False
                
        label_x = leftest_label_x

    #print(is_tracking, pre_is_tracking, leftest_label_x, pre_target_point[0], pre_pre_target_point[0])

    tmp_is_tracking = is_tracking
    if is_tracking:
        distance = GetDist(pre_target_point, (label_x, topmost_label_y))
        if distance < VAILD_DIST or not pre_is_tracking:
            target_label, min_dict = target_label, 999999
            for i in range(1, len(centroids)):
                centroids_list = list(centroids[i])
                d = GetDist(pre_target_point, (centroids_list[0], centroids_list[1]))
                if d < min_dict and d >= 10:
                    min_dict = d
                    target_label = i
            origin_labels_im[origin_labels_im!=target_label] = 0
            labels_im = origin_labels_im

            # Map component labels to hue val (HSV), then convent to RGB
            label_hue = np.uint8(179 * labels_im / np.max(labels_im)) if np.max(labels_im) != 0 else np.uint8(labels_im * 0)
            blank_ch = 255 * np.ones_like(label_hue)
            labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
            labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
            labeled_img[label_hue==0] = 0 # set bg label to black
            labeled_img[label_hue!=0] = 255 # set target label to white
            labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_BGR2GRAY)
        else: # out of tracking range
            tmp_is_tracking = False
            labeled_img = np.zeros_like(mask)
            if method == 0: # 正拍
                label_x, topmost_label_y = 0, 0
            else: # 反拍
                label_x, topmost_label_y = videoW, videoH

    # ignore cannot captured frame
    if method == 0: # 正拍
        if label_x != 0 and topmost_label_y != 0: 
            pre_pre_target_point = pre_target_point
            pre_target_point = (label_x, topmost_label_y)
    else: # 反拍
        if label_x != videoW and topmost_label_y != videoH: 
            pre_pre_target_point = pre_target_point
            pre_target_point = (label_x, topmost_label_y)
    return labeled_img, tmp_is_tracking

def ShowFrameState(frame, mask_dilate, labeled_img):
    global pre_frame
    pre_frame = cv2.add(pre_frame, labeled_img)

    frame = cv2.line(frame, (examining_line_x, 0), (examining_line_x, videoH), (0, 0, 255), 5)

    mask_dilate_BGR = cv2.cvtColor(mask_dilate, cv2.COLOR_GRAY2BGR)
    labeled_img_BGR = cv2.cvtColor(labeled_img, cv2.COLOR_GRAY2BGR)
    pre_frame_BGR = cv2.cvtColor(pre_frame, cv2.COLOR_GRAY2BGR)

    # Add spacing between each image
    frame_states = [frame, mask_dilate_BGR, labeled_img_BGR, pre_frame_BGR]
    texts = ["Origin (include pose)", "HSV Filter Mask", "Tennis Mask", "Trajectory Mask"]
    imgs, new_imgs = [], []
    for i in range(4):
        imgs.append(Image.fromarray(frame_states[i]))
        new_imgs.append(Image.new("RGB", (videoW + 100, videoH + 100), color=(255, 255, 255)))
        new_imgs[i].paste(imgs[i], (50, 50))
        new_imgs[i] = np.asarray(new_imgs[i])
        
        (w, h), _ = cv2.getTextSize(texts[i], cv2.FONT_HERSHEY_DUPLEX, 3, 5)
        cv2.rectangle(new_imgs[i], (70, 130 - h), (90 + w, 190), (0, 0, 0), -1)
        cv2.putText(new_imgs[i], texts[i], (80, 150), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 255, 255), 5, cv2.LINE_AA)

    hor = np.hstack((new_imgs[0], new_imgs[3]))
    hor2 = np.hstack((new_imgs[1], new_imgs[2]))
    ver = np.vstack((hor, hor2))
    
    cv2.namedWindow("Video", 0)
    cv2.resizeWindow("Video", (screenW + 100) * 2, (screenH + 100) * 2)
    cv2.imshow("Video", ver)

pre_frame = None
is_new_round = True
is_coming, pre_is_coming = True, False
has_lowest_tmp, has_lowest = False, False
has_highest_tmp, has_highest = False, False

poseKeyPoints = []

def GetTargetPoseKeypoints():
    global pre_poseKeyPoints

    keyPoints = datum.poseKeypoints
    if keyPoints is None:
        keyPoints = pre_poseKeyPoints
    else:
        if len(keyPoints) >= 2:
            minDist = videoW
            for p in keyPoints:
                if method == 0: ref = 0
                else: ref = videoW
                d = GetDist((p[0][0], p[0][1]), (ref, p[0][1]))
                if d < minDist:
                    minDist = d
                    keyPoints = [p.tolist()]

    return keyPoints

def Run(c):
    global knn
    global pre_frame, is_new_round, is_coming, pre_is_coming, pre_is_tracking
    global has_lowest, has_highest, has_lowest_tmp, has_highest_tmp
    global touch_ground_point, hightest_point, hit_point
    global poseKeyPoints, pre_poseKeyPoints
    global origin_video_out, result_video_out, is_video_saving
    global pressA, pressS, pressD, has_pressA
    pressA, pressS, pressD = False, False, False

    ret = c.grab()
    if ret is False: return ret, None
    ret, frame = c.retrieve()
    if frame is None: return ret, frame
    if is_video_saving: origin_video_out.write(frame) # saving origin video clip

    fgmask1 = knn.apply(frame)

    if is_new_round == True:
        is_new_round = False
        is_coming = True
        has_lowest_tmp, has_lowest = False, False
        has_highest_tmp, has_highest = False, False
        
        if method == 0:
            touch_ground_point, hightest_point, hit_point = (0, 0), (videoW, videoH), (videoW, videoH)
        else:
            touch_ground_point, hightest_point, hit_point = (0, 0), (videoW, videoH), (0, 0)
        poseKeyPoints = []

        pre_frame = np.zeros_like(fgmask1)

    fgmask1 = cv2.medianBlur(fgmask1, 5)

    #fgmask1 = ErodeImg(fgmask1)
    hsv_mask = FilterHSV(frame)
    #mask = GetMask(fgmask, hsv_mask)
    mask = cv2.bitwise_and(fgmask1, hsv_mask)
    ret, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    mask_dilate = DilateImg(mask, 3)
    labeled_img, is_tracking = GetTennis(mask_dilate)

    # human pose estimation
    datum.cvInputData = frame
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))
    poseKeyPoints = GetTargetPoseKeypoints()
    frame = datum.cvOutputData    

    has_lowest_tmp = False
    has_highest_tmp = True
    is_coming = False

    # detect ball
    cnt, _ = cv2.findContours(labeled_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnt) > 0:
        (cnt, _) = contours.sort_contours(cnt)
        for (i, cc) in enumerate(cnt):
            box = cv2.minAreaRect(cc)
            box = cv2.boxPoints(box)
            box = box.astype("int")
            box = perspective.order_points(box)
            cv2.drawContours(frame, [box.astype(int)], 0, (0, 255, 0), 2)
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = GetMidPoint(tl, tr)
            (tlblX, tlblY) = GetMidPoint(tl, bl)
            (blbrX, blbrY) = GetMidPoint(bl, br)
            (trbrX, trbrY) = GetMidPoint(tr, br)
            cv2.line(frame, (int(tltrX), int(tltrY)),
                    (int(blbrX), int(blbrY)), (255, 0, 0), 2)
            cv2.line(frame, (int(tlblX), int(tlblY)),
                    (int(trbrX), int(trbrY)), (255, 0, 0), 2)

            M = cv2.moments(cc)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            if method == 0:
                if center[0] < hit_point[0]:
                    is_coming = True
                    hit_point = center
            else:
                if center[0] > hit_point[0]:
                    is_coming = True
                    hit_point = center
                
            has_lowest_tmp = True
            if center[1] > touch_ground_point[1] and is_coming == True and has_lowest == False:
                has_lowest_tmp = False
                touch_ground_point = center
            if is_coming == True and has_lowest_tmp == True:
                has_lowest = True
                if center[1] < hightest_point[1]:
                    has_highest_tmp = False
                    hightest_point = center

    if has_lowest and has_highest_tmp and not (touch_ground_point[1] - hightest_point[1] <= 100):
        has_highest = True

    #print(pre_is_coming, is_coming, pre_is_tracking, has_highest, has_lowest)
    if has_pressA and pre_is_coming and not is_coming and pre_is_tracking and has_highest and has_lowest: pressS = True
    pre_is_coming = is_coming
    pre_is_tracking = is_tracking
    pre_poseKeyPoints = poseKeyPoints

    ShowFrameState(frame, mask_dilate, labeled_img)

    if is_video_saving: result_video_out.write(frame) # saving result video clip
    return ret, frame

start_frame, end_frame = 0, 0
ball_count = 1
continue_frame = 0

file_name = file_path.split("\\")[-1]
print("Path:", file_path)
if is_mutiple_files: file_path = os.path.join(file_path, file_name)
# reading from a existing csv
if os.path.exists(file_path + "/" + file_name + ".csv"):
    data = pd.read_csv(file_path + "/" + file_name + ".csv")
    print(data[["Index", "File", "Time"
               , "StartFrame", "EndFrame"
               , "GroundPoint", "HightestPoint", "HitPoint"
               , "IsDistrubed"]].to_string(index=False))

    ball_count = len(data["Index"]) + 1 # get to last index to continue

    # get to last frame to continue
    if not is_mutiple_files: continue_frame = int(data["EndFrame"][len(data["Index"]) - 1]) 

isQuit = False
def Perform(cc, fname=file_name):
    global origin_video_out, result_video_out, is_video_saving
    global start_frame, end_frame
    global pressA, pressD, pressS, has_pressA
    global is_new_round, is_auto
    global ball_count, isQuit

    global videoW, videoH, fps
    videoW, videoH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = round(cap.get(cv2.CAP_PROP_FPS))

    global examining_line_x
    examining_line_x = int(videoW * examining_line_percentage_W) if method == 0 else int(videoW * (1 - examining_line_percentage_W))

    global touch_ground_point, hightest_point, hit_point
    if method == 0:
        touch_ground_point, hightest_point, hit_point = (0, 0), (videoW, videoH), (videoW, videoH)
    else:
        touch_ground_point, hightest_point, hit_point = (0, 0), (videoW, videoH), (0, 0)

    while cc.isOpened() and not isQuit:
        ret, frame = Run(cc)
        if ret is False: break

        keycode = cv2.waitKey(1) & 0xFF

        if keycode == ord("a") or (is_auto and pressA):
            is_new_round = True
            start_frame = int(cc.get(cv2.CAP_PROP_POS_FRAMES))

            if is_save_video:
                # create each round's clip, preparing to save
                result_clips_path = file_path + "/Clips/Result/"
                if not os.path.exists(result_clips_path):
                    os.makedirs(result_clips_path)
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                result_video_out = cv2.VideoWriter(result_clips_path + str(ball_count) + ".avi"
                                                , fourcc, fps // 3, (videoW,  videoH))

                origin_clips_path = file_path + "/Clips/Origin/"
                if not os.path.exists(origin_clips_path):
                    os.makedirs(origin_clips_path)
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                origin_video_out = cv2.VideoWriter(origin_clips_path + str(ball_count) + ".avi"
                                                , fourcc, fps // 3, (videoW,  videoH))

                is_video_saving = True
                print("Saving video {}...".format(ball_count))

            pressA, has_pressA = False, True

        if keycode == ord("s") or keycode == ord("d") or (is_auto and (pressS or pressD)):
            if touch_ground_point == (0, 0) or hightest_point == (videoW, videoH): continue # ignore invaild data
            is_new_round = True

            start_time = str((start_frame // int(fps)) // 60).zfill(2) + ":" + str((start_frame // int(fps)) % 60).zfill(2)
            end_frame = int(cc.get(cv2.CAP_PROP_POS_FRAMES))
            data_dict = {
                "Index": [ball_count],
                "File": [fname],
                "Time": [start_time],
                "StartFrame": [start_frame],
                "EndFrame": [end_frame],
                "GroundPoint": [touch_ground_point],
                "HightestPoint": [hightest_point],
                "HitPoint": [hit_point],
                "PoseKeyPoints": [poseKeyPoints]
            }
            
            has_pressA = False
            if keycode == ord("s") or (is_auto and pressS): # normal
                data_dict["IsDistrubed"] = False
                pressS = False
            elif keycode == ord("d") or (is_auto and pressD): # has noise to disturbed
                data_dict["IsDistrubed"] = True
                pressD = True

            df = pd.DataFrame(data_dict)
            print(df.to_string(index=False, header=False))

            # record data in this round to file
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            csv_path = file_path + "/" + file_name +".csv"
            df.to_csv(csv_path, mode="a", index=False, header=not os.path.exists(csv_path), encoding="utf-8-sig")
            
            # record the trajectory image file
            img_path = file_path + "/Trajectory/"
            if not os.path.exists(img_path):
                os.makedirs(img_path)
            img_filename = img_path + str(ball_count) + ".jpg"
            # cv2.imwrite(img_filename, pre_frame) # origin usage, but error (the reason is in next line)
            cv2.imencode(".jpg", pre_frame)[1].tofile(img_filename) # because path has chinese, so using imencode()

            if is_save_video:
                result_video_out.release()
                origin_video_out.release()
                is_video_saving = False
                print("Saved video {}.".format(ball_count))

            ball_count += 1
            if is_mutiple_files: break

        if keycode == ord("q"): isQuit = True
        if keycode == ord("z"): is_auto = not is_auto; print("is_auto = {}".format(is_auto))

    cc.release()

if not is_mutiple_files: 
    cap.set(cv2.CAP_PROP_POS_FRAMES, continue_frame - 1)
    knn = cv2.createBackgroundSubtractorKNN()
    Perform(cap)
else:
    for (i, file) in enumerate(files):
        fname = file.split('\\')[-1]
        print("File {}:".format(i), fname)
        if i < ball_count: continue
        knn = cv2.createBackgroundSubtractorKNN()
        cap = cv2.VideoCapture(file)
        Perform(cap, fname)
        if isQuit: break

cv2.destroyAllWindows()
