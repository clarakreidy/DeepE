/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html",
        "./static/src/**/*.js",
        "./node_modules/flowbite/**/*.js"
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    "50": "#F1EFF8",
                    "100": "#DDD8ED",
                    "200": "#C7BEE1",
                    "300": "#B0A3D5",
                    "400": "#9F90CC",
                    "500": "#8E7CC3",
                    "600": "#8674BD",
                    "700": "#7B69B5",
                    "800": "#715FAE",
                    "900": "#5F4CA1"
                }
            }
        },
        fontFamily: {
            'body': [
                'Inter',
                'ui-sans-serif',
                'system-ui',
                '-apple-system',
                'system-ui',
                'Segoe UI',
                'Roboto',
                'Helvetica Neue',
                'Arial',
                'Noto Sans',
                'sans-serif',
                'Apple Color Emoji',
                'Segoe UI Emoji',
                'Segoe UI Symbol',
                'Noto Color Emoji'
            ],
            'sans': [
                'Inter',
                'ui-sans-serif',
                'system-ui',
                '-apple-system',
                'system-ui',
                'Segoe UI',
                'Roboto',
                'Helvetica Neue',
                'Arial',
                'Noto Sans',
                'sans-serif',
                'Apple Color Emoji',
                'Segoe UI Emoji',
                'Segoe UI Symbol',
                'Noto Color Emoji'
            ]
        },
        plugins: [
            require("flowbite/plugin")
        ],
    }
}