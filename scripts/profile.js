
/*
// Constantes para os elementos do DOM
import { getStorage, ref, uploadBytes, getDownloadURL } from "firebase/storage";
import { getFirestore, collection, addDoc, Timestamp } from "firebase/firestore";

const storage = getStorage();
const db = getFirestore();

const inputFile = document.getElementById("avatar-upload");
const avatarPreview = document.getElementById("preview-avatar");
let selectedFile = null;

// Mostrar preview
inputFile.addEventListener("change", (e) => {
  selectedFile = e.target.files[0];
  const reader = new FileReader();
  reader.onload = () => {
    avatarPreview.src = reader.result;
  };
  reader.readAsDataURL(selectedFile);
});

document.getElementById("profile-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = document.getElementById("nome").value;
  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;
  const plano = document.getElementById("plano").value;

  try {
    let imageUrl = "";

    if (selectedFile) {
      const imageRef = ref(storage, `avatars/${Date.now()}_${selectedFile.name}`);
      await uploadBytes(imageRef, selectedFile);
      imageUrl = await getDownloadURL(imageRef);
    }

    const diasPlano = { básico: 30, premium: 60, empresarial: 90 };
    const dataExp = new Date();
    dataExp.setDate(dataExp.getDate() + diasPlano[plano]);

    await addDoc(collection(db, "usuarios"), {
      nome,
      email,
      senha, // use hash ou Firebase Auth em produção
      plano,
      dataExpiracao: Timestamp.fromDate(dataExp),
      fotoPerfil: imageUrl
    });

    alert("Usuário cadastrado com sucesso!");
  } catch (err) {
    console.error("Erro ao salvar perfil:", err);
    alert("Erro ao cadastrar usuário.");
  }
});


document.getElementById("avatar-upload").addEventListener("change", function (e) {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = function () {
      document.getElementById("preview-avatar").src = reader.result;
    };
    if (file) reader.readAsDataURL(file);
  });  
-->
*/


// onClick function to redirect to the profile page
function asClick() {
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;
    showLoading();
    firebase.auth().signInWithEmailAndPassword(email, senha).then(response => {
        hideLoading();
        window.location.href = "profile/teste.html";

    }).catch(error => {
        hideLoading();
        console.error("Erro ao fazer login:", error);
    });

    //

}
    // var profile = document.getElementById("profile").value;
    // var url = "/infogeo/profile/" + profile;
    // window.open(url, "_self");
    // return false;
    // }