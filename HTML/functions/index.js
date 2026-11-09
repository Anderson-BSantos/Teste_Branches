
const functions = require("firebase-functions");
const admin = require("firebase-admin");
admin.initializeApp();

const db = admin.firestore();

// Gera e salva link baseado na data atual (executado diariamente)
exports.gerarLinkDiario = functions.pubsub.schedule("every day 02:00").onRun(async () => {
    const data = new Date();
    const dia = data.getDate();
    const mes = data.getMonth() + 1;
    const ano = data.getFullYear();
    const sum = ano * 15;
    const parametro = `${dia}${mes}${sum}`;
  
    // URL original protegida
    const linkOriginal = "https://app.powerbi.com/view?r=eyJrIjoiYTY4ZDJmY2QtNjc0Yi00NDcxLWI1YmItNDNmNDVkMmYwNGRjIiwidCI6IjRjZDgzNWY0LTU0NDAtNDA4Zi05M2EzLTk3NWZjMTdjMzg0YSIsImMiOjR9";
  
    await db.collection("links").doc(parametro).set({
      original: linkOriginal,
      criadoEm: admin.firestore.FieldValue.serverTimestamp()
    });
  
    console.log(`✅ Link diário salvo: ${parametro} → ${linkOriginal}`);
    return null;
  });
  
exports.redirecionar = functions.https.onRequest(async (req, res) => {
    const id = req.path.replace("/", "");
  
    if (!id) {
      return res.status(400).send("Código inválido.");
    }
  
    try {
      const doc = await db.collection("links").doc(id).get();
  
      if (!doc.exists) {
        return res.status(404).send("Link não encontrado ou expirado.");
      }
  
      const data = doc.data();
      const linkOriginal = data.original;
  
      // Redireciona sem mostrar nada
      return res.redirect(linkOriginal);
  
    } catch (err) {
      console.error("Erro ao redirecionar:", err);
      return res.status(500).send("Erro interno ao redirecionar.");
    }
  });
  
// Redireciona acesso para o link original com base no código
exports.redirecionar = functions.https.onRequest(async (req, res) => {
    const id = req.path.replace("/", "");
    const doc = await db.collection("links").doc(id).get();

    if (!doc.exists) {
        return res.status(404).send("Link não encontrado");
    }

    const urlOriginal = doc.data().original;
    return res.redirect(urlOriginal);
});
