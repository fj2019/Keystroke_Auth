# encoding=utf-8

#原始文本中每行击键信息格式：(keyname keydown/keyup timestamp)

#为文本中出现的按键名称进行逐一编号
keycode = {}
for i in range(65, 91):
    keycode[chr(i)] = i
keycode['LMenu'] = 1
keycode['Tab'] = 2
keycode['Return'] = 3
keycode['LShiftKey'] = 4
keycode['Space'] = 32
keycode['Back'] = 5
keycode['OemPeriod'] = 6
keycode['Oemcomma'] = 7
keycode['OemMinus'] = 9
for j in range(10):
    str1 = "D" + str(j)
    keycode[str1] = j + 10
keycode['RShiftKey'] = 20
keycode['OemQuestion'] = 21
keycode['Oemplus'] = 22
for j in range(10):
    str1 = "Oem" + str(j)
    keycode[str1] = j + 100
keycode['Capital'] = 23
keycode['LControlKey'] = 24
keycode['RControlKey'] = 25
keycode['Up'] = 26
keycode['Down'] = 27
keycode['Left'] = 28
keycode['Right'] = 29
keycode['Escape'] = 30
keycode['Delete'] = 31
keycode['End'] = 33
keycode['Insert'] = 34
keycode['OemOpenBrackets'] = 35
for j in range(10):
    str1 = "NumPad" + str(j)
    keycode[str1] = j + 36
for j in range(10):
    str1 = "F" + str(j)
    keycode[str1] = j + 46
keycode['LButton,'] = 56
keycode['Apps'] = 57
keycode['RWin'] = 58
keycode['RMenu'] = 59
keycode['Oemtilde'] = 60
keycode['Home'] = 61
keycode['Next'] = 62
keycode['PageUp'] = 63
keycode['NumLock'] = 64
keycode['Clear'] = 110
keycode['Add'] = 111
keycode['F12'] = 112
keycode['Subtract'] = 113
keycode['Decimal'] = 114

# 提取取单个文本的击键信息，返回一个list构成一个击键序列,其中每个元素的格式[keyid,keydowntime,keyuptime]
def load_txt(path, file):

    #计算一个文本中包含[keyid,keydowntime,keyuptime]的个数
    len1 = 0
    for line in open(path + file):
        len1 = len1 + 1
    num = 0
    keytimelist = [[] for i in range(int(len1 / 2) + 10)]


    d = [] #定义d是为了处理一个按键的keydowntime和keyuptime不相邻的情况

    #逐条读取文本处理成[keyid,keydowntime,keyuptime]格式，保存在keytimelist中
    for line in open(path + file):
        keylist = line.split(' ')
        keylist[0] = keycode[keylist[0]]
        keylist[2] = float(keylist[2])
        if len(d) == 0:
            if keylist[1] == "KeyDown":
                keylist.append(num)
                d.append(keylist)
                num = num + 1
        else:
            f = -1
            for i in range(len(d)):
                if d[i][0] == keylist[0]:
                    f = i
                    break
            if f == -1:
                if keylist[1] == "KeyDown":
                    keylist.append(num)
                    d.append(keylist)
                    num = num + 1
            else:
                if keylist[1] == "KeyUp":
                    keytimelist[d[f][3]].append(keylist[0])
                    keytimelist[d[f][3]].append(d[f][2])
                    keytimelist[d[f][3]].append(keylist[2])
                    del d[f]

    for i in range(len(keytimelist) - 1, -1, -1):
        if len(keytimelist[i]) == 0:
            keytimelist.pop(i)

    return keytimelist