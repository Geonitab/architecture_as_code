(function initialiseMermaid() {
  if (window.mermaidReady) {
    return;
  }

  const mermaidVersion = "11.3.0";
  const mermaidSource = `https://cdn.jsdelivr.net/npm/mermaid@${mermaidVersion}/dist/mermaid.esm.min.mjs`;
  const radarModuleSource = `https://cdn.jsdelivr.net/npm/mermaid@${mermaidVersion}/dist/diagrams/radarDiagram-definition.esm.min.mjs`;

  window.mermaidReady = (async () => {
    try {
      const module = await import(mermaidSource);
      const mermaid = module?.default ?? module;

      mermaid.initialize({
        startOnLoad: true,
        theme: "default",
        securityLevel: "loose",
        diagramLoader: async (type) => {
          if (type === "radar") {
            return import(radarModuleSource);
          }

          return undefined;
        }
      });

      window.mermaid = mermaid;
      return mermaid;
    } catch (error) {
      console.error("Mermaid initialisation failed", error);
      throw error;
    }
  })();
})();
