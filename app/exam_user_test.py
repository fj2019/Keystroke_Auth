# coding:utf-8
from pynput import keyboard
from pynput import keyboard
from pynput.keyboard import Key
import time
import numpy
import paddle.v2 as paddle
from model import model_building

class exam_user_test:
    userid=-1
    upnum = 0
    path = "model_parameter" + str(userid) + "/_.tar"
    with open(path) as f:
        parameters = paddle.parameters.Parameters.from_tar(f)

    feeding = {'keys': 0, 'label': 1}
    out = model_building.get_net(1)
    keycode = {}
    for i in range(65, 91):
        keycode[str(chr(i))] = i
    keycode['space'] = 32
    keycode['shift'] = 4
    keycode['backspace'] = 5
    keycode['.'] = 7
    keycode[','] = 6
    keycode['/'] = 8
    keylist_base = []
    def __init__(self,id):
        self.userid=id

    def on_press(self, key):
        # print(key)
        if key == Key.space:
            keychar = 'space'
        elif key == Key.shift:
            keychar = 'shift'
        elif key == Key.backspace:
            keychar = 'backspace'
        else:
            keychar = format(key.char).encode("utf-8").upper()

            # print(keychar)
            print(keychar, self.keycode[keychar], 'KeyDown', int(time.time() * 1000))
            tmp = []
            tmp.append(keychar)
            tmp.append(self.keycode[keychar])
            tmp.append('KeyDown')
            tmp.append(int(time.time() * 1000))
            self.keylist_base.append(tmp)
            return False

    def on_release(self, key):
        self.upnum+=1
        # print(key)
        if key == Key.space:
            keychar = 'space'
        elif key == Key.shift:
            keychar = 'shift'
        elif key == Key.backspace:
            keychar = 'backspace'
        else:
            keychar = format(key.char).encode("utf-8").upper()

        print(keychar, self.keycode[keychar], 'KeyUp', int(time.time() * 1000))
        tmp = []
        tmp.append(keychar)
        tmp.append(self.keycode[keychar])
        tmp.append('KeyUp')
        tmp.append(int(time.time() * 1000))
        self.keylist_base.append(tmp)
        lengt = len(self.keylist_base)
        if self.upnum%50==0:
            keytimelist = [[] for i in range(int(lengt / 2) + 10)]
            d = []
            num = 0
            for i in range(lengt):
                keylist = self.keylist_base[i]
                # print(keylist)
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

            # print(keytimelist)
            for i in range(len(keytimelist) - 1, -1, -1):
                if len(keytimelist[i]) == 0:
                    keytimelist.pop(i)
            # print(keytimelist)
            key_word_list = []
            keylist1 = keytimelist
            for i in range(len(keylist1) - 1):
                key_word = []
                key_word.append(keylist1[i][0])
                key_word.append(keylist1[i + 1][0])
                # key_word.append(keylist[i+2][0])

                key_word.append(keylist1[i][2] - keylist1[i][1])
                key_word.append(keylist1[i + 1][2] - keylist1[i + 1][1])
                # key_word.append(keylist[i+2][2]-keylist[i+2][1])

                key_word.append(keylist1[i + 1][1] - keylist1[i][2])
                key_word.append(keylist1[i + 1][1] - keylist1[i][1])
                key_word_list.append(key_word)
            # print(key_word_list)
            # print(len(key_word_list))
            seq_length = 30
            l = 0
            r = seq_length
            # print(r)
            len1 = len(key_word_list)
            xx = []
            while r < len1:
                xx.append(key_word_list[l:r])
                l = l + 1
                r = r + 1
            if r > len1:
                xx.append(key_word_list[len1 - seq_length:len1])

            # 将击键序列展成一维
            for j in range(len(xx)):
                tmpone = xx[j]
                tmp = []
                for k in range(seq_length):
                    tmp.extend(tmpone[k])
                xx[j] = tmp
            X_test=numpy.array(xx)
            len1=X_test.shape[0]
            for i in range(len1):
                test_batch = []
                # print(i.shape)
                test_batch.append([list(X_test[i])])

                test_batch = numpy.array(test_batch)
                # print(test_batch.shape)
                probs = paddle.infer(output_layer=self.out, parameters=self.parameters, input=[test_batch], feeding=self.feeding)
                print(probs[0][0])
                if probs[0][0] < 0.5:
                    num = num + 1
            #print(num / len1)
            if num >= int(0.15 *len1):
                print("经系统检测，存在入侵可能请输入验证码！！")
                #强制中断用户操作,转入验证
            else:
                print("账户安全！！")

            self.keylist_base=[]

        return False

    def listener(self):
        while 1:
            with keyboard.Listener(
                    on_press=self.on_press, on_release=self.on_release) as listener:
                listener.join()
