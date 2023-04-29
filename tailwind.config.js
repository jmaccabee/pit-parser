/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './pit_parser/templates/**/*.html'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}