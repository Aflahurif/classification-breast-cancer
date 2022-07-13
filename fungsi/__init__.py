import cv2
import pandas as pd
from skimage.feature import graycomatrix, graycoprops
from sklearn import svm

props = [
        "energy",
        "homogeneity",
        "contrast",
        "correlation"
        ]
degrees = [0,45,90,135]


def glcm(img):
    row = []
    value = []
    # data = []
    upload = img.split("/")
    file = upload[-1]
    img_read = cv2.imread(img,0)
    name_gray = "tmp/img/"+file[:-4]+" gray.jpg"
    cv2.imwrite(name_gray,img_read)
    resz = cv2.resize(img_read, (200,200))
    name_resize = "tmp/img/"+file[:-4]+" resize.png"
    cv2.imwrite(name_resize,resz)
    im2 = cv2.equalizeHist(resz) 
    name_hist = "tmp/img/"+file[:-4]+" hist.png"
    cv2.imwrite(name_hist,im2)
    image_disp = {
        'original'  : img,
        'gray'      : name_gray,
        'resize'    : name_resize,
        'histogram' : name_hist
    }
    # print(image_disp)
    for degree in degrees:
        glcm = graycomatrix(im2, [5], [degree], symmetric=True, normed=True)
        ro = []
        ro.append(degree)
        for prop in props:
            ro.append(float(graycoprops(glcm, prop)))
            row.append(float(graycoprops(glcm, prop)))
        # print(ro)
        value.append(ro)
        # data.append(row)
    
    return image_disp, value, pd.DataFrame([row],columns=kolom())

def kolom():
    col = []
    for degree in degrees:
        for prop in props:
            col.append(prop+'('+str(degree)+')')
    return col

glcm_df = pd.read_csv("tmp/glcm_no_index.csv")
X = glcm_df.drop('label',axis=1)
Y = glcm_df['label']
clf = svm.SVC(decision_function_shape='ovr')
clf.fit(X, Y)

# train_glcm()
def predict_glcm(img):
    l, x,res = glcm(img)
    # print(clf.predict(res)[0])
    return l,x, clf.predict(res)[0]