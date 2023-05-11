const placa23 = document.querySelector("#placaVit")
if(placa23){
  console.log(placa23)
placa23.addEventListener('blur', (event) => {
  let vari = event.target.value;
  console.log(vari.toUpperCase())
  event.target.value = vari.toUpperCase()
  
  
});
  
}


function categoriaestacadastrada(result){
      // Display que exibe se achar a categoria ou não
const catnone = document.querySelector("#categorync")
if(!result){
  catnone.classList.remove("d-none");
}else{
  catnone.classList.add("d-none");
}

}

function capitalizeFirstLetter(word) {
    if (word && typeof word === 'string') {
      return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
    }
  return word;
}

// FUNÇÃO RESPONSAVEL POR CONTROLAR O A AUTORIZAÇÃO DE TITULARES NO SISTEMA

const authTitular = document.getElementById('authTitular')
if(authTitular){

  authTitular.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const authNameTit = button.getAttribute('data-bs-whateverauthnamtit')
    const authCatTit = button.getAttribute('data-bs-whateverauthcattit')
    const authIdTit = button.getAttribute('data-bs-whateverauthidtit')
    const authRecTit = button.getAttribute('data-bs-whateverauthrectit')
    const authdddTit = button.getAttribute('data-bs-whateverdddtit')
    const authtelTit = button.getAttribute('data-bs-whateverteltit')
    const titmatch = button.getAttribute('data-bs-whatevertitmatch')
    // Atualizando campos do meu model deputado

    const modalTitle = document.querySelector("#authModalLabel")
    const modaltitularfinded = document.querySelector("#titularfinded")
    const modalauthnamedtit = document.querySelector("#authnamedtit")
    const modalselectcategtit = document.querySelector("#addcategtit")
    const modalinputcategtit = document.querySelector("#lastaddtit")
    const modalauthuserchat = document.querySelector("#authuserchat")
    const modalauthRecTit = document.querySelector("#auth_only_assec")
    const modaldddauttit = document.querySelector("#dddauttit")
    const modaltelefauttit = document.querySelector("#telefauttit")
  
    // const authCatTit2 = capitalizeFirstLetter(authCatTit)
  
    modalTitle.textContent = 'Analisar dados titular - ' + authNameTit
    modaltitularfinded.value = titmatch
    modalauthnamedtit.value = authNameTit
    modalauthuserchat.value = authIdTit
    modalauthRecTit.checked = authRecTit
    modalselectcategtit.value = authCatTit
    modalinputcategtit.value = authCatTit
    modaldddauttit.value = authdddTit
    modaltelefauttit.value = authtelTit

    // categoriaestacadastrada(modalauthCatTit.value)
 
  })

}


// FUNÇÃO RESPONSAVEL POR CONTROLAR O A AUTORIZAÇÃO DE ASSESSORES NO SISTEMA

const authAssessor = document.getElementById('authAssessor')
if(authAssessor){

  authAssessor.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const authNameAss = button.getAttribute('data-bs-whatevernamAss')
    const authIdAss = button.getAttribute('data-bs-whateveridUserAss')
    const authAssCatTit = button.getAttribute('data-bs-whateverNomeCatAss')
    const authAssNomeTit = button.getAttribute('data-bs-whateverNomeTitAss')
    const idfullTit = button.getAttribute('data-bs-idfullTit')
    const dddAutAss = button.getAttribute('data-bs-whateverdddAss')
    const telAutAss = button.getAttribute('data-bs-whatevertelAss')
    console.log(`authNameAss: ${authNameAss}`)

    // Atualizando campos do meu model deputado
    const modalTitle = document.querySelector('#authAssModalLabel')
    const modalauthnameAss2 = document.querySelector("#authnameAss2")
    const modalauthidasschat = document.querySelector("#authasschatid")
    const modalSelectTit = document.querySelector("#authdepRep2")
    const modalCategoriaAssTit = document.querySelector("#categoriaDepAss")
    const modalinputcategtit = document.querySelector("#athinlinecat")
    const modalAuthAssNameTit = document.querySelector("#authassnametit")
    const modaldddAutAss = document.querySelector("#dddautass")
    const modaltelefautass = document.querySelector("#telefautass")
    
    // Rotulos dinamicos de acordo com a resposta
    const sugesttit = document.querySelector("#authsugesttit")
    
    
    modalTitle.textContent = 'Analisar dados assessor - ' + authNameAss
    modalauthnameAss2.value = authNameAss
    modalauthidasschat.value = authIdAss
    modalCategoriaAssTit.value = authAssCatTit
    modalinputcategtit.value = authAssCatTit
    modalAuthAssNameTit.value = authAssNomeTit
    modaldddAutAss.value = dddAutAss
    modaltelefautass.value = telAutAss
    numero_esc = parseInt(idfullTit, 10);
    
    if(numero_esc < 0){
      modalSelectTit.selectedIndex = 0
      sugesttit.classList.remove("d-none");
      console.log("Não achou...")
    }else{
      modalSelectTit.value = numero_esc
      console.log("Achou agora...")
      console.log(`numero_esc: ${numero_esc}`)
      sugesttit.classList.add("d-none");
    }
    
    
  })
  
}

function ajustaCategoriaTit(){

// Função que ajusta a categoria se vazia ou não
const authCategory = document.querySelector("#authCatTit") 
const categorync = document.querySelector("#categorync") 

console.log(authCategory.value)

if(authCategory.value !== 'Não listada'){
  if(authCategory.value !== ''){
    console.log("Foi selecionado algo")
    categorync.classList.add("d-none")
  }else{
    console.log("Seleção vazia")
    categorync.classList.remove("d-none")
  }
}else{
  console.log("Seleção vazia")
  categorync.classList.remove("d-none")
}


}


function adicionaTitModel(){
  // Função que faz aparecer ou esconde o formulário de cadastro de titulares
  const divAddTit = document.querySelector("#adicionadorTitModel") 
  divAddTit.classList.toggle("d-none")
}

function addCatModel(){
  // Permite adicionar categoria in-line
  const selectCat = document.querySelector("#categoriaDepAss") 
  const inputCat = document.querySelector("#divathinlinecat") 
  selectCat.classList.toggle("d-none")
  inputCat.classList.toggle("d-none")
}

function ajustadisplay(){
  // Sempre que um componente é modificado ele verifica os outros displays das models
  const authdeprep = document.querySelector("#authdepRep2") 
  const divAddTit = document.querySelector("#authsugesttit") 
  
  if(authdeprep.value == 'Não listado'){
    console.log("Foi selecionado algo")
    divAddTit.classList.remove("d-none")
  }else if(authdeprep.value == 'Selecione o parlamentar'){
    console.log("Foi selecionado algo")
    divAddTit.classList.remove("d-none")
  }else{
    console.log("Seleção vazia")
    divAddTit.classList.add("d-none")
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const formulario = document.getElementById('idauthFormDep2');
  if(formulario){
    formulario.addEventListener('submit', function(event) {
      event.preventDefault(); // Impede o envio padrão do formulário
      
      const nome = document.getElementById('authnamedtit').value;
      const categoria = document.getElementById('titularfinded').value;
      const categoria1 = document.getElementById('addcategtit').value;
      const categoria2 = document.getElementById('lastaddtit').value;
      
      if ((categoria === "" || categoria === "Não listado" || categoria === "Selecione o parlamentar") && categoria1 == "" && categoria2 == "") {
          alert('Você deve selecionar uma categoria válida ou marcar a opção "Adicionar Categoria" para enviar o formulário');
      }else if(nome === ""){
        alert('Você deve selecionar um nome válido para enviar o formulário'); 
      }else {
          formulario.submit(); // Envia o formulário
      }
  });

  }

});

function resetmodel(){
  ajustadisplay()
}

function somenteNumeros(e) {
  var charCode = (e.which) ? e.which : e.keyCode;
  if (charCode > 31 && (charCode < 48 || charCode > 57)) {
      return false;
  }
  return true;
}

function formatarNumero(el) {
  var valor = el.value.replace(/\D/g, ''); // Remove todos os caracteres não numéricos
  var novoValor = '';
  console.log(valor.length)
  if (valor.length <= 4) {
      novoValor = valor;
  } else if (valor.length === 9) {
      novoValor = valor.slice(0, 5) + '-' + valor.slice(5, 9);
  } else {
      novoValor = valor.slice(0, 4) + '-' + valor.slice(4);
  }

  if (valor.length === 5 && el.value.length === 5) {
      novoValor = valor.slice(0, 4) + '-' + valor.slice(4);
  }

  el.value = novoValor;
}

function mudarFoco(element) {
if(element['id'] == 'dddtit'){
   if (element.value.length == element.maxLength) {
    document.getElementById("telefonetit").focus();
}
}else if(element['id'] == 'dddass'){
if (element.value.length == element.maxLength) {
  document.getElementById("telefoneass").focus();
}

}
}