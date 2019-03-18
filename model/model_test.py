# encoding=utf-8
import numpy
import paddle.v2 as paddle

import pickle
from model import model_building

feeding={'keys': 0, 'label': 1}
epochs=200#迭代轮数
buffer_size=200#缓冲大小
batch_size=50 #批处理大小




#模型测试
def model_test(X_test,Y_test,userid):
        #print(model_train.get_opt())
        # 读取训练好的模型最优参数
        path = "model_parameter"+str(userid)+"/_.tar"
        with open(path) as f:
            parameters = paddle.parameters.Parameters.from_tar(f)

        out = model_building.get_net(1)

        #X_test=X_val[:2].tolist()
        num1=0
        num2=0
        for i in range(X_test.shape[0]):
            test_batch = []
            #print(i.shape)
            test_batch.append([list(X_test[i])])

            test_batch=numpy.array(test_batch)
            #print(test_batch.shape)
            probs = paddle.infer(output_layer=out, parameters=parameters, input=[test_batch], feeding=feeding)
            print(probs)
            labs = numpy.argsort(-probs)
            print("predict label is", labs[0][0],"real label is",Y_test[i])
            if labs[0][0]!=Y_test[i]:
                num1+=1

        print "Model accuracy：",(1-1.0*num1/X_test.shape[0])

#单个用户模型测试
def model_test_user(id):

    file_path_test = 'data_processed' + str(id) + '/test.pkl'

    # 读取测试集
    with open(file_path_test, "rb") as f:
        X_test = pickle.load(f)
        Y_test = pickle.load(f)
    print('参与者%d开始测试。。。'%(id+1))
    model_test(X_test,Y_test,id)


if __name__ == "__main__":
    #print(opt_id)
    model_test_user(4)
