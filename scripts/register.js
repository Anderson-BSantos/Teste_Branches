const app = firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();

document.getElementById("form-registro").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const plano = document.getElementById("plano").value;

  if (!plano) {
    alert("Por favor, selecione um plano.");
    return;
  }

  try {
    const userCredential = await auth.createUserWithEmailAndPassword(email, password);
    const user = userCredential.user;

    await db.collection("usuarios").doc(user.uid).set({
      email: user.email,
      plano: plano,
      nome: "",
      telefone: "",
      created_at: firebase.firestore.FieldValue.serverTimestamp()
    });

    alert("Registro realizado com sucesso!");
    window.location.href = "perfil.html";
  } catch (error) {
    console.error("Erro ao registrar:", error);
    alert("Erro ao registrar: " + error.message);
  }
});


const form = {
    plano: () => document.getElementById("plano"),
    email: () => document.getElementById("email"),
    password: () => document.getElementById("password")




}