#!/usr/bin/env python
# -*- coding: utf-8 -*-
from splash import *
from core import HackerrankSession

def main(start, stop, username, email, password):
    current = int(start)
    while current <= int(stop):
        sess = HackerrankSession()
        sess.signup(username.format(uid=current), email.format(uid=current), password)
        run(6, 2560, sess=sess, n_procs=200)
        current += 1
    

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
