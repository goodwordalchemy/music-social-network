const webpack = require('webpack');

const path = require('path');

module.exports = {
    entry: './static/js/src/index.js',
    output: {
        filename: 'bundle.js',
        path: path.join(__dirname, 'static/js/dist/')
    },
    module: {
        loaders: [
            {
                loader: 'babel-loader',

                exclude: /(node_modules|bower_components)/,

                query: {
                    presets: ['es2015', 'react']
                }
            }
        ]
    }
};
