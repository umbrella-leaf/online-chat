const { defineConfig } = require('@vue/cli-service')
const Timestamp = new Date().getTime();

module.exports = defineConfig({
  transpileDependencies: true,
  runtimeCompiler: true,

  configureWebpack: {
    //每次打包后生成的js携带时间�?
    output: {
      filename: `[name].${Timestamp}.js`,
      chunkFilename: `[name].${Timestamp}.js`,
    },
  },
  css: {
    loaderOptions: {
      //这只主题样式，修改此文件后需要重新启�?
      less: {
        lessOptions: {
          modifyVars: {
            //这是配置css主题�?
            "primary-color": "#007AFF",
          },
          javascriptEnabled: true,
        },
      },
    },
    // 每次打包后生成的css携带时间�?
    extract: {
      filename: `css/[name].${Timestamp}.css`,
      chunkFilename: `css/[name].${Timestamp}.css`,
    },
  },
})
