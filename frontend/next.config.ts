module.exports = {
  reactStrictMode: true,
  experimental: {
    turbo: {
      loaders: {
        '.css': ['postcss-loader'],
      },
    },
  },
};
