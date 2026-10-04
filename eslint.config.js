module.exports = [
  {
    ignores: ["site/**"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "script",
      globals: {
        browser: "readonly",
        chrome: "readonly",
        console: "readonly",
        document: "readonly",
        navigator: "readonly",
        URL: "readonly",
      },
    },
  },
];
