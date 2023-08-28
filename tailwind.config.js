/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html", "./app/**/forms.py"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
};
