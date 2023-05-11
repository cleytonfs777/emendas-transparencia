const menul = document.querySelectorAll("#navbar-items > ul > li > a")
const placa = document.querySelector("#placaVit")

// In your Javascript (external .js resource or <script> tag)
$(document).ready(function() {
    $('.filtrado').select2();
});



function verSubmenu(event) {
event.stopPropagation();
var target = event.target;
var submenus = target.nextElementSibling;
submenus.classList.toggle("ul-click");
}        


function setUnvisto(elemento, act){
    if(act == 'remover'){
        if(!(elemento.classList.contains("unvisto"))){
            elemento.classList.add("unvisto");
        }
    }else{
        if(elemento.classList.contains("unvisto")){
            elemento.classList.remove("unvisto");
        }
    }
}

   // Função para selecionar o lista a ser apresentado no cadastro
   function updateUrlParam(param, value) {
    let url = new URL(window.location.href);
    url.searchParams.set(param, value);
    window.history.replaceState(null, null, url);
  }

 
  
  // FUNÇÃO RESPONSAVEL POR CONTROLAR O CARREGAMENTO DOS DADOS PARA EDIÇÃO - TITULAR
  
  const exampleModal = document.getElementById('editTitular')
  if(exampleModal){
  exampleModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const idDep = button.getAttribute('data-bs-whatever')
    const namDep = button.getAttribute('data-bs-whatevernamDep')
    const catDep = button.getAttribute('data-bs-whatevercatDep')
    const idtelegtit = button.getAttribute('data-bs-whateveridtelegtit')
    const telfnumber = button.getAttribute('data-bs-whatevertelfnumber')
    const ddd = button.getAttribute('data-bs-whateverddd')
    const MsgDep = button.getAttribute('data-bs-whateverRecMsgDep')
  
    // Atualizando campos do meu model deputado
    const modalTitle = exampleModal.querySelector('.modal-title')
    const modalcateg = document.querySelector("#categoriaDep2")
    const modalname = document.querySelector("#nameDep2")
    const modalidtelegtit = document.querySelector("#idtelegtit")
    const dddmodaltit = document.querySelector("#dddmodaltit")
    const telefmodaltit = document.querySelector("#telefmodaltit")
    const modalrecInfo = document.querySelector("#flexSwitchCheckDefault2")
    const modalForm = document.querySelector("#idFormDep2")
  
    const RecMsgDep = MsgDep == 'True' ? true : false;
  
    modalTitle.textContent = 'Editar dados do Títular ' + namDep
    modalcateg.value = catDep
    modalname.value = namDep
    modalidtelegtit.value = idtelegtit
    dddmodaltit.value = ddd == "None" ? "" : ddd
    telefmodaltit.value = telfnumber == "None" ? "" : telfnumber
    modalrecInfo.checked = RecMsgDep
    let url = modalForm.getAttribute("data-action"); 
    url = url.replace('0',idDep)  
    modalForm.setAttribute("action", url);
    
  })
  }
  // FUNÇÃO RESPONSAVEL POR CONTROLAR O CARREGAMENTO DOS DADOS PARA EDIÇÃO - ASSESSORES
  
  const assessorModal = document.getElementById('editAssessor')
  assessorModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const idAss = button.getAttribute('data-bs-whateverAss')
    const nameAss = button.getAttribute('data-bs-whatevernamAss')
    const idtelegAss = button.getAttribute('data-bs-whateveridtelegass')
    const dddAss = button.getAttribute('data-bs-whateverdddAss')
    const numberAss = button.getAttribute('data-bs-whatevertelfnumberAss')
    const RepDep = button.getAttribute('data-bs-whateverDepAss')
  
    // Atualizando campos do meu model titular
    const modalTitle = assessorModal.querySelector('.modal-title')
    const modalname = document.querySelector("#nameAss2")
    const modalidtelegass = document.querySelector("#idtelegass")
    const dddmodalass = document.querySelector("#dddmodalass")
    const telefmodalass = document.querySelector("#telefmodalass")
    const modalDepRep = document.querySelector("#depRep2")
    const modalForm22 = document.querySelector("#idFormAss2")
  
  
    modalTitle.textContent = 'Editar dados do Assessor ' + nameAss
    modalname.value = nameAss
    modalidtelegass.value = idtelegAss
    dddmodalass.value = dddAss == 'None'  ? "" : dddAss
    telefmodalass.value = numberAss == 'None'  ? "" : numberAss
    modalDepRep.value = RepDep
    let url = modalForm22.getAttribute("data-action");
    url = url.replace('0',idAss)
    modalForm22.setAttribute("action", url);
    
  })
  
  // FUNÇÃO RESPONSAVEL POR CONTROLAR O CARREGAMENTO DOS DADOS PARA EDIÇÃO - VIATURAS
  
  const viaturasModal = document.getElementById('editViatura')
  viaturasModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const idVit = button.getAttribute('data-bs-whatevervit')
    const tipVit = button.getAttribute('data-bs-whateverTip')
    const placaVit = button.getAttribute('data-bs-whateverPlac')
    const vitDep = button.getAttribute('data-bs-whateverDepVit')
  
    // Atualizando campos do meu model deputado
    const modalTitle = viaturasModal.querySelector('.modal-title')
    const modalTipoVit = document.querySelector("#tipoVit2")
    const modalPlacaVit = document.querySelector("#placaVit2")
    const modalDepRep2 = document.querySelector("#tipoDep3")
    const modalForm23 = document.querySelector("#idFormVit2")
  
  
    modalTitle.textContent = 'Editar dados da Viatura ' + placaVit
    modalTipoVit.value = tipVit
    modalPlacaVit.value = placaVit
    modalDepRep2.value = vitDep
    let url = modalForm23.getAttribute("data-action");
    console.log(url)
    url = url.replace('0',idVit)
    console.log(idVit)
    console.log(url)
    modalForm23.setAttribute("action", url);
    
  })
  
  
  
  
  



