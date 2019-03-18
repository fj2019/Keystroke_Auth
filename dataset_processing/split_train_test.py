# encoding=utf-8
import numpy
import random
import os
from dataset_processing import load_all_txt
import pickle

seq_length=30#击键序列的固定长度，即滑动窗口的长度

# 交叉验证时划分数据集
def split_list(n, list):
    num = int(len(list) / 10)
    l = num * n
    if n == 9:
        r = len(list)
    else:
        r = num * n + num
    X_test = list[l:r]
    if l == 0:
        X_train = list[r:]
    elif r == len(list):
        X_train = list[:l]
    else:
        X_train = list[:l] + list[r:]
    return X_train, X_test

def readom_select(x,y,leave):

    samplenum = len(x) * 2
    #print(samplenum)
    if samplenum % 10 >= 5:
        samplenum = (int(samplenum / 10) + 1) * 10
    else:
        samplenum = int(samplenum / 10) * 10
    len1 = samplenum - len(x)

    #print(len1)
    x.extend(random.sample(leave, len1))  # 随机挑选与正例数据量相等的反例数据加到训练集
    y.extend([0] * len1)

    x=numpy.array(x)
    y=numpy.array(y)
    return x,y

#划分数据集
def split_dataset(seq_length):
    keyer = load_all_txt.z_score(seq_length)
    train_list = []  # 所有用户的训练集list
    test_list = []  # 所有用户的测试集list
    for j in range(75):
        #print(len(keyer[j]))
        one = keyer[j]
        random.shuffle(one)  # 随机打乱list
        #print(one)
        train, test = split_list(0, one)
        #print(len(train),len(test))
        train_list.append(train)
        test_list.append(test)

    return train_list,test_list

#生成新的数据集
def gen_dataset(train_list,test_list,userid):

    x_train = train_list[userid]
    y_train = [1] * len(x_train)
    #print(x_train)
    x_test = test_list[userid]
    y_test = [1] * len(x_test)
    #print(x_test)
    leave_train = []#其他用户数据的训练集合，用于构造反例数据
    leave_test = []  # 其他用户数据的测试集合，用于构造反例数据
    for k in range(75):
        if k != userid:
            leave_train.extend(train_list[k])
            leave_test.extend(test_list[k])

    x_train_new,y_train_new=readom_select(x_train,y_train,leave_train)#加入反例后的训练集
    x_test_new,y_test_new=readom_select(x_test,y_test,leave_test)#加入反例后的测试集

    #print(x_train_new.shape)
    #print(x_test_new.shape)

    #将划分好的训练集和测试集保存到本地文件
    file_path='data_processed'+str(userid)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path_train=file_path+'/train.pkl'
    with open(file_path_train, "wb") as f:
        pickle.dump(x_train_new, f)
        pickle.dump(y_train_new, f)

    file_path_test = file_path + '/test.pkl'
    with open(file_path_test, "wb") as f:
        pickle.dump(x_test_new, f)
        pickle.dump(y_test_new, f)

    print('参与者%d保存数据集成功！！!' % (id + 1))
    #return x_train_new,y_train_new,x_test_new,y_test_new
train_list,test_list=split_dataset(seq_length)

def get_train_test(id):
    gen_dataset(train_list, test_list, id)

# if __name__ == "__main__":
#
#     #print(train_list.shape)
#     for id in range(5):#保存参与者的训练集和测试机，取前5个作测试
#         #print(x_train)
#         gen_dataset(train_list,test_list,id)
