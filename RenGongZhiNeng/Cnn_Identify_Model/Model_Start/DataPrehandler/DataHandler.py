from Cnn_Identify_Model.Model_Start import Config
from sklearn.preprocessing import Normalizer
import pandas as pd
import numpy as np
class handlerData():
    def __init__(self):
        self.config = Config.config()
        # 训练集
        self.train_data = pd.read_csv('/home/mao/Mao/Documents/MyDataTrain1.csv', header=None)
        # 测试集
        self.test_data = pd.read_csv('/home/mao/Mao/Documents/MyDataTest1.csv', header=None)
        #return result
        train, test, train_lb, test_lb = self.handledata()
        self.train_lb, self.test_lb, self.trainx, self.testy = self.guiyihua(train, test, train_lb, test_lb)

    def handledata(self):
        # 训练集训练部分
        train = self.train_data.iloc[:, 0:self.config.data]
        # 训练集标签
        train_lb = self.train_data.iloc[:, self.config.label]

        # 测试集测试部分
        test = self.test_data.iloc[:, 0:self.config.data]
        # 测试集标签
        test_lb = self.test_data.iloc[:, self.config.label]

        return train, test, train_lb, test_lb


    def guiyihua(self, train, test, train_lb, test_lb):
        # 归一化训练集和测试集
        scaler = Normalizer().fit(train)

        # 训练集的归一化操作
        x_train = scaler.transform(train)

        # 测试集的归一化操作
        scaler = Normalizer().fit(test)
        x_test = scaler.transform(test)

        x = np.expand_dims(x_train, axis=2)
        y = np.expand_dims(x_test, axis=2)

        # 标签数组化
        tr_lb = np.reshape(train_lb, self.config.trainnum)
        te_lb = np.reshape(test_lb, self.config.testnum)
        return tr_lb, te_lb, x, y
