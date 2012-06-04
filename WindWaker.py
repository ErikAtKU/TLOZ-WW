from PIL import ImageDraw, Image
import glob, os, sys, re
def reduce(text):
    count = 0
    for i in range(0,len(text)-2):
        if(text[i]==text[i+1]==text[i+2]):
            text = text.replace(text[i]+text[i]+text[i]," "+text[i]+text[i])
            count+=1
    if(count==0):
        for i in range(0,len(text)-1):
            if(text[i]==text[i+1]):
                temp = re.sub("[aeiou]","-",text[i])
                temp = re.sub("[bcdfghjklmnpqrstvwxz]"," ",temp)
                text = text.replace(text[i]+text[i],text[i]+temp)
                count+=1
    text = re.sub(" ","",text)
    if(count == 0):
        return text
    return reduce(text)
def convert(text):
    text = text.lower()
    text = re.sub("bh","b",text)
    text = re.sub("tch","tu",text)
    text = re.sub("ch","t",text)
    text = re.sub("dh","d",text)
    text = re.sub("fh","f",text)
    text = re.sub("gh","g",text)
    text = re.sub("jh","j",text)
    text = re.sub("kh","k",text)
    text = re.sub("lh","l",text)
    text = re.sub("mh","m",text)
    text = re.sub("nh","n",text)
    text = re.sub("ph","f",text)
    text = re.sub("qh","q",text)
    text = re.sub("rh","r",text)
    text = re.sub("she","si",text)
    text = re.sub("sh","s",text)
    text = re.sub("th","t",text)
    text = re.sub("vh","v",text)
    text = re.sub("wh","w",text)
    text = re.sub("xh","x",text)
    text = re.sub("zh","z",text)
    text = re.sub("ci","si",text)
    text = re.sub("ce","se",text)
    text = re.sub("c","k",text)
    text = re.sub("j","z",text)
    text = re.sub("f","h",text)
    text = re.sub("l","r",text)
    text = re.sub("q","k",text)
    text = re.sub("shi","si",text)
    text = re.sub("tsu","tu",text)
    text = re.sub("wi","wa",text)
    text = re.sub("we","wa",text)
    text = re.sub("wo","wu",text)
    text = re.sub("v","h",text)
    text = re.sub("x","k",text)
    text = re.sub("ye","ya",text)
    text = re.sub("yi","ya",text)
    return reduce(text)
def punctuation(letter):
    letter = re.sub("\(","left",letter)
    letter = re.sub("\)","right",letter)
    letter = re.sub("\-","dash",letter)
    letter = re.sub("\,","comma",letter)
    letter = re.sub("\.","period",letter)
    letter = re.sub("[^a-z0-9]","null",letter)
    return letter
def translate(name,text):
    offset = 1
    text = convert(text)
    path = sys.path[0]+"\WW\\"
    im = Image.open(path+"a.bmp")
    rows = text.split("@")
    length = 0
    for i in rows:
        if len(i) > length:
            length = len(i)
    height = len(rows)
    length *= 50
    height *= 56
    diagram = Image.new("RGBA",(length,height),(255,255,255))
    longest = 0
    for i in range(0,len(rows)):
        letters = []
        pos = 0
        line = []
        for j in range(0,len(rows[i])):
            temp = punctuation(rows[i][j])
            if(temp != "null"):
                line.append(temp)
            if(temp == "period"):
                line.append("space")
        j = 0
        print line
        while (j < len(line)):
            if(len(line)>1+j):
                try:
                    im = Image.open(path+line[j]+line[j+1]+".bmp")
                    print line[j],
                    j+=1
                except IOError:
                    try:
                        im = Image.open(path+line[j]+".bmp")
                    except IOError:
                        try:
                            im = Image.open(path+line[j]+"u.bmp")
                        except IOError:    
                            im = Image.open(path+"a.bmp")
                            im = im.crop((0,0,0,56))
                            pos-=offset
            else:
                try:
                    im = Image.open(path+line[j]+".bmp")
                except IOError:
                    try:
                        im = Image.open(path+line[j]+"u.bmp")
                    except IOError:    
                        im = Image.open(path+"a.bmp")
                        im = im.crop((0,0,0,56))
                        pos-=offset
            (le,up,ri,bo) = im.getbbox()
            print line[j]
            diagram.paste(im,(pos,i*56,pos+ri,(i+1)*56))
            pos+=ri+offset
            j+=1
        pos = pos
        if(pos > longest):
            longest = pos-offset
    diagram = diagram.crop((0,0,longest,len(rows)*56))
    diagram.save(path+name+".png")
    diagram.show()
translate("lol","the legend of zelda:wind waker@gather the might of the storms@evil approaches(ganons wrath)")