#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 13:54:42 2017

@author: koolok
"""

import random
from multiprocessing import Pool, cpu_count, Process, Manager
from distanceC import distance, distance_multi
from editdistance import eval as editdistance

def analyse(word,base,label) :
    label_mini = -1
    mini = -1

    for i in range(len(base)) :
        w = base[i]
            
        dist = distance(word,w)
#        dist = editdistance.eval(word,w)
#        print(dist)
        if dist < mini or mini < 0 :
            mini = dist
            label_mini = label[i]
    return label_mini  

def analyse_multi(word,base,label,k=1) :
    if len(base) == 0 :
        return -1
    if len(base) == 1 :
        return label[0]
        
    pool = Pool()
    
    all_distance = pool.starmap_async(distance_multi, zip(base,[word]*len(base),label)).get()
    
    pool.close()

#    all_distance = dict(zip(label, all_distance))
#    
#    all_distance = sorted(label, key=all_distance.__getitem__)

    all_distance = sorted(all_distance, key=lambda tup: tup[1])
    
    votes = [0]*10
    
    for i in range(k):
        votes[all_distance[i][0]] +=1
                
    return votes.index(max(votes))
    

def analyse_triangle(word,base,label,distance_matrix) :
    if len(base) == 0 :
        return -1
    if len(base) == 1 :
        return label[0]
    
    pool = list(range(len(base)))
    
    w1 = random.choice(pool)
    pool.remove(w1)
    
    w2 = random.choice(pool)
    pool.remove(w2)

#    dist_w1 = editdistance.eval(base[w1],word)
#    dist_w2 = editdistance.eval(base[w2],word)
    dist_w1 = distance(base[w1],word)
    dist_w2 = distance(base[w2],word)
    
    while (pool != []) :
        if dist_w1 > dist_w2 :
            for i in pool :
                if distance_matrix[i][w1] < dist_w1 - dist_w2 or distance_matrix[i][w1] > dist_w1 + dist_w2 :
                    pool.remove(i)
                    
            if pool == [] :
                break
            w1 = random.choice(pool)
            pool.remove(w1)
            dist_w1 = distance(base[w1],word)
#            dist_w1 = editdistance.eval(base[w1],word)
                    
        else :
            for i in pool :
                if distance_matrix[i][w1] < dist_w2 - dist_w1 or distance_matrix[i][w1] > dist_w2 + dist_w1 :
                    pool.remove(i)
            
            if pool == [] :
                break
            w2 = random.choice(pool)
            pool.remove(w2)
            dist_w2 = distance(base[w2],word)
#            dist_w2 = editdistance.eval(base[w2],word)
            
    if (dist_w1 < dist_w2) :
        return label[w1]
    else :
        return label[w2]
    
    

def analyse_triangle_knn_multi(word,base,label,distance_matrix,k) :
#    q = Manager().Queue()
#    
#    cpu = cpu_count()
#    
#    p_list = []
#    
#    for i in range(cpu) :        
#        p = Process(target=analyse_triangle_knn_queue, args=(word,base,label,distance_matrix,k,q))
#        p.start()
#        p_list.append(p)
#        
#    result = q.get()
#    
#    for p in p_list :
#        p.terminate()

#    cpu = cpu_count()
#        
#    pool = Pool()
#    
#    result = pool.starmap_async(analyse_triangle_knn, [(word,base,label,distance_matrix,k)]*cpu).get()
#    
#    pool.close()

    cpu = cpu_count()
    
    pool = Pool()
    
    results = []
    
    for i in range(cpu):
        result = pool.apply_async(analyse_triangle_knn, (word,base,label,distance_matrix,k))
        results.append(result)
        
    while True :
        for result in results :
            if result.ready() :
                pool.terminate()
                return result.get()
        
    

    
def analyse_triangle_knn_queue(word,base,label,distance_matrix,k,q) :
    if len(base) == 0 :
        q.put(-1)
    if len(base) == 1 :
        q.put(label[0])
    
    k += 1
    
    sv_k = k
    
    if k == 1:
        k = 2
    
    pool = list(range(len(base)))
    
    w_list = {}
    
    for i in range(k) :
        if pool == [] :
            break
        w = random.choice(pool)
        pool.remove(w)
        
        w_list[distance(base[w],word)] = w
        
#    print(w_list)
        
    while pool != [] :
        
        sorted_keys = sorted(w_list)
        
        maxi1 = sorted_keys[-1]
        maxi2 = sorted_keys[-2]
        
        for i in pool :
            if distance_matrix[i][w_list[maxi1]] < maxi1 - maxi2 or distance_matrix[i][w_list[maxi1]] > maxi1 + maxi2 :
                pool.remove(i)
                
        del w_list[maxi1]
        if pool == [] :
            break
        
        w = random.choice(pool)
        pool.remove(w)
        
        d = distance(base[w],word)
        
        while d in w_list and pool != [] :
            w = random.choice(pool)
            pool.remove(w)
           
            d = distance(base[w],word)

            
        if pool == [] :
            break
        
        w_list[d] = w
    
    if sv_k == 1 :
        for w in w_list :
            q.put(label[w_list[w]])
        
    
    votes = [0]*10
    
    
    for w in w_list:
        votes[label[w_list[w]]] +=1
                
    q.put(votes.index(max(votes)))

    
def analyse_triangle_knn(word,base,label,distance_matrix,k) :
    if len(base) == 0 :
        return -1
    if len(base) == 1 :
        return label[0]
    
    k += 1
    
    sv_k = k
    
    if k == 1:
        k = 2
    
    pool = list(range(len(base)))
    
    w_list = {}
    
    for i in range(k) :
        if pool == [] :
            break
        w = random.choice(pool)
        pool.remove(w)
        
        w_list[distance(base[w],word)] = w
        
#    print(w_list)
        
    while pool != [] :
        
        sorted_keys = sorted(w_list)
        
        maxi1 = sorted_keys[-1]
        maxi2 = sorted_keys[-2]
        
        for i in pool :
            if distance_matrix[i][w_list[maxi1]] <= maxi1 - maxi2 or distance_matrix[i][w_list[maxi1]] >= maxi1 + maxi2 :
                pool.remove(i)
                
        del w_list[maxi1]
        if pool == [] :
            break
        
        w = random.choice(pool)
        pool.remove(w)
        
        d = distance(base[w],word)
        
        while d in w_list and pool != [] :
            w = random.choice(pool)
            pool.remove(w)
           
            d = distance(base[w],word)
            

        if pool == [] :
            break
        
        w_list[d] = w
    
    if sv_k == 1 :
        for w in w_list :
            return label[w_list[w]]
        
    
    votes = [0]*10
    
    
    for w in w_list:
        votes[label[w_list[w]]] +=1
                
    return votes.index(max(votes))
    


#==============================================================================
# Same functions but with the module editdistance
#==============================================================================

def edit_analyse(word,base,label) :
    label_mini = -1
    mini = -1

    for i in range(len(base)) :
        w = base[i]
            
        dist = editdistance(word,w)
#        dist = editdistance.eval(word,w)
#        print(dist)
        if dist < mini or mini < 0 :
            mini = dist
            label_mini = label[i]
    return label_mini  

def edit_analyse_multi(word,base,label,k=1) :
    if len(base) == 0 :
        return -1
    if len(base) == 1 :
        return label[0]
        
    pool = Pool()
    
    all_distance = pool.starmap_async(distance, zip(base,[word]*len(base))).get()

    all_distance = dict(zip(label, all_distance))
    
    all_distance = sorted(label, key=all_distance.__getitem__)
    
    votes = [0]*10
    
    for i in range(k):
        votes[all_distance[i]] +=1
                
    return votes.index(max(votes))
    

def edit_analyse_triangle(word,base,label,distance_matrix) :
    if len(base) == 0 :
        return -1
    if len(base) == 1 :
        return label[0]
    
    pool = list(range(len(base)))
    
    w1 = random.choice(pool)
    pool.remove(w1)
    
    w2 = random.choice(pool)
    pool.remove(w2)

#    dist_w1 = editdistance.eval(base[w1],word)
#    dist_w2 = editdistance.eval(base[w2],word)
    dist_w1 = editdistance(base[w1],word)
    dist_w2 = editdistance(base[w2],word)
    
    while (pool != []) :
        if dist_w1 > dist_w2 :
            for i in pool :
                if distance_matrix[i][w1] < dist_w1 - dist_w2 or distance_matrix[i][w1] > dist_w1 + dist_w2 :
                    pool.remove(i)
                    
            if pool == [] :
                break
            w1 = random.choice(pool)
            pool.remove(w1)
            dist_w1 = editdistance(base[w1],word)
#            dist_w1 = editdistance.eval(base[w1],word)
                    
        else :
            for i in pool :
                if distance_matrix[i][w1] < dist_w2 - dist_w1 or distance_matrix[i][w1] > dist_w2 + dist_w1 :
                    pool.remove(i)
            
            if pool == [] :
                break
            w2 = random.choice(pool)
            pool.remove(w2)
            dist_w2 = editdistance(base[w2],word)
#            dist_w2 = editdistance.eval(base[w2],word)
            
    if (dist_w1 < dist_w2) :
        return label[w1]
    else :
        return label[w2]
    
def edit_analyse_triangle_knn_multi(word,base,label,distance_matrix,k) :
    q = Manager().Queue()
    
    cpu = cpu_count()
    
    p_list = []
    
    for i in range(cpu) :        
        p = Process(target=edit_analyse_triangle_knn_queue, args=(word,base,label,distance_matrix,k,q))
        p.start()
        p_list.append(p)
        
    result = q.get()
    
    for p in p_list :
        p.terminate()
        
    return result
    
    

    
def edit_analyse_triangle_knn_queue(word,base,label,distance_matrix,k,q) :
    if len(base) == 0 :
        q.put(-1)
    if len(base) == 1 :
        q.put(label[0])
    
    k += 1
    
    sv_k = k
    
    if k == 1:
        k = 2
    
    pool = list(range(len(base)))
    
    w_list = {}
    
    for i in range(k) :
        if pool == [] :
            break
        w = random.choice(pool)
        pool.remove(w)
        
        w_list[editdistance(base[w],word)] = w
        
#    print(w_list)
        
    while pool != [] :
        
        sorted_keys = sorted(w_list)
        
        maxi1 = sorted_keys[-1]
        maxi2 = sorted_keys[-2]
        
        for i in pool :
            if distance_matrix[i][w_list[maxi1]] < maxi1 - maxi2 or distance_matrix[i][w_list[maxi1]] > maxi1 + maxi2 :
                pool.remove(i)
                
        del w_list[maxi1]
        if pool == [] :
            break
        
        w = random.choice(pool)
        pool.remove(w)
        
        d = editdistance(base[w],word)
        
        while d in w_list and pool != [] :
            w = random.choice(pool)
            pool.remove(w)
           
            d = editdistance(base[w],word)

            
        if pool == [] :
            break
        
        w_list[d] = w
    
    if sv_k == 1 :
        for w in w_list :
            q.put(label[w_list[w]])
        
    
    votes = [0]*10
    
    
    for w in w_list:
        votes[label[w_list[w]]] +=1
                
    q.put(votes.index(max(votes)))

def edit_analyse_triangle_knn(word,base,label,distance_matrix,k) :
    if len(base) == 0 :
        return -1
    if len(base) == 1 :
        return label[0]
    
    k += 1
    
    sv_k = k
    
    if k == 1:
        k = 2
    
    pool = list(range(len(base)))
    
    w_list = {}
    
    for i in range(k) :
        if pool == [] :
            break
        w = random.choice(pool)
        pool.remove(w)
        
        w_list[editdistance(base[w],word)] = w
        
#    print(w_list)
        
    while pool != [] :
        
        sorted_keys = sorted(w_list)
        print(len(pool))
        
        maxi1 = sorted_keys[-1]
        maxi2 = sorted_keys[-2]
        
        for i in pool :
            if distance_matrix[i][w_list[maxi1]] <= maxi1 - maxi2 or distance_matrix[i][w_list[maxi1]] >= maxi1 + maxi2 :
                pool.remove(i)
                
        del w_list[maxi1]
        if pool == [] :
            break
        
        w = random.choice(pool)
        pool.remove(w)
        
        d = editdistance(base[w],word)
        
        while d in w_list and pool != [] :
            w = random.choice(pool)
            pool.remove(w)
           
            d = editdistance(base[w],word)
            

        if pool == [] :
            break
        
        w_list[d] = w
    
    if sv_k == 1 :
        for w in w_list :
            return label[w_list[w]]
        
    
    votes = [0]*10
    
    
    for w in w_list:
        votes[label[w_list[w]]] +=1
                
    return votes.index(max(votes))
