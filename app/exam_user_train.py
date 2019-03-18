# coding:utf-8
from pynput import keyboard
from pynput.keyboard import Key
import time
from dataset_processing import split_train_test
from model import model_train


class exam_user_train:
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
    userid = -1
    seq_length=30
    txtid = 0

    def __int__(self, id):
        self.userid = id

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
        if keychar == '/':
            self.txtid = self.txtid + 1
            print(self.txtid)
            file = '0' + str(self.userid) + '.' + str(self.txtid)
            f = open('free_txt/baseline_0/' + file + '.txt', 'w')
            for i in range(len(self.keylist_base)):
                tmp = self.keylist_base[i]
                f.write(tmp[0] + ' ')
                f.write(str(tmp[1]) + ' ')
                f.write(tmp[2] + ' ')
                f.write(str(tmp[3]) + '\n')
            f.close()
            if self.txtid == 3:
                # print(1)
                self.txtid = 0

                datapath = 'free_txt/'

                train_list, test_list = split_train_test.split_dataset(self.seq_length, datapath)

                file_path = 'data_processed' + str(self.userid)
                split_train_test.gen_dataset(train_list, test_list, self.userid, file_path)

                file_path_train = 'dataset_processing/data_processed' + str(self.userid) + '/train.pkl'
                file_path_test = 'dataset_processing/data_processed' + str(self.userid) + '/test.pkl'

                model_train.model_train_user(self.userid, file_path_train, file_path_test)

            self.keylist_base = []
# print('release',key,time.time()-last_time)
        return False


def listener(self):
    while 1:
        with keyboard.Listener(
                on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
