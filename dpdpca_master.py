import json;
import argparse
from os import listdir
from os.path import isfile, join
import sys
import numpy as np
#import sklearn
#import sklearn.linear_model


parser = argparse.ArgumentParser(description='read beta vector from single site and do beta averaging!')
parser.add_argument('--run', type=str,  help='grab coinstac args')
args = parser.parse_args()
args.run = json.loads(args.run)

#inspect what args were passed
#runInputs = json.dumps(args.run, sort_keys=True, indent=4, separators=(',', ': '))
#sys.stderr.write(runInputs + "\n")

#if 'remoteResult' in args.run and \
#    'data' in args.run['remoteResult'] and \
#    username in args.run['remoteResult']['data']:
#    sys.exit(0); # no-op!  we already contributed our data



user_results = args.run['userResults']

n_site = len(user_results)

P = np.array([])
en_sites_true = []
C = 0
C_central = 0
for i in range(0,n_site):
    en_sites_true.append(user_results[i]['data']['en'])
    Ps = np.array(user_results[i]['data']['P'])
    C_central += np.dot(Ps, Ps.T)
#    P = np.hstack([P, Ps]) if P.size else Ps
    C = C + np.array(user_results[i]['data']['C'])

# consensus subspace    
K = 4
Ua, Sa, Va = np.linalg.svd(C_central)
Uak = Ua[:, :K]
var_cons = np.trace(np.dot(Uak.T, np.dot(C, Uak)))
var_true = sum(en_sites_true)

sys.stderr.write("Done! consensus subspace energy : {}".format(var_cons)+"\n")
sys.stderr.write("Done! true subspace energy : {}".format(var_true)+"\n")
computationOutput = json.dumps({'complete': True, 'var_cons': var_cons, 'var_true': var_true}, sort_keys=True, indent=4, separators=(',', ': '))

#sys.stderr.write("Done! consensus subspace energy : {}".format(var_true)+"\n")
#computationOutput = json.dumps({'complete': True, 'var_true': var_true}, sort_keys=True, indent=4, separators=(',', ': '))

# preview output data
#sys.stderr.write(computationOutput + "\n")

# send results
sys.stdout.write(computationOutput)

