from flask import session, url_for, g
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from datetime import datetime
import glob
global vid, vid_data
users = {}
# global_count = 0
app = Flask(__name__, template_folder='templates')
app.secret_key = 'secretkey'
app.config['videos'] = r'C:\Users\91981\PycharmProjects\flask\static\videos'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'

@app.route('/',  methods=['POST', 'GET'])
def success():
    print("0")
    if request.method == 'POST':
        print("1")
        req = request.form
        email =req.get("email")
        print(email, "2")
        g.global_count = 0
        users[g.global_count] = email

        # global_count = global_count + 1
        # users.update({"user": email})
        print(users)
        if len(users) == 0:
            print("Username not found")
        else:
            global user
            g.user = users[g.global_count]
            print(g.user, "3")
            print("3")
            directory = g.user
            parent_dir = r'C:\Users\91981\PycharmProjects\flask\static\videos'
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            print("directory created", directory)
            g.global_count += 1

        return redirect(url_for('enterdetails'))
    return render_template('success.html')

print(users)
@app.route('/enterdetails', methods=['POST', 'GET'])
def enterdetails():
    print("4")
    return render_template('enterdetails.html')

@app.route('/uploaded/', methods = ['POST', 'GET'])
def uploaded():
    print("6")
    if request.method == "POST":
        print("7")
        #and request.files:
        # print("hello")
        # # print(request.files['video'])
        # video = request.files['video']
        # req = request.form
        # video = req.get("video")
        # print(video)
        print(users)
        vid = request.files['video']
        print(vid)
        if vid == '':
            print("Empty file")
        else:
            g.filename = secure_filename(vid.filename)
            basedir = os.path.abspath(os.path.dirname(__file__))
            vid.save(os.path.join(basedir, app.config["videos"],user,  g.filename))
            g.path = os.path.join(basedir, app.config["videos"],user,  g.filename)
            print("video name", g.filename)

        return render_template("uploaded.html", filename=g.filename)
    return render_template('uploaded.html')

if __name__ == '__main__':
    app.run(debug=True)

# start = datetime.now()
name = glob.glob(r'C:\Users\91981\PycharmProjects\flask\static\videos\*.mp4')
file_name = str(name[0])
cap = cv2.VideoCapture()


def getFrames(sec):
     cap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
     result, frame = cap.read()
     if result:
         cv2.imwrite("img" + str(count) + ".png", frame)
         return result


sec = 0
frameRate = 1/24
count = 1
obj1 = getFrames(sec)
similarity_ratio = []
while obj1:
     count += 1
     sec = sec + frameRate
     sec = round(sec, 2)
     obj1 = getFrames(sec)

for i in range(1, count-1):
     im1 = cv2.imread('img{}.png'.format(i))
     im2 = cv2.imread('img{}.png'.format(i+1))
     img1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
     img2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
     arr1 = np.array(img1)
     arr2 = np.array(img2)
     dim1 = np.shape(arr1)
     dim2 = np.shape(arr2)
     total_elements1 = dim1[0]*dim1[1]
     total_elements2 = dim2[0]*dim2[1]
     sub = arr1 -arr2
     z = np.count_nonzero(sub)
     dim3 = np.shape(sub)
     total_elements3 = dim3[0]*dim3[1]
     zero_elements = total_elements3 - z
     sim_ratio = total_elements3/zero_elements
     similarity_ratio.append(sim_ratio)

print(similarity_ratio)

database_to_be_deleted = dict()
database_to_be_added = dict()
ofl_start = int(0.1*count)
print("ofl start: ", ofl_start)
ofl_end = (count//2) +1
print("ofl end: ", ofl_end)
print("count: ", count)
for h in range(ofl_start, ofl_end):
    print(str(h) + " value of h ")
    temp_to_be_deleted = []
    temp_to_be_added = []
    for i in range(0, count//h):
        if (i+1) * h < count:
            for j in range(i*h, (i+1)*h):
                # print("value of j: ",j)
                if 1.00 <= similarity_ratio[j] <= 1.099:
                    # print("true")
                    temp_to_be_deleted = temp_to_be_deleted + [j]
                else:
                    temp_to_be_added = temp_to_be_added + [j]
        else:
            # print("false")
            break

    database_to_be_deleted[h] = list(set(temp_to_be_deleted))
    database_to_be_added[h] = list(set(temp_to_be_added))
print(database_to_be_deleted)
print(database_to_be_added)


height, width, layers = im1.shape
size = (width, height)
for i in database_to_be_added:
    out = cv2.VideoWriter('fps_2_video{}.avi'.format(i), cv2.VideoWriter_fourcc(*'DIVX'), 24, size)
    for j in database_to_be_added[i]:
        img = cv2.imread("img" + str(j) + ".png")
        out.write(img)
    out.release()
    print("fps_video{}.avi".format(i) + " created")
# end = datetime.now()
# print("time of execution :", str(end-start)[5:])

