const app = firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();

// Substitua pelo seu Client ID do Imgur
const IMGUR_CLIENT_ID = "62f17188ceb8421"; // Ex.: "f1XXXXXXXXXXXXX"

// Monitora o estado de autenticação
auth.onAuthStateChanged(async (user) => {
  if (!user) {
    window.location.href = "login.html";
    return;
  }

  // Preenche o email automaticamente
  document.getElementById("email").value = user.email || "-";
  document.getElementById("preview-email").innerText = user.email || "-";

  // Carrega os dados existentes do Firestore
  try {
    const docRef = db.collection("usuarios").doc(user.uid);
    const doc = await docRef.get();

    if (doc.exists) {
      const data = doc.data();

      // Preenche os campos com os dados existentes
      document.getElementById("plano").value = data.plano || "-";
      document.getElementById("preview-plano").innerText = data.plano || "-";
      document.getElementById("nome").value = data.nome || "";
      document.getElementById("telefone").value = data.telefone || "";
      document.getElementById("preview-nome").innerText = data.nome || "-";
      document.getElementById("preview-telefone").innerText = data.telefone || "-";

      if (data.fotoPerfil) {
        document.getElementById("preview-foto").src = data.fotoPerfil;
      }
    } else {
      // Se o documento não existe, cria um documento inicial
      await docRef.set({
        email: user.email,
        plano: "", // Será preenchido pelo usuário ou no registro
        nome: "",
        telefone: "",
        created_at: firebase.firestore.FieldValue.serverTimestamp()
      });
    }
  } catch (error) {
    console.error("Erro ao carregar dados do perfil:", error);
    alert("Erro ao carregar dados do perfil: " + error.message);
  }
});

// Manipula o envio do formulário
document.getElementById("form-perfil").addEventListener("submit", async (e) => {
  e.preventDefault();

  const user = auth.currentUser;
  if (!user) {
    alert("Usuário não autenticado. Faça login novamente.");
    window.location.href = "login.html";
    return;
  }

  // Obtém os valores do formulário
  const nome = document.getElementById("nome").value.trim();
  const telefone = document.getElementById("telefone").value.trim();
  const plano = document.getElementById("plano").value || "";
  const file = document.getElementById("foto").files[0];

  // Validações
  if (!nome) {
    alert("Por favor, insira seu nome.");
    return;
  }

  const telefoneRegex = /^\d{10,11}$/; // Exemplo: 11987654321 (10 ou 11 dígitos)
  if (!telefone || !telefoneRegex.test(telefone)) {
    alert("Por favor, insira um telefone válido (apenas números, 10 ou 11 dígitos).");
    return;
  }

  try {
    // Feedback visual durante o salvamento
    const submitButton = document.querySelector("#form-perfil button");
    submitButton.disabled = true;
    submitButton.innerText = "Salvando...";

    // Carrega a foto atual do Firestore (para manter a foto existente se não houver nova)
    let fotoPerfil = "";
    const userDoc = await db.collection("usuarios").doc(user.uid).get();
    if (userDoc.exists && userDoc.data().fotoPerfil) {
      fotoPerfil = userDoc.data().fotoPerfil;
    }

    // Faz o upload da nova foto para o Imgur, se fornecida
    if (file) {
      // Valida o tamanho da foto (máximo 5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert("A foto deve ter no máximo 5MB.");
        submitButton.disabled = false;
        submitButton.innerText = "Salvar Perfil";
        return;
      }

      // Cria um FormData para enviar a foto para o Imgur
      const formData = new FormData();
      formData.append("image", file);

      // Faz a requisição para o Imgur API
      const response = await fetch("https://api.imgur.com/3/image", {
        method: "POST",
        headers: {
          Authorization: `Client-ID ${IMGUR_CLIENT_ID}`,
        },
        body: formData,
      });

      const jsonData = await response.json();
      if (!jsonData.success) {
        throw new Error("Erro ao fazer upload para o Imgur: " + (jsonData.data.error || "Desconhecido"));
      }

      // Obtém a URL da foto
      fotoPerfil = jsonData.data.link; // Ex.: "https://i.imgur.com/abc123.jpg"
    }

    // Salva os dados no Firestore
    await db.collection("usuarios").doc(user.uid).set({
      nome: nome,
      telefone: telefone,
      plano: plano,
      email: user.email,
      ...(fotoPerfil && { fotoPerfil: fotoPerfil }),
      updated_at: firebase.firestore.FieldValue.serverTimestamp()
    }, { merge: true });

    // Atualiza a prévia em tempo real
    document.getElementById("preview-nome").innerText = nome || "-";
    document.getElementById("preview-telefone").innerText = telefone || "-";
    document.getElementById("preview-plano").innerText = plano || "-";
    if (fotoPerfil) {
      document.getElementById("preview-foto").src = fotoPerfil;
    }

    alert("Perfil salvo com sucesso!");
  } catch (error) {
    console.error("Erro ao salvar perfil:", error);
    alert("Erro ao salvar perfil: " + error.message);
  } finally {
    // Restaura o botão
    const submitButton = document.querySelector("#form-perfil button");
    submitButton.disabled = false;
    submitButton.innerText = "Salvar Perfil";
  }
});