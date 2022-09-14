from src import *

import argparse
import subprocess
import time


def parse_args():
    parser = argparse.ArgumentParser(description="Transmission through a black-box channel simulator",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog="To promote efficient communication schemes, transmissions are limited to 100 a samples.")

    parser.add_argument('--srv', action='store_true',
                        help='If set, it runs the program on the EPFL server (requires VPN)')
    parser.add_argument('--n', type=int, default=1,
                        help='Number of times to test the transmission')
    parser.add_argument('--m', type=int, default=64,
                        help='Number of points in the qam constellation')
    parser.add_argument('--k', type=int, default=9,
                        help='Number of points used to estimate Theta')
    parser.add_argument('--lim', type=float, default=0.9,
                        help='Limit of the qam constellation')
    parser.add_argument('--init_file', type=str, default='initial.txt',
                        help='.txt file containing the text to transmit.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    
    n = args.n
    qam = qam.QAM(args.m, args.k, args.lim)
    cmd = " --srv_hostname=iscsrv72.epfl.ch --srv_port=80" if args.srv else ""

    utils.encode(qam, args.init_file)

    tot = 0
    nb0 = 0
    nberr = 0
    for i in range(n):
        subprocess.call("python src/client.py --input_file=input.txt --output_file=output.txt" + cmd, shell=True)
        
        utils.decode(qam)

        nberr = utils.compute_score(args.init_file)
        tot += nberr

        if (nberr == 0):
            nb0 += 1
        
        if args.srv and n > 1:
            time.sleep(30)

    if n > 1:
        print("Average difference is : ", tot/n)
        print("Number of perfect : ", nb0)
