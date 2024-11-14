module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'https://piyo.my.id/api', // Your Flask API URL
                changeOrigin: true,
                pathRewrite: { '^/api': '' },
            },
        },
    },
};