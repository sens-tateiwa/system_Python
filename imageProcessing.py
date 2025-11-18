import cv2
import numpy as np
import sharedFlag

laser_point = (int(720/2), int(540/2))

def HoughTransform(image):
    
    #グレースケールに変換
    if len(image.shape) == 3 and image.shape[2] == 3:
        image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    else:
        image_gray = image
    cv2.imshow('image_gray',image_gray)
    cv2.waitKey(0)

    #平均化によるノイズ除去
    #第一引数で指定したオブジェクトgrayscale_imgを輝度で平均化処理する。第二引数は平均化するピクセル数で、今回の場合は9,9は9x9ピクセルの計81ピクセル
    image_average = cv2.blur(image_gray,(9,9)) 
    #cv2.imshow('image_average',image_average)
    #cv2.waitKey(0)

    #二値化
    _,image_binary = cv2.threshold(image_average,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

    cv2.imshow('image_binary',image_binary)
    cv2.waitKey(0)

    #エッジ検出
    med_val = np.median(image_binary)
    sigma = 0.33  # 0.33
    min_val = int(max(0, (1.0 - sigma) * med_val))
    max_val = int(max(255, (1.0 + sigma) * med_val))
    #image_edge = cv2.Canny(image_binary,threshold1=min_val,threshold2=max_val)
    image_edge = cv2.Canny(image_binary,125,255)
    #cv2.imshow('image_edge',image_edge)
    #cv2.waitKey(0)

    #エッジを太くする処理　Hough変換で円を抽出しやすくするため
    #image_open = cv2.morphologyEx(image_binary,cv2.MORPH_OPEN,kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)),iterations=3)
    image_edge = cv2.morphologyEx(image_edge,cv2.MORPH_DILATE,kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)))
    #cv2.imshow('image_open',image_edge)
    #cv2.waitKey(0)
    
    #細線化　ximgproc.THINNING_ZHANGSUEN or THINNING_GUOHALL
    #image_thinning = cv2.ximgproc.thinning(image_edge,thinningType=cv2.ximgproc.THINNING_GUOHALL)
    #cv2.imshow('image_thinning',image_thinning)
    #cv2.waitKey(0)

    #print(image_edge.shape)
    
    #ハフ変換で円を検出 
    # （入力画像,
    #   method:cv2.HOUGH_GRADIENT or cv2.HOUGH_GRADIENT_ALT(計算速度良,精度低い or　計算遅い,精度高い,ノイズに強い),
    #   dp:入力画像に対する蓄積面の解像度の逆比,
    #   minDist:検出された円の中心間の最小距離[ピクセル])返り値は検出された円の2次元配列[x座標,y座標,r半径]
    circles = cv2.HoughCircles(image_edge,method=cv2.HOUGH_GRADIENT,dp=3,minDist=50,minRadius=100,maxRadius=150)

    #print(circles)
    """
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 2)#ここで指定する画像はカラー画像
            cv2.circle(image, (x, y), 2, (0, 0, 255), 3)
    
    #線の検出と描画
    lines = cv2.HoughLines(image_edge,1,np.pi/180,80)
    if lines is not None:
        for indx in range(len(lines)):
            for rho,theta in lines[indx]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
    """
    #cv2.imshow('image_hough',image)
    #cv2.imwrite(rootDir+'/'+dataName +"_hough.png",image)
    #cv2.waitKey(0)

    #反転
    image_binary_invert = cv2.bitwise_not(image_binary)

    return image

def changeScale(image):
    scale = 0.5
    height, width = image.shape[0],image.shape[1]
    resized_image = cv2.resize(image,(int(width*scale),int(height*scale)) )
    return resized_image

def createTemplateCircleImage(radius=120):
    
    height = int(radius*2)
    width = int(radius*2)
    #template画像を生成
    image_template = np.zeros((height,width,3),dtype=np.uint8)#黒背景
    #グレースケールに変換
    if len(image_template.shape) == 3 and image_template.shape[2] == 3:
        image_template = cv2.cvtColor(image_template,cv2.COLOR_BGR2GRAY)
    else:
        image_template = image_template

    cv2.circle(image_template,(int(width/2),int(height/2)),radius,(255,255,255),thickness=-1)#白色の円
    #反転
    #image_template = cv2.bitwise_not(image_template)#白背景に黒色の円
    #cv2.imshow("template image",image_template)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #cv2.imshow('matching image',image_template)
    #cv2.imwrite('C:/Users/yuto/Downloads'+'/'+'templateimage_new.png',image_template)
    #cv2.waitKey(0)

    image_template = changeScale(image_template)

    return image_template

def TemplateMatching(image, image_template, isPlotMatchpoint=False):
    to_templateimage_center_y, to_templateimage_center_x = int(image_template.shape[0]/2),int(image_template.shape[1]/2)

    #グレースケールに変換
    if len(image.shape) == 3 and image.shape[2] == 3:
        image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    else:
        image_gray = image

    #平均化によるノイズ除去
    #第一引数で指定したオブジェクトgrayscale_imgを輝度で平均化処理する。第二引数は平均化するピクセル数で、今回の場合は9,9は9x9ピクセルの計81ピクセル
    #image_average = cv2.blur(image_gray,(9,9)) 
    image_average = image_gray #平均化いらなくね？処理時間はあってもなくても変わらん

    """
    #二値化
    _,image_binary = cv2.threshold(image_average,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    cv2.imshow('image_binary',image_binary)
    cv2.waitKey(0)
    """

    #method = cv2.TM_CCORR_NORMED   #正規化相互相関(NCC:Normalized Cross-Correlation)
    method = cv2.TM_CCOEFF_NORMED  #正規化相関係数(ZNCC:Zero-mean Normalized Cross-Correlation)
    # NCCよりもZNCCの方が輝度値の変化に強い
    
    height, width = image.shape[0],image.shape[1]
    """
    ROI_x_start = 0#int(width*0.25)
    ROI_x_end = width#int(width*0.75)
    ROI_y_start = 0#int(height*0.25)
    ROI_y_end = height#int(height*0.75)
    """

    margin_rate = 0.12#注目領域を制限する、0で制限なし、全体のmargin_rateの割合分の上下左右領域を無視してマッチングする
    margin_rate = 0

    ROI_x_start = int(width*margin_rate)
    ROI_x_end = int(width*(1-margin_rate))
    ROI_y_start = int(height*margin_rate)
    ROI_y_end = int(height*(1-margin_rate))

    image_ROI = image_average[ROI_y_start:ROI_y_end,ROI_x_start:ROI_x_end] #関心領域：ROI(Region of Interest)
    match_result = cv2.matchTemplate(image_ROI,image_template,method=method)
    match_point = np.argwhere(match_result == match_result.max())
    #print("match_point",match_point)

    match_y = match_point[0][0]
    match_x = match_point[0][1]

    match_center = (int(match_x+to_templateimage_center_x)+ROI_x_start, int(match_y+to_templateimage_center_y)+ROI_y_start)#検出した指先位置の中心(x,y)

    """
    #テンプレートマッチングした最大値の位置ではきれいに指先中心に一致しなかったため処理を追加した
    #以下、追加した処理
    #テンプレートマッチングのマッチ率が閾値以上の点の中心を計算し、その中心とマッチングの最大値の位置の中点をトラッキング点とした
    threshold = 0.2
    y_indices, x_indices = np.where(match_result > threshold)
    center_x = np.mean(x_indices)
    center_y = np.mean(y_indices)
    try:#閾値以上の点の中心が計算できる時、中心と最大値の位置の中点をマッチ位置(トラッキング点)とする
        center = (int(center_x+to_templateimage_center_x)+ROI_x_start, int(center_y+to_templateimage_center_y)+ROI_y_start)  #マッチング結果の閾値以上の重心
    except:#閾値以上の点の中心が計算できない時、マッチの最大値の位置をそのままマッチ位置とする
        center = match_center
    match = (int((match_center[0]+center[0])/2), int((match_center[1]+center[1])/2))
    """

    #マッチに関する座標やテンプレートイメージの重ね合わせ描画
    #ここで指定する画像はカラー画像
    if(isPlotMatchpoint):
        cv2.circle(image, match_center, to_templateimage_center_x, (0, 255, 0), 1) #緑の縁でテンプレートマッチングした位置を表示
        cv2.circle(image, match_center, 2, (0, 255, 0), 2)      #緑の点でテンプレートマッチングした最大値の座標を表示
        #cv2.circle(image, center, 2, (255, 0, 0), 2)            #青い点でテンプレートマッチングした閾値以上の点の重心を表示
    
    return image, match_center


def calculateCentor2FingerDistance(image, image_template, laser_point, isPlotMatchpoint=False):
    image, match_center = TemplateMatching(image, image_template, isPlotMatchpoint)

    #height, width = image.shape[0],image.shape[1]

    #print(f"laser_center is {laser_center}")

    distance = (match_center[0]-laser_point[0], match_center[1]-laser_point[1])

    if(isPlotMatchpoint):
        #cv2.line(image,match_center,laser_center,(255,255,255),2)
        cv2.arrowedLine(image,laser_point,match_center,(255,255,255),2)
        cv2.circle(image, laser_point, 3, (0, 0, 255), -2)            #cv2.circle(入力画像, centor, radius, color, thickness)
        cv2.circle(image, match_center, 2, (255, 255, 255), -2)        #白い点で

    return image,distance

def calculateLaserPoint(file_name):
    image = cv2.imread(file_name, cv2.IMREAD_COLOR)
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(image_gray)
    """
    _,image_binary = cv2.threshold(image_gray,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    image_binary = changeScale(image_binary) 
    
    y_indices, x_indices = np.where(image_binary == 255)
    """
    image_gray = changeScale(image_gray) 
    
    y_indices, x_indices = np.where(image_gray >= max_val-10)
    center_x = np.mean(x_indices)
    center_y = np.mean(y_indices)
    center = (int(center_x), int(center_y))
    
    #cv2.circle(image, max_loc, 2, (0, 255, 0), 2)#ここで指定する画像はカラー画像
    #cv2.imshow('image',image)
    #cv2.waitKey(0)

    #cv2.circle(image, center, 2, (0, 0, 255), 2)
    #cv2.imshow('image',image)
    #cv2.waitKey(0)

    #print(f"laser_point is {max_loc}")
    print(f"center is {center}")
    return center

if __name__ == "__main__":
    #rootDir = 'C:/Users/yuto/Downloads'
    #dataName = 'image_0.png'
    rootDir = 'C:/Users/yuto/Documents/system_python/data'
    dataName = '20250703_151737_list/image_353.png'

    laserImage = 'Image__2025-11-13__16-05-34.png'

    OrizinalImage = 'Image__2025-11-11__10-36-38.png'

    laser_point = calculateLaserPoint('C:/Users/yuto/Documents/system_python/'+laserImage)

    #画像読み込み
    #image = cv2.imread('C:/Users/yuto/Documents/system_python/'+laserImage, cv2.IMREAD_COLOR)
    image = cv2.imread("C:/Users/yuto/Downloads/"+OrizinalImage, cv2.IMREAD_COLOR)
    image = changeScale(image)

    radius = 120    
    image_template = createTemplateCircleImage(radius)

    image,distance = calculateCentor2FingerDistance(image,  image_template, laser_point, isPlotMatchpoint=True)

    cv2.imwrite("C:/Users/yuto/Downloads/matching_"+OrizinalImage,image)
    
    cv2.imshow("template image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
