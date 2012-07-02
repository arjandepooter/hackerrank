#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core import HackerrankSession
from multiprocessing import Queue, Process
from copy import deepcopy
from clint.textui import colored
from time import time

_start = time()

def log(msg):
    print colored.yellow("[%10.6fs]" % (time() - _start,)), msg

def run_games(uid, queue, sess):
    while not queue.empty():
        start = time()
        n = queue.get()
        if n % 6 == 0: continue
        res = sess.post('/splash/challenge.json', { 'n' : n })
        current = int(res['current'])

        while current > 0:
            res = sess.put('/splash/challenge.json', { 'move' : current % 6 })
            current = int(res['game']['current'])
            if 'solved' in res['game'] and res['game']['solved']:
                log("Process #%03d solved n = %d in " % (uid, n) + colored.red("%.2fs" % (time() - start)))

def run(start, stop, n_procs = 100, username='', password='', sess=None):
    if sess is None:
        sess = HackerrankSession()
        res = sess.login(username, password)
        log("Logged in as %s" % (colored.green(res['username'])))    
    
    q = Queue()
    for i in range(start, stop+1):
        q.put(i)
    
    processes = [Process(target=run_games, args=(uid, q, deepcopy(sess))) for uid in range(n_procs)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    log("Finished in " + colored.green(" %.2fs" % (time()-_start)))

def main(username, password, start, stop):
    run(int(start), int(stop), username, password)

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:5])
