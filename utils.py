'''
Created on Oct 21, 2015

@author: I309388
'''
from PIL import Image
def lev_distance(s,t):
    if s==t:
        return 0
    if min([len(s),len(t)])==0:
        return max([len(s),len(t)])
    v0=[]
    v1=[]
    for i in range(len(t)+1):
        v0.append(i)
        v1.append(0)
    for i in range(len(s)):
        v1[0]=i+1
        for j in range(len(t)):
            cost=(s[i]!=t[j])
            v1[j+1]=min([v1[j]+1,v0[j+1]+1,v0[j]+cost])
        for j in range(len(v0)):
            v0[j]=v1[j]
    return v1[len(t)]
def binaryzation(im,treshold):
    im=im.convert("L")
    table=[]
    for i in range(256):
        if i<=treshold:
            table.append(0)
        else:
            table.append(1)
    im=im.point(table,"1")
    return im
def img2str(im):
    im=binaryzation(im,140)
    (width,height)=im.size
    pix=im.load()
    res=""
    for i in range(height):
        for j in range(width):
            res+=(str(pix[j,i]))
        res+=('\n')
    return res
def spliteImg(im):
    (width,height)=im.size
    last=0
    status=False
    start=0
    charList=[]
    pix=im.load()
    for i in range(0,width):
        count=0
        for j in range(0,height):
            if pix[i,j]==0:
                count+=1
        if(count>0 and last<=0):
            status=True
            start=i
        elif count<=0 and last>0:
            if status:
                split=im.crop((start,0,i,height))
                charList.append(split)
        last=count
    result=[]
    for char in charList:
        (width,height)=char.size
        pix=char.load()
        last=0
        status=False
        start=0
        for i in range(0,height):
            count=0
            for j in range(0,width):
                if pix[j,i]==0:
                    count+=1
            if(count!=0 and last==0):
                status=True
                start=i
            if(count==0 and last!=0):
                if status:
                    split=char.crop((0,start,width,i))
                    if (split.size)[0]*(split.size)[1]>10:
                        result.append(split)
            last=count
    return result

def classify_knn(im,trainSet):
    minDis=65535
    minNum=-1
    for num in range(len(trainSet)):
        disCurr=lev_distance(img2str(im), trainSet[num])
        if disCurr<=minDis:
            minDis=disCurr
            minNum=num
    return minNum
def loadTrainSet():
    trainSet=[]
    for i in range(10):
        im=Image.open("C:\\excel\\Train\\"+str(i)+".png")
        descaled=im.resize((8, 13), Image.ANTIALIAS)
        trainSet.append(img2str(descaled))
    return trainSet
def recognize(im,trainSet):
    res=""
    im=binaryzation(im, 145)
    chars=spliteImg(im)
    for char in chars:
        char=char.resize((8, 13), Image.ANTIALIAS)
        char.show()
        res+=str(classify_knn(char,trainSet))
    return res
def denoise(im):
    (width,height)=im.size
    temp=im.copy()
    pix=im.load()
    pixtemp=temp.load()
    for i in range(1,width-1):
        for j in range(1,height-1):
            if pixtemp[i,j]==0:
                if pixtemp[i-1,j]!=0 or pixtemp[i+1,j]!=0 or pixtemp[i,j-1]!=0 or pixtemp[i,j+1]!=0:
                    pix[i,j]=1

if __name__ == '__main__':
    trainSet=loadTrainSet()
    im=Image.open("C:\\excel\\testSet\\4647.PNG")
    print(recognize(im,trainSet))