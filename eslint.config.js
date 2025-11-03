export default [
  {
    files: ["frontend/*.js"], // tous les fichiers JS
    languageOptions: {
      globals: {
        window: "readonly",
        document: "readonly",
        console: "readonly"
      },
      ecmaVersion: 2021,
      sourceType: "module"
    },
    rules: {
      // Obligatoire : point-virgule
      semi: ["error", "always"],
      // Obligatoire : guillemets doubles
      quotes: ["error", "double"]
      // Tu peux ajouter d'autres règles ici
    }
  }
];
