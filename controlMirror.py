import optoMDC
import time


def setMirror():
    mre2 = optoMDC.connectmre2()
    ch_0 = mre2.Mirror.Channel_0                         #channel_0がX,channel_1がY
    ch_0.StaticInput.SetAsInput()                        # (1) here we tell the Manager that we will use a static input
    ch_0.InputConditioning.SetGain(1.0)                  # (2) here we tell the Manager some input conditioning parameters
    ch_0.SetControlMode(optoMDC.UnitType.XY)             #電流(current)でなくX,Y値でミラーを制御
    ch_0.LinearOutput.SetCurrentLimit(1.0)               #電流の最大値を制限
    ch_0.Manager.CheckSignalFlow()                       # This is a useful method to make sure the signal flow is configured correctly.
    #si_0 = mre2.Mirror.Channel_0.StaticInput

    ch_1 = mre2.Mirror.Channel_1
    ch_1.StaticInput.SetAsInput()                        # (1) here we tell the Manager that we will use a static input
    ch_1.InputConditioning.SetGain(1.0)                  # (2) here we tell the Manager some input conditioning parameters
    ch_1.SetControlMode(optoMDC.UnitType.XY)
    ch_1.LinearOutput.SetCurrentLimit(1.0)
    ch_1.Manager.CheckSignalFlow()                       # This is a useful method to make sure the signal flow is configured correctly.
    #si_1 = mre2.Mirror.Channel_1.StaticInput

    return mre2


def changeAngle(X, Y,mre2):
    mre2.Mirror.Channel_0.StaticInput.SetXY(X) 
    mre2.Mirror.Channel_1.StaticInput.SetXY(Y) 

    return

if __name__ == "__main__":
    X=0
    Y=0
    distance = (150,150)
    intervalX = 0.05/126
    intervalY = 0.05/126
    mre2 = setMirror()
    t1 = time.time()
    while((time.time()-t1)<10):
        X += distance[0]*intervalX
        Y += distance[1]*intervalY
        print(X,Y)
        changeAngle(X,Y,mre2)
        time.sleep(0.5)
    changeAngle(0,0,mre2)
        