import face_recognition
from PIL import Image
import cv2
from sklearn.neighbors import NearestNeighbors
import time
import random
from sklearn.metrics.pairwise import cosine_similarity
import os
import shutil
import numpy
from flask import Flask, request
import json
import base64
import pickle

#基于开源框架的人脸识别，错误对应的code查看文件

def save_image(image, addr, id):
    address = addr + id + '.jpg'
    cv2.imwrite(address, image)#保存图片

app = Flask('face_reg')
#初始化
# all = {}
# ids = {}
# nn = {}

#都是list对象
all = pickle.load(open("known.pkl", "rb")) #全部的特征
ids = pickle.load(open("ids.pkl", "rb")) #相对应的id
nn = pickle.load(open("search.pkl", "rb")) #近邻搜索

timeF = 24 #视频采集频率

@app.route('/', methods=['POST'])
def handler():
    res = {}
    mode = str(request.json.get('mode')) #使用模式，1是注册人脸，2是识别人脸，3是更新已有人脸特征，4是删除指定已有人脸
    id = str(request.json.get('id')) #传入的id，识别模式不是必须
    b64 = str(request.json.get('base64')) #视频/图片的base64编码
    format = str(request.json.get('format')) #文件格式
    check = str(request.json.get('check')) #注册模式是否检测该人脸已在库中
    database = str(request.json.get('database')) #那一个数据库下的人脸
    if not database or database == "None":
        res["code"] = "112"
        return json.dumps(res)
    path = database + "/"
    if database in all: #判断数据库是否已经注册过
        cur = all[database]
        curid = ids[database]
        curnn = nn[database]
    else: #没注册过需要先注册
        if mode == "1":
            all[database] = []
            cur = all[database]
            ids[database] = []
            curid = ids[database]
            os.mkdir(path)
            os.mkdir(path + "known") #known保存注册的底片
            os.mkdir(path + "tmp") #tmp保存每次识别时传入的照片，最多保存5张，以便收集数据
            nn[database] = NearestNeighbors(n_neighbors=1, algorithm='auto', metric='euclidean') #基于欧式距离的近邻搜索
            curnn = nn[database]
        else:
            res["code"] = "113"
            return json.dumps(res)
    if mode in ["1", "2", "3", "4"]:
        if mode == "2": #识别人脸
            if format not in ["mp4", "mov", "jpg"]: #规定的视频/图片的格式
                res["code"] = "110"
                return json.dumps(res)
            else:
                format = "." + format
        if mode != "4":
            if b64 and b64 != "None": #确保base64正确
                try:
                    b64 = bytes(b64, encoding="utf-8")#转二进制
                    inputdata = base64.b64decode(b64)#编码参数必须是二进制数据
                except:
                    res["code"] = "102"
                    return json.dumps(res)
            else:
                res["code"] = "102"
                return json.dumps(res)
        if mode != "2":
            if not id or id == "None":
                res["code"] = "103"
                return json.dumps(res)

        if mode == "1":
            if os.path.exists(path + id): #id已经存在
                res["code"] = "104"
                return json.dumps(res)
            else:
                file = open(path + "known/" + id + ".jpg", 'wb') #保存注册人脸图片留底
                file.write(inputdata)
                file.close()
                try:
                    known_image = face_recognition.load_image_file(path + "known/" + id + ".jpg")
                    encoding = face_recognition.face_encodings(known_image)
                    if len(encoding) > 1: #如果图片里存在多个人脸
                        res["code"] = "106"
                        if os.path.exists(path + "known/" + id + ".jpg"):
                            os.remove(path + "known/" + id + ".jpg")
                        return json.dumps(res)
                    else:
                        biden_encoding = encoding[0]
                except:
                    res["code"] = "106"
                    if os.path.exists(path + "known/" + id + ".jpg"):
                        os.remove(path + "known/" + id + ".jpg")
                    return json.dumps(res)
                if check == "1" and cur: #如果启用检测，判断该人脸是否已经注册过
                    distances, cid = curnn.kneighbors([biden_encoding])
                    cos = cosine_similarity([biden_encoding], [cur[cid[0][0]]])
                    if cos > 0.965: #阈值设定
                        res["code"] = "111"
                        if os.path.exists(path + "known/" + id + ".jpg"):
                            os.remove(path + "known/" + id + ".jpg")
                        return json.dumps(res)
                    else: #添加注册人脸信息，更新pikle本地保存
                        cur.append(biden_encoding)
                        pickle.dump(all, open("known.pkl", "wb"))
                        curid.append(id)
                        pickle.dump(ids, open("ids.pkl", "wb"))
                        curnn.fit(cur)
                        pickle.dump(nn, open("search.pkl", "wb"))
                        res["code"] = "100"
                        os.mkdir(path + id)
                        return json.dumps(res)
                else:
                    cur.append(biden_encoding)
                    pickle.dump(all, open("known.pkl", "wb"))
                    curid.append(id)
                    pickle.dump(ids, open("ids.pkl", "wb"))
                    curnn.fit(cur)
                    pickle.dump(nn, open("search.pkl", "wb"))
                    res["code"] = "100"
                    os.mkdir(path + id)
                    return json.dumps(res)

        if mode == "2": #识别模式
            if cur:
                if format in [".mp4", ".mov"]: #如果传入的是视频
                    video_format = format
                    curName = str(random.randint(0, 10)) #视频临时保存
                    while os.path.exists(path + "tmp/" + curName + video_format):
                        curName = str(random.randint(0, 10))#生成0-10之间的随机整数
                    try: #保存并读取视频
                        file = open(path + "tmp/" + curName + video_format, 'wb') #二进制格式打开文件只用于写入
                        file.write(inputdata)
                        file.close()
                        #cv2.VideoCapture参数是视频文件路径则打开视频，是0则表示打开笔记本内置摄像头
                        videoCapture = cv2.VideoCapture(path + "tmp/" + curName + video_format)
                    except:
                        res["code"] = "105"#视频无法解析，并删除视频
                        if os.path.exists(path + "tmp/" + curName + video_format):
                            os.remove(path + "tmp/" + curName + video_format)
                        return json.dumps(res)
                    for i in range(1, 73):
                        #按既定帧数抽取三张图片
                        # cap.read()是指按帧读取视频
                        # ret, frame是cap.read()的两个返回值。
                        # ret是布尔值，读取帧是正确的返回True，如文件读取到结尾，返回值就为False。
                        # frame就是每一帧的图像，是个三维矩阵
                        success, frame = videoCapture.read()
                        if not success: #视频帧数已经读完
                            res["code"] = "106"#视频质量问题
                            if os.path.exists(path + "tmp/" + curName + video_format):
                                os.remove(path + "tmp/" + curName + video_format)
                            if os.path.exists(path + "tmp/" + curName + ".jpg"):
                                os.remove(path + "tmp/" + curName + ".jpg")
                            return json.dumps(res)

                        if (i % timeF == 0): #按帧数频率抽取     视频采集频率timeF=24
                            try:
                                save_image(frame, path + "tmp/", curName)
                                known_image = face_recognition.load_image_file(path + "tmp/" + curName + ".jpg")
                                encoding = face_recognition.face_encodings(known_image)
                                biden_encoding = encoding[0]
                            except:
                                im = Image.open(path + "tmp/" + curName + ".jpg")
                                im = im.rotate(90, expand=True)
                                im.save(path + "tmp/" + curName + ".jpg")
                                try: #因为苹果手机的视频可能会被识别为旋转，旋转状态人脸无法被识别，后续需探索是否可以从根源解决这个问题
                                    known_image = face_recognition.load_image_file(path + "tmp/" + curName + ".jpg")
                                    encoding = face_recognition.face_encodings(known_image)
                                    biden_encoding = encoding[0]
                                except: #进行旋转为正方向，因为原始选装状态未知所以可能要进行多次旋转。
                                    im = Image.open(path + "tmp/" + curName + ".jpg")
                                    im = im.rotate(180, expand=True)
                                    im.save(path + "tmp/" + curName + ".jpg")
                                    try:
                                        known_image = face_recognition.load_image_file(path + "tmp/" + curName + ".jpg")
                                        encoding = face_recognition.face_encodings(known_image)
                                        biden_encoding = encoding[0]
                                    except:
                                        if os.path.exists(path + "tmp/" + curName + video_format):
                                            os.remove(path + "tmp/" + curName + video_format)
                                        if os.path.exists(path + "tmp/" + curName + ".jpg"):
                                            os.remove(path + "tmp/" + curName + ".jpg")
                                        continue
                            if len(encoding) > 1: #出现多个人脸
                                res["code"] = "106"
                                if os.path.exists(path + "tmp/" + curName + video_format):
                                    os.remove(path + "tmp/" + curName + video_format)
                                if os.path.exists(path + "tmp/" + curName + ".jpg"):
                                    os.remove(path + "tmp/" + curName + ".jpg")
                                return json.dumps(res)
                            distances, cid = curnn.kneighbors([biden_encoding])
                            cos = cosine_similarity([biden_encoding], [cur[cid[0][0]]])
                            if cos > 0.965:
                                res["id"] = curid[cid[0][0]]
                                res["code"] = "100"
                                shutil.copyfile(path + "tmp/" + curName + ".jpg", path + curid[cid[0][0]] + "/" + str(random.randint(0, 4)) + ".jpg") #识别成功保存人脸，维持最多五个
                                if os.path.exists(path + "tmp/" + curName + video_format):
                                    os.remove(path + "tmp/" + curName + video_format)
                                if os.path.exists(path + "tmp/" + curName + ".jpg"):
                                    os.remove(path + "tmp/" + curName + ".jpg")
                                return json.dumps(res)
                    try:
                        biden_encoding
                        res["code"] = "107"
                    except:
                        res["code"] = "106"
                    if os.path.exists(path + "tmp/" + curName + video_format):
                        os.remove(path + "tmp/" + curName + video_format)
                    if os.path.exists(path + "tmp/" + curName + ".jpg"):
                        os.remove(path + "tmp/" + curName + ".jpg")
                    return json.dumps(res)
                else: #如果是图片
                    curName = str(random.randint(0, 10))
                    while os.path.exists(path + "tmp/" + curName + ".jpg"):
                        curName = str(random.randint(0, 10))
                    try:
                        file = open(path + "tmp/" + curName + ".jpg", 'wb')
                        file.write(inputdata)
                        file.close()
                    except:
                        if os.path.exists(path + "tmp/" + curName + ".jpg"):
                            os.remove(path + "tmp/" + curName + ".jpg")
                        res["code"] = "106"
                        return json.dumps(res)
                    try:
                        known_image = face_recognition.load_image_file(path + "tmp/" + curName + ".jpg")
                        encoding = face_recognition.face_encodings(known_image)
                        if len(encoding) > 1:
                            res["code"] = "106"
                            os.remove(path+ "tmp/" + curName + ".jpg")
                            return json.dumps(res)
                        else:
                            biden_encoding = encoding[0]
                    except:
                        res["code"] = "106"
                        if os.path.exists(path + "tmp/" + curName + ".jpg"):
                            os.remove(path + "tmp/" + curName + ".jpg")
                        return json.dumps(res)
                    try:
                        distances, cid = curnn.kneighbors([biden_encoding])
                        cos = cosine_similarity([biden_encoding], [cur[cid[0][0]]])
                    except:
                        res["code"] = "106"
                        if os.path.exists(path + "tmp/" + curName + ".jpg"):
                            os.remove(path + "tmp/" + curName + ".jpg")
                        return json.dumps(res)
                    if cos > 0.965:
                        res["id"] = curid[cid[0][0]]
                        res["code"] = "100"
                        shutil.copyfile(path + "tmp/" + curName + ".jpg", path + curid[cid[0][0]] + "/" + str(random.randint(0, 4)) + ".jpg")
                        if os.path.exists(path + "tmp/" + curName + ".jpg"):
                            os.remove(path + "tmp/" + curName + ".jpg")
                        return json.dumps(res)
                    else:
                        res["code"] = "107"
                        if os.path.exists(path + "tmp/" + curName + ".jpg"):
                            os.remove(path + "tmp/" + curName + ".jpg")
                        return json.dumps(res)
            else:
                res["code"] = "108"
                return json.dumps(res)

        if mode == "3": #更新人脸特征
            if os.path.exists(path + id): #id存在
                file = open(path + "known/" + id + "_replace.jpg", 'wb')
                file.write(inputdata)
                file.close()
                try:
                    known_image = face_recognition.load_image_file(path + "known/" + id + "_replace.jpg")
                    encoding = face_recognition.face_encodings(known_image)
                    if len(encoding) > 1:
                        os.remove(path + "known/" + id + "_replace.jpg")
                        res["code"] = "106"
                        return json.dumps(res)
                    else:
                        biden_encoding = encoding[0]
                except:
                    if os.path.exists(path + "known/" + id + "_replace.jpg"):
                        os.remove(path + "known/" + id + "_replace.jpg")
                    res["code"] = "106"
                    return json.dumps(res)
                pos = curid.index(id) #找到id的索引
                cur[pos] = biden_encoding #更新人脸表征
                pickle.dump(all, open("known.pkl", "wb"))
                curnn.fit(cur) #重新更新搜索结构
                pickle.dump(nn, open("search.pkl", "wb"))
                if os.path.exists(path + "known/" + id + ".jpg"):
                    os.remove(path + "known/" + id + ".jpg") #删除旧的底片
                os.rename(path + "known/" + id + "_replace.jpg", path + "known/" + id + ".jpg")
                res["code"] = "100"
                return json.dumps(res)
            else:
                res["code"] = "109"
                return json.dumps(res)

        if mode == "4": #删除模式
            try:
                delId = curid.index(id) #找到id索引
            except:
                res["code"] = "109"
                return json.dumps(res)
            curid[delId] = curid[-1] #删除操作
            curid.pop()
            pickle.dump(ids, open("ids.pkl", "wb"))
            cur[delId] = cur[-1]
            cur.pop()
            pickle.dump(all, open("known.pkl", "wb"))
            if cur:
                curnn.fit(cur)
                pickle.dump(nn, open("search.pkl", "wb"))
            shutil.rmtree(path + id)
            if os.path.exists(path + "known/" + id + ".jpg"):
                os.remove(path + "known/" + id + ".jpg")
            res["code"] = "100"
            return json.dumps(res)
    else:
        res["code"] = "101"
        return json.dumps(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=65530, threaded=True)