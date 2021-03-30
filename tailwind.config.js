const colors = require('tailwindcss/colors')

module.exports = {
    purge: [
        'apps/*/templates/**/*.html',
        'apps/*/templates/**/*.txt',
        'templates/**/*.html',
        'templates/**/*.txt',
    ],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            typography: {
                DEFAULT: {
                    css: {
                        color: colors.gray['800'],
                        'ul > li::before': {
                            backgroundColor: colors.gray['700'],
                        },

                    },
                },
            },
            colors: {
                gray: colors.trueGray,
            },
            boxShadow: {
                center: 'rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 10%) 0px 1px 3px 0px, rgb(0 0 0 / 6%) 0px 1px 2px 0px, rgb(0 0 0 / 10%) 0px -1px 3px 0px, rgb(0 0 0 / 6%) 0px -1px 2px 0px',
            },
            transitionDuration: {
                '0': '0ms',
                '2000': '2000ms',
            },
            screens: {
                'print': {'raw': 'print'},
                // => @media print { ... }
            }
        },
    },
    variants: {
        extend: {
            textAlign: ['last'],
            backgroundColor: ['active'],
            translate: ['group-hover'],
            padding: ['last', 'first'],
            margin: ['last', 'first'],
            scale: ['group-hover']
        }
    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/line-clamp'),
    ],
}
