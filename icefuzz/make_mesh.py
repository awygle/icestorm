#!/usr/bin/env python3

from fuzzconfig import *
import numpy as np
import os

os.system("rm -rf work_mesh")
os.mkdir("work_mesh")

for idx in range(num):
    with open("work_mesh/mesh_%02d.v" % idx, "w") as f:
        if os.getenv('ICE384PINS'):
            print("module top(input [9:0] a, output [17:0] y);", file=f)
        else:
            print("module top(input [39:0] a, output [39:0] y);", file=f)
        print("  assign y = a;", file=f)
        print("endmodule", file=f)
    with open("work_mesh/mesh_%02d.pcf" % idx, "w") as f:
        p = np.random.permutation(pins)
        if os.getenv('ICE384PINS'): r = 18
        else: r = 40
        for i in range(r):
            print("set_io a[%d] %s" % (i, p[i]), file=f)
        for i in range(r):
            print("set_io y[%d] %s" % (i, p[r+i]), file=f)

with open("work_mesh/Makefile", "w") as f:
    print("all: %s" % " ".join(["mesh_%02d.bin" % i for i in range(num)]), file=f)
    for i in range(num):
        print("mesh_%02d.bin:" % i, file=f)
        print("\t-bash ../icecube.sh mesh_%02d > mesh_%02d.log 2>&1 && rm -rf mesh_%02d.tmp || tail mesh_%02d.log" % (i, i, i, i), file=f)

