#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
import argparse

import numpy as np
import six

import chainer
from chainer import computational_graph
from chainer import cuda
import chainer.functions as F
import chainer.links as L
from chainer import optimizers
from chainer import serializers

from data import Data
import net

parser = argparse.ArgumentParser(description='Chainer example: CS27')
parser.add_argument('--initmodel', '-m', default='', help='Initialize the model from given file')
parser.add_argument('--resume', '-r', default='', help='Resume the optimization from snapshot')
parser.add_argument('--net', '-n', choices=('simple', 'parallel'), default='simple', help='Network type')
parser.add_argument('--gpu', '-g', default=-1, type=int, help='GPU ID (negative value indicates CPU)')
args = parser.parse_args()


batchsize = 100
n_epoch = 30
n_units = 10


# Prepare dataset
print('load CS27 dataset')
data = Data()
cs27 = data.load()
cs27['data'] = cs27['data'].astype(np.float32)
cs27['target'] = cs27['target'].astype(np.int32)

N = 100000
x_train, x_test = np.split(cs27['data'], [N])
y_train, y_test = np.split(cs27['target'], [N])
N_test = y_test.size

model = L.Classifier(net.MLP(34, n_units, 2), F.softmax_cross_entropy)
xp = np
    
# Setup optimizer
optimizer = optimizers.Adam()
optimizer.setup(model)


# Init/Resume
if args.initmodel:
    print('Load model from', args.initmodel)
    serializers.load_npz(args.initmodel, model)
if args.resume:
    print('Load optimizer state from', args.resume)
    serializers.load_npz(args.resume, optimizer)

# Learning loop
for epoch in range(1, n_epoch + 1):
    print('epoch', epoch)
    
    # training 
    perm = np.random.permutation(N) #入れ替え
    sum_accuracy = 0
    sum_loss = 0
    for i in range(0, N, batchsize):
        x = chainer.Variable(xp.asarray(x_train[perm[i:i + batchsize]]))
        t = chainer.Variable(xp.asarray(y_train[perm[i:i + batchsize]]))
        # Pass the loss function (Classifier defines it) and its arguments
        optimizer.update(model, x, t)

        if epoch == 1 and i == 0:
            with open('graph.dot', 'w') as o:
                g = computational_graph.build_computational_graph(
                    (model.loss, ), remove_split=True)
                o.write(g.dump())
            print('graph generated')

        sum_loss += float(model.loss.data) * len(t.data)
        sum_accuracy += float(model.accuracy.data) * len(t.data)
            
    print('train mean loss={}, accuracy={}'.format(
        sum_loss / N, sum_accuracy / N))


    # evaluation
    sum_accuracy = 0
    sum_loss = 0
    for i in range(0, N_test, batchsize):
        x = chainer.Variable(xp.asarray(x_test[i:i + batchsize]), volatile='on')
        t = chainer.Variable(xp.asarray(y_test[i:i + batchsize]), volatile='on')
        loss = model(x, t)
        sum_loss += float(loss.data) * len(t.data)
        sum_accuracy += float(model.accuracy.data) * len(t.data)
        #print(F.softmax(model.y).data)

    print('test mean loss={}, accuracy={}'.format(
        sum_loss/ N_test, sum_accuracy / N_test))





# Save the model and the optimizer
print('save the model')
serializers.save_npz('mlp.model', model)
print('save the optimiezer')
serializers.save_npz('mlp.state', optimizer)
        


