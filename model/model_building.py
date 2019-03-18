# encoding=utf-8
import numpy
import random
import os
from functools import partial
import paddle.v2 as paddle
import paddle.fluid as fluid
import pickle

key_vc = 30*6  # 击键向量的维度
context_len=2 #行卷积的宽度
hidden_size = 128  # RNN神经元个数
reg_num=2# 分类的类别
rnn_type='gru' #RNN类型
stacked_rnn_num=2# RNN堆叠层数

# 构建模型
def get_net(flag):

    # 输入层
    x = paddle.layer.data(name="keys", type=paddle.data_type.dense_vector_sequence(key_vc))
    '''
    # 卷积层
    conv_2 = paddle.layer.row_conv(input=x, context_len=context_len)

    #池化层
    pool = paddle.layer.pooling(input=conv_2, pooling_type=paddle.pooling.Avg())

    #全连接层
    fc=paddle.layer.fc(input=pool,size=1024,bias_attr=False)
    '''
    #RNN层
    if rnn_type == "lstm":
        for i in range(stacked_rnn_num):
            rnn_cell = paddle.networks.simple_lstm(
                input=rnn_cell if i else x, size=hidden_size)
    elif rnn_type == "gru":
        for i in range(stacked_rnn_num):
            rnn_cell = paddle.networks.simple_gru(
                input=rnn_cell if i else x, size=hidden_size)

    else:
        raise Exception("rnn_type error!")

    #dropout层
    dropout1=paddle.layer.dropout(input=rnn_cell, dropout_rate=0.5)

    # 全连接层
    fc = paddle.layer.fc(input=dropout1, size=1024, bias_attr=False)

    dropout2 = paddle.layer.dropout(input=fc, dropout_rate=0.5)

    output = paddle.layer.fc(input=dropout2, size=reg_num, act=paddle.activation.Softmax())

    if flag != 0:
        return output
    else:
        # 定义标签层
        y = paddle.layer.data(name="label", type=paddle.data_type.integer_value(2))

        # 定义损失函数
        cost = paddle.layer.classification_cost(input=output, label=y)
        #print(11111111)
        return cost