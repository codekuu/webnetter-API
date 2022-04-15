module.exports = {
    outputDir: "dist",
    assetsDir: "static",

  chainWebpack: config => {
    config.module
      .rule('eslint')
      .use('eslint-loader')
      .options({
        fix: true,
    });
  },

  productionSourceMap: false,

  devServer: {
    overlay: {
      warnings: true,
      errors: true
    }
  },
}

