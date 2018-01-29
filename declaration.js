
const path = require('path');

module.exports = {
  computationPath: path.resolve(
    __dirname,
    'computation.js'
  ),
  local: [{
    dirs: ['site0'],
  }, {
    dirs: ['site1'],
  }, {
    dirs: ['site2'],
  }, {
    dirs: ['site3'],
  }, {
    dirs: ['site4'],
  }],
  verbose: true,
};
