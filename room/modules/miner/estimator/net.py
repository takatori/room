#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chainer
import chainer.functions as F
import chainer.links as L

class MLP(chainer.Chain):
    
    def __init__(self, n_in, n_units, n_out):
        super(MLP, self).__init__(
            l1=L.Linear(n_in, n_units),
            l2=L.Linear(n_units, n_units),
            l3=L.Linear(n_units, n_out),
        )


    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        return self.l3(h2) 


class MLPParallel(chainer.Chain):

    def __init__(self, n_in, n_units, n_out):
        super(MLPParallel, self).__init__(
            first0=MLP(n_in, n_units // 2, n_units).to_gpu(0),
            first1=MLP(n_in, n_units // 2, n_units).to_gpu(1),
            second0=MLP(n_units, n_units // 2, n_out).to_gpu(0),
            second1=MLP(n_units, n_units // 2, n_out).to_gpu(1),
        )


    def __call__(self, x):
        # assume x is on GPU 0
        x1 = F.copy(x, 1)

        z0 = self.first0(x)
        z1 = self.first1(x1)


        # sync
        h0 = z0 + F.copy(z1, 0)
        h1 = z1 + F.copy(z0, 1)


        y0 = self.second0(F.relu(h0))
        y1 = self.second1(F.relu(h1))

        # sync
        y = y0 + F.copy(y1, 0)

        return y
