const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const webpack = require('webpack')

const hash = Math.random().toString(36).substring(7, 13);

const scriptFileName = `app.bundle_${hash}.js`
const styleSheetName = `style_${hash}.css`

module.exports = env => {
  return {
    entry: {
      [scriptFileName]: './src/index.js'
    },
    output: {
      filename: '[name]',
      path: path.resolve(__dirname, '../public'),
      publicPath: '/'
    },
    devtool: env.NODE_ENV === 'production' ? false : 'inline-source-map',
    devServer: {
      contentBase: '../public',
      hot: true,
      port: 3000,
      historyApiFallback: {
        index: '/',
      }
    },
    plugins: [
      new CleanWebpackPlugin(['../public']),
      new HtmlWebpackPlugin({
        inject: false,
        template: './src/index.ejs',
        scriptFileName: scriptFileName,
        styleSheetName: styleSheetName
      }),
      new webpack.HotModuleReplacementPlugin(),
      new ExtractTextPlugin(`../public/style_${hash}.css`),
      new CopyWebpackPlugin([
        {from: 'src/manifest.json', to:'../public/manifest.json'},
        {from: 'src/assets/icons', to:'../public/assets'},
        {from: 'src/serviceWorker.js', to: '../public/serviceWorker.js'}
      ])
    ],
    externals: {
      'cheerio': 'window',
      'react/lib/ExecutionEnvironment': true,
      'react/lib/ReactContext': true,
    },
    module: {
      rules: [
        {
          test: /\.scss$/,
          use: ExtractTextPlugin.extract({
            fallback: "style-loader",
            use: ["css-loader", "sass-loader"]
          })
        },
        {
          test: /\.(png|svg|jpg|gif)$/,
          use: [
            'file-loader'
          ]
        },
        {
          test: /\.(woff|woff2|eot|ttf|otf|html)$/,
          use: [
            'file-loader'
          ]
        },
        {
          test: /\.(js|jsx)$/,
          use: 'babel-loader',
          exclude: /node_modules/
        }
      ],
    }
  }
}
