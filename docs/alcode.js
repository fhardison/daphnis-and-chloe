
  document.addEventListener("DOMContentLoaded", function(event) {
    import ("https://cdn.jsdelivr.net/npm/alpheios-embedded@latest/dist/alpheios-embedded.min.js").then(embedLib => {
      window.AlpheiosEmbed.importDependencies({
        mode: 'cdn'
      }).then(Embedded => {
        new Embedded({
          clientId: 'test'
        }).activate();
      }).catch(e => {
        console.error(`Import of Alpheios embedded library dependencies failed: ${e}`)
      })
    }).catch(e => {
      console.error(`Import of Alpheios Embedded library failed: ${e}`)
    })
  });

