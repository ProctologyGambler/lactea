/** @type {import('tailwindcss').Config} */
module.exports = {
  // Scan every file that could carry Tailwind class names. Django
  // templates + any JS + per-skin Python copy files (a class string
  // could live in copy).
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
    './skins/**/*.py',
    './core/**/*.py',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

