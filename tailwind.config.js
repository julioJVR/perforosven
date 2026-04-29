/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",               // base.html y otros
    "./core/templates/**/*.html",
    "./compras/templates/**/*.html",
    "./ventas/templates/**/*.html",        // ← importante
    "./contabilidad/templates/**/*.html",
    "./static/**/*.js",                    // si tienes JS con clases dinámicas
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}