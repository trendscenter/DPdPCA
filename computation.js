
'use strict';

module.exports = { // eslint-disable-line
  name: 'HI_dpdPCA',
  version: '0.0.1',
  cwd: __dirname,
  local: {
    type: 'cmd',
    cmd: 'python',
    args: ['./dpdpca_local.py'],
    verbose: true,
  },
  remote: {
    type: 'cmd',
    cmd: 'python',
    args: ['./dpdpca_master.py'],
    verbose: true,
  },
  plugins:['group-step'],
};
