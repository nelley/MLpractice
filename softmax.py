# -*- coding=utf-8 -*-

import numpy as np
import pdb

pdb.set_trace()
a = np.array([0.3, 2.9, 4.0])


def softmax_imp(a):
    # 入力値の中で最大値を取得
    c = np.max(a)
    # オーバーフロー対策として、最大値cを引く。こうすることで値が小さくなる
    exp_a = np.exp(a - c)
    print exp_a
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y

print(softmax_imp(a))
