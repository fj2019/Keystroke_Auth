# encoding=utf-8
import os
import paddle.v2 as paddle

import pickle
from model import model_building

feeding={'keys': 0, 'label': 1}
epochs=200#迭代轮数
buffer_size=200#缓冲大小
batch_size=50 #批处理大小



paddle.init(use_gpu=False)

#创建一个reader
def reader_creator(data, label):
    def reader():
        for i in range(len(data)):
            yield [data[i]], label[i]
    return reader

#模型训练
def model_train(train_reader,test_reader,userid):


    eva_list=[]#每一轮迭代的模型错误率
    # 利用cost创建parameters
    cost = model_building.get_net(0)
    parameters = paddle.parameters.create(cost)
    #print(11111111)
    # 创建优化器
    optimizer = paddle.optimizer.Adam(learning_rate=0.001, regularization=paddle.optimizer.L2Regularization(rate=0.01))
    #print(11111111)
    # 创建训练器
    trainer = paddle.trainer.SGD(cost=cost,
                                 parameters=parameters,
                                 update_equation=optimizer)

    # 事件处理器
    def event_handler(event):
        if isinstance(event, paddle.event.EndIteration):
            if event.batch_id % 1 == 0:
                print ("Pass %d, Batch %d, Cost %f" % (
                    event.pass_id, event.batch_id, event.cost))

        # 保存迭代的模型参数
        if isinstance(event, paddle.event.EndPass):
            file_path = 'model_parameter' + str(userid)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            with open(file_path + '/params_pass_%d.tar' % event.pass_id, 'w') as f:
                trainer.save_parameter_to_tar(f)
            result = trainer.test(reader=test_reader)  # 在测试集上准确率
            # print(result)
            eva=float(result.metrics['classification_error_evaluator'])
            eva_list.append(eva)
            print ("Test with Pass %d, Cost %f, %s\n" % (event.pass_id, result.cost, result.metrics))


    # 开始训练
    trainer.train(
        reader=train_reader,
        feeding=feeding,
        event_handler=event_handler,
        num_passes=epochs)

    return eva_list

#单个用户的模型训练
def model_train_user(id):
    file_path_train = 'data_processed' + str(id) + '/train.pkl'
    file_path_test = 'data_processed' + str(id) + '/test.pkl'

    # 读取训练集
    with open(file_path_train, "rb") as f:
        X_train = pickle.load(f)
        Y_train = pickle.load(f)
    print(X_train.shape)
    # 读取测试集
    with open(file_path_test, "rb") as f:
        X_test = pickle.load(f)
        Y_test = pickle.load(f)

    # print(X_test.shape)
    train_reader = paddle.batch(paddle.reader.shuffle(reader_creator(X_train, Y_train), buf_size=buffer_size),
                                batch_size=batch_size)
    test_reader = paddle.batch(paddle.reader.shuffle(reader_creator(X_test, Y_test), buf_size=buffer_size),
                               batch_size=batch_size)
    print('参与者%d开始测试。。。' % (id+1))
    eva_list=model_train(train_reader, test_reader, id)
    opt_parm=1.0
    opt_id=-1# 记录错误率最低的参数文件标号
    for i in range(len(eva_list)):
        if opt_parm>eva_list[i]:
            opt_id=i
            opt_parm=eva_list[i]
    #print('model_parameter' + str(id) + '/params_pass_' + str(opt_id) + '.tar')
    os.rename('model_parameter' + str(id)+'/params_pass_'+str(opt_id)+'.tar','model_parameter'+ str(id)+'/_.tar')#将最优的参数文件标记

    print('模型训练完成！')
    #print(eva_list)

if __name__ == "__main__":
   model_train_user(3)#随机取一位用户测试
   #print(opt_id)






