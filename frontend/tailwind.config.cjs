module.exports = {
  content: ['./index.html', './src/**/*.{svelte,js,ts}'],
  theme: {
    extend: {}
  },
  plugins: [
    require("daisyui"),
    require('@tailwindcss/line-clamp')
  ],
}