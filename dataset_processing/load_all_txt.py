# encoding=utf-8
import numpy
import os
from dataset_processing import load_single_txt


# 提取所有用户的击键文本，每个人的击键序列转化为击键特征向量的集合
def load_all_txt(seq_length):

    all_seq_list = [] #全部的划分后击键序列
    all_seq_id = [] #击键序列的对应的参与者的标号

    for dircnum in range(3):
        dirc = "baseline_" + str(dircnum) + "/"
        path = "free_txt/" + dirc  # 文件夹目录
        files = os.listdir(path)
        for file in files:
            #print(file)

            stable_seq_list = [] #单个文本划分后的击键序列集合
            seq_id = [] #击键序列的对应的参与者的标号

            key_seq = load_single_txt.load_txt(path, file) #单个文本的击键序列

            key_vec_list = [] #击键向量构成的击键序列
            for i in range(len(key_seq) - 1):

                key_vec = [] #击键向量,格式：[keyid1,keyid2,H1,H2,UD,DD]
                key_vec.append(key_seq[i][0])
                key_vec.append(key_seq[i + 1][0])
                key_vec.append(key_seq[i][2] - key_seq[i][1])
                key_vec.append(key_seq[i + 1][2] - key_seq[i + 1][1])
                key_vec.append(key_seq[i + 1][1] - key_seq[i][2])
                key_vec.append(key_seq[i + 1][1] - key_seq[i][1])
                key_vec_list.append(key_vec)

            # 将key_vec_list击键序列划分成固定长度seq_length的击键序列
            l = 0
            r = seq_length
            len1 = len(key_vec_list)
            for i in range(int(len1 / seq_length)):
                stable_seq_list.append(key_vec_list[l:r])
                seq_id.append(int(file[:3]) - 1)
                l = l + seq_length
                r = r + seq_length
            all_seq_list.extend(stable_seq_list)
            all_seq_id.extend(seq_id)

    keyer = [[] for i in range(75)] #将每个参加者的击键序列集合在一起，每个元素为一个参与者的所有击键序列，有75个参与者

    for i in range(len(all_seq_id)):
        keyer[all_seq_id[i]].append(all_seq_list[i])
    #print(keyer)
    return keyer

#使用Z-score，数据归一化
def z_score(seq_length):

    keyer=load_all_txt(seq_length)
    #print(keyer)
    #print(keyer[0])
    #针对每个参与者的击键向量的每一维数据进行归一化
    for i in range(75):
        #maxv = [0] * 6
        #minv = [100000000] * 6
        col = [[]] * 6 #统计每一维的所有数据
        one = keyer[i]
        #print(one)
        '''
        for k in range(6):
            for j in range(len(one)):
                for l in range(seq_length):
                    #maxv[k] = max(maxv[k], one[j][l][k])
                    #minv[k] = min(minv[k], one[j][l][k])
                    col[k].append(one[j][l][k])

        for k in range(6):
            mean = numpy.mean(col[k]) #计算每一维的均值
            std = numpy.std(col[k])   #计算每一维的标准差
            for j in range(len(one)):
                for l in range(seq_length):
                    one[j][l][k] = (one[j][l][k] - mean) / std
        '''
        #将击键序列展成一维
        for j in range(len(one)):
               tmpone=one[j]
               tmp=[]
               for k in range(seq_length):
                   tmp.extend(tmpone[k])
               one[j]=tmp
        #print(one)
        a=numpy.array(one)
        #print(a.shape)
        #print keyer
        #print a

    return keyer





