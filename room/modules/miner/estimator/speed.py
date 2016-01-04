#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import defaultdict

class SPEED(object):
    '''
    Markov chain

    '''

    def __init__(self):
        self.window = []
        self.max_episode_length = 1
        self.tree = defaultdict(int)
        
    def execute(self, event):
        '''
        '''
        self.window.append(event) # windowに追加
        e = self.opposite(event) # 逆のイベントを取得

        for i in range(0, len(self.window)-1): # windowの前から走査
            if self.window[i] == e: # 入力されたイベントと逆のイベントがあれば
                episode = self.window[i:] # 一連のエピソードを取得 ex: deABca -> ABca
      
                if len(episode) > self.max_episode_length: # エピソード長がmax_episode_lengthより長ければ更新
                    self.max_episode_length = len(episode)

                self.window = self.window[-self.max_episode_length:] # windowを更新
                self.update_tree(self.generate_contexts(episode)) # treeを更新
                break
            
        #print(self.max_episode_length, str(self.window))
        print(self.tree)

    def generate_contexts(self, episode):
        '''
        episodeの中のeventの組み合わせを羅列する
        '''
        result = []
        
        for i in range(0, len(episode)):
            tmp = '';
            for j in range(i, len(episode)):
                tmp += episode[j]
                result.append(tmp)
                
        return result

    
    def update_tree(self, contexts):
        for c in contexts:
            self.tree[c]  += 1

    
    def opposite(self, event):
        '''
        入力されたイベント(家電操作・入退室)と逆のイベントを返す
        
        ex: ('viera', 'on') -> ('viera', 'off')
          :  A -> a
        '''
        return event.swapcase() # 大文字小文字を入れ替える


    def calc_probability(self, event, context):
        '''
        入力されたイベントが現在の状態の後に起こる確率を計算する

        '''
        # print(event, context) # DEBUG
        
        occurrence_c  = self.tree[context] # total occurrence of episodes of k-1 length
        ck = context + event 
        occurrence_ck = self.tree[ck] # total occurrence φ event after exploring the current episode

        pattern = r"^{0}.$".format(context) # contextプラス一文字にマッチする ex: Ab -> Aba, Abb...
        child_nodes = [key for key in self.tree.keys() if re.match(pattern, key)] # 子ノード
        child_nodes_occurrence = sum([self.tree[node] for node in child_nodes])
        num_c0 = self.tree[context] - child_nodes_occurrence # total number of null outcomes after exploring the current episode

        # print(ce) # DEBUG        
        # print(num_c, num_ck, num_ce) # DEBUG
        # print('-------------------') # DEBUG

        if occurrence_c == 0:
            return occurrence_ck / child_nodes_occurrence
        else:
            return (occurrence_ck / occurrence_c) + (num_c0 / occurrence_c) * self.calc_probability(event, context[:-1])
            

    def make_decition(self):
        pass


if __name__ == "__main__":
    speed = SPEED()
    input = ['A', 'B', 'b', 'D', 'C', 'c', 'a', 'B', 'C', 'b', 'd', 'c', 'A', 'D', 'a', 'B', 'A', 'd', 'a', 'b']

    for i in input:
        speed.execute(i)
    
    #speed.calc_probability('b', ''.join(speed.window))
    print(speed.calc_probability('d', 'Ada'))
