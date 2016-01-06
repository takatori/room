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
        self.tree = ContextTree()

    def execute(self, event):
        '''
        @param event: ('appliance', 'method')

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
            
        return self.make_decition()

    def generate_contexts(self, episode):
        '''
        episodeの中のeventの組み合わせを羅列する

        @param episode: list
        '''
        result = []
        for i in range(0, len(episode)):
            tmp = [];
            for j in range(i, len(episode)):
                tmp.append(episode[j])
                result.append(tmp[:]) # pythonの引数は参照渡しなのでtmpを渡すと次のループで書き換えられてしまう。そのため[:]で配列をコピーして渡す
        return sorted(result, key=len)

    def update_tree(self, contexts):
        '''
        '''
        for context in contexts:
            self.tree.upsert(context)

    
    def opposite(self, event):
        '''
        入力されたイベント(家電操作・入退室)と逆のイベントを返す
        
        ex: ('viera', 'on') -> ('viera', 'off')
          :  A -> a
        '''
        #return event.swapcase() # 大文字小文字を入れ替える
        return (event[0], 'off') if event[1] == 'on' else (event[0], 'on') # on と off の入れ替え



    def calc_probability(self, event, node):
        '''
        入力されたイベントが過去の状態(tree)とcontextの下で起こる確率を計算する

        '''
        if not isinstance(node, Node): return 0
        
        occurrence_c  = node.occurrence # total occurrence of episodes of k-1 length
        ck = self.tree.search_child(node.children, event)
        occurrence_ck = 0 if ck == None else ck.occurrence # total occurrence φ event after exploring the current episode

        child_nodes_occurrence = sum([c.occurrence for c in node.children])
        num_c0 = node.occurrence - child_nodes_occurrence # total number of null outcomes after exploring the current episode

        if occurrence_c == 0:
            return occurrence_ck / child_nodes_occurrence
        else:
            return (occurrence_ck / occurrence_c) + (num_c0 / occurrence_c) * self.calc_probability(event, node.parent) # Pk = ck/c + ce/c * Pk-1



    def make_decition(self):
        '''
        
        '''
        events = [c.event for c in self.tree.root.children] # アトミックなイベント
        context = self.window
        result = [(e, self.calc_probability(e, self.tree.trace(self.tree.root, context))) for e in events] # 全てのイベントに対して現在のコンテキストの後に発生する確率を計算する
        return result


class ContextTree(object):
    '''
    過去の履歴を保持するためのツリー

    '''

    def __init__(self):
        self.root = Node(parent=None, event='Root', occurrence=0)

        
    def upsert(self, context):
        '''
        contextが存在していればoccurenceをインクリメント
        存在していなければtreeにnodeを追加

        '''
        target = self.trace(self.root, context)

        if isinstance(target, Node):
            target.occurrence += 1 # update
        else:
            current_node = target[0] 
            new_node = Node(parent=current_node, event=target[1])
            current_node.children.append(new_node) # insert
        
    def trace(self, node, context):
        '''
        木をたどる

        @param context: list ex: [('viera', 'on'), ('light', 'off')]
        '''
        if len(context) == 0: return node # treeの最後まで辿れた

        child = self.search_child(node.children, context[0])
        if child:
            return self.trace(child, context[1:]) # 次のノードを探索
        else:
            # contextが残っているが、次のノードが見つからなかった場合
            # 短いcontextから追加していくので、
            # nodeが見つからないcontextは必ず要素が一つになるはずなのでcontext[0]としている
            # 辿れた一番最後のnodeと残りのevent(contextシークエンスの最後)を返す
            return (node, context[0])
            

    def search_child(self, children, event):
        '''
        子ノードに指定されたイベントを持つノードがあるかを判定する
        '''
        for node in children:
            if node == event: return node
        return None
    

    def print_tree(self, node, line=[], depth=0):
        '''
        木構造を表示する
        
        '''
        if len(node.children) == 0:
            print(' ' * (depth - len(line)) * 9, end='')
            for n in line:
                print('({0},{1:>3})'.format(n.event, n.occurrence), end='')
                print('--', end='')
            print(' {0}'.format(depth))
            line[:] = []
            return
        
        for c in node.children:
            line.append(c)
            depth += 1
            self.print_tree(c, line, depth)
            depth -= 1

            
class Node(object):
    '''

    '''
    def __init__(self, parent, event, occurrence=1):
        self.parent = parent 
        self.children = [] 
        self.event = event
        self.occurrence = occurrence # 発生回数
        

    def __eq__(self, event):
        '''
        if self.event[0] == event:
            return True
        else:
            return False
        '''
        if event and self.event[0] == event[0] and self.event[1] == event[1]:
            return True
        else:
            return False

        
if __name__ == "__main__":
    speed = SPEED()
    #input = ['A', 'B', 'b', 'D', 'C', 'c', 'a', 'B', 'C', 'b', 'd', 'c', 'A', 'D', 'a', 'B', 'A', 'd', 'a', 'b']
    # A -> viera on
    # B -> light
    # C -> fan
    # D -> tv
    input = [('viera', 'on'),
             ('light', 'on'),
             ('light', 'off'),
             ('tv', 'on'),
             ('fan', 'on'),
             ('fan', 'off'),
             ('viera', 'off'),
             ('light', 'on'),
             ('fan', 'on'),
             ('light', 'off'),
             ('tv', 'off'),
             ('fan', 'off'),
             ('viera', 'on'),
             ('tv','on'),
             ('viera','off'),
             ('light','on'),
             ('viera','on'),
             ('tv','off'),
             ('viera','off'),
             ('light','off')]
    for i in input:
        speed.execute(i)

    speed.tree.print_tree(speed.tree.root)
    print(speed.calc_probability(('light', 'off'), speed.tree.trace(speed.tree.root, [('viera', 'on'), ('tv', 'off'), ('viera', 'off')])))
    print(speed.make_decition())
