import json;
import argparse
from os import listdir
from os.path import isfile, join
import sys
import numpy as np

def dp_pca_ag ( data, epsilon=1.0, delta=0.1 ):
    '''
    This function provides a differentially-private estimate using Analyze Gauss method
    of the second moment matrix of the data

    Input:

      data = data matrix, samples are in columns
      epsilon, delta = privacy parameters
      hat_A = (\epsilon, \delta)-differentially-private estimate of A = data*data'

    Example:

      >>> import numpy as np
      >>> data = np.random.rand(10)
      >>> hat_A = dp_pca_ag ( data, 1.0, 0.1 )
      [[ 1.54704321  2.58597112  1.05587101  0.97735922  0.03357301]
       [ 2.58597112  4.86708836  1.90975259  1.41030773  0.06620355]
       [ 1.05587101  1.90975259  1.45824498 -0.12231379 -0.83844168]
       [ 0.97735922  1.41030773 -0.12231379  1.47130207  0.91925544]
       [ 0.03357301  0.06620355 -0.83844168  0.91925544  1.06881321]]

    '''

    import numpy as np

    if any( np.diag( np.dot( data.transpose(), data ) ) ) > 1:
        print('ERROR: Each column in the data matrix should have 2-norm bounded in [0,1].')
        return
    elif epsilon < 0.0:
        print('ERROR: Epsilon should be positive.')
        return
    elif delta < 0.0 or delta > 1.0:
        print('ERROR: Delta should be bounded in [0,1].')
        return
    else:
        m, N = data.shape
        A = (1.0 / N) * np.dot( data, data.transpose() )
        D = ( 1.0 / (N * epsilon) ) * np.sqrt( 2.0 * np.log( 1.25 / delta ) )
        temp = np.random.normal( 0, D, (m, m))
        temp2 = np.triu( temp )
        temp3 = temp2.transpose()
        temp4 = np.tril(temp3, -1)
        E = temp2 + temp4
        hat_A = A + E
        return hat_A


parser = argparse.ArgumentParser(description='help read in my data from my local machine!')
parser.add_argument('--run', type=str,  help='grab coinstac args')
args = parser.parse_args()
args.run = json.loads(args.run)

username = args.run['username']

# inspect what args were passed
# runInputs = json.dumps(args.run, sort_keys=True, indent=4, separators=(',', ': '))
# sys.stderr.write(runInputs + "\n")

if 'remoteResult' in args.run and \
    'data' in args.run['remoteResult'] and \
    username in args.run['remoteResult']['data']:
    sys.exit(0); # no-op!  we already contributed our data

passedDir = args.run['userData']['dirs'][0]
sys.stderr.write("reading files from dir: " + passedDir)

files = [f for f in listdir(passedDir) if isfile(join(passedDir, f))]

# allFileData = {}

for f in files:
    
    X = np.load(join(passedDir,f))
    d, n = X.shape
    K = 8
    epsilon = 1.0
    delta = 0.01
    C = (1.0 / n) * np.dot( X, X.T ) # true second-moment matrix
    C_hat = dp_pca_ag ( X, epsilon, delta ) # differentially-private second-moment matrix
    U, S, V = np.linalg.svd(C_hat)
    Uk = U[:, :K]
    Sk = np.diag(S)[:K, :K]
    P = np.dot(Uk, np.sqrt(Sk))
    en = np.trace(np.dot(Uk.T, np.dot(C, Uk))) # this is the true energy in the true matrix C

computationOutput = json.dumps({'P': P.tolist(), 'en': en, 'C': C_hat.tolist()}, sort_keys=True, indent=4, separators=(',', ': '))
#computationOutput = json.dumps({'en': en}, sort_keys=True, indent=4, separators=(',', ': '))

# preview output data
# sys.stderr.write(computationOutput + "\n")

# send results
sys.stdout.write(computationOutput)

