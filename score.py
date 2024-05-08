#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2012-2019 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# AUTHORS
# Gaofeng Cheng     chenggaofeng@hccl.ioa.ac.cn     (Institute of Acoustics, Chinese Academy of Science)
# Yifan Chen        chenyifan@hccl.ioa.ac.cn        (Institute of Acoustics, Chinese Academy of Science)
# Runyan Yang       yangrunyan@hccl.ioa.ac.cn       (Institute of Acoustics, Chinese Academy of Science)
# Qingxuan Li       liqx20@mails.tsinghua.edu.cn    (Tsinghua University)


from pyannote.core import Annotation, Segment
from diarization import CSSDErrorRate, DiarizationErrorRate
from rttm_io import rttm_read
import numpy as np
from argparse import ArgumentParser
from pre_process import rttm_read_cder

def main(refs_list, hyp_list):

    CDERS = []
    for ref_rttm, hyp_rttm in zip(refs_list, hyp_list):
        ref = rttm_read_cder(ref_rttm)
        hyp = rttm_read_cder(hyp_rttm)

        CSSDER = CSSDErrorRate()
        results = []

        flag = 1
        for key, val in ref.items():
            reference = val[1]
            if key not in hyp:
                print("Warning:", key, "is missed!")
                flag = 0
                continue
            else:
                hypothesis = hyp[key][1]
                result = CSSDER(reference, hypothesis)
            #print(key, "CDER = {0:.3f}".format(result))
            results.append(result)

        if flag:
            #print("Avg CDER file : {0:.3f}".format(np.mean(results)))
            CDERS.append(np.mean(results))
        else:
            print("Avg CDER : Error!")
    print("Avg CDER : {0:.3f}".format(np.mean(CDERS)))

if __name__ == "__main__":
    main()
