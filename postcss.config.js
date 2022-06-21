const cssnano = require('cssnano')
const autoprefixer = require('autoprefixer');

module.exports = ({env}) => ({
    plugins: [
        require("postcss-import"),
        require("tailwindcss/nesting"),
        require("tailwindcss"),
        env === 'production' ? autoprefixer() : null,
        env === 'production' ? cssnano({
            preset: ["default", {discardComments: {removeAll: true}}],
        }) : null,
    ],
})
