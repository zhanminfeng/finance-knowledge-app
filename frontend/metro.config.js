const { getDefaultConfig } = require('@expo/metro-config');

const config = {
  resolver: {
    sourceExts: ['jsx', 'js', 'ts', 'tsx', 'json'],
    assetExts: ['png', 'jpg', 'jpeg', 'gif', 'webp', 'ttf', 'otf', 'woff', 'woff2'],
  },
  transformer: {
    getTransformOptions: async () => ({
      transform: {
        experimentalImportSupport: false,
        inlineRequires: true,
      },
    }),
    babelTransformerPath: require.resolve('react-native-svg-transformer'),
  },
};

module.exports = getDefaultConfig(__dirname, config); 