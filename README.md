# dPCA
This repository contains the differentially-private distributed PCA code written for the old coinstac simulator (v2.3). It contains the following files:
1. dpdpca_local.py - for computing the local PCA on local data and sending the differentially private proxy data matrix to the master.
2. dpdpca_master.py - for aggregation of the differentially-private proxy data matrices sent by local sites and releasing the top-K principal components
3. computation.js - computation specification JavaScript file
4. declaration.js - declaration file specifying the local site names,  JavaScript file
