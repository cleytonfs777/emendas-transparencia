
// In your Javascript (external .js resource or <script> tag)
  let selectedFiles = [];

  function separarItens(s) {
    const itensSeparados = s.split(';');
    const resultado = [];

    for (const item of itensSeparados) {
        if (item) {
            resultado.push(item.split(','));
        }
    }

    return resultado;
  }  

  function agruparElementos(arr) {
    if (!Array.isArray(arr[0]) && arr.length === 2) {
      return [arr];
    }
  
    const resultado = [];
  
    arr.forEach(item => {
      const primeiroElemento = item[0];
      const segundoElemento = item[1];
      let elementoEncontrado = false;
  
      for (let i = 0; i < resultado.length; i++) {
        if (resultado[i][1] === segundoElemento) {
          resultado[i][0].push(primeiroElemento);
          elementoEncontrado = true;
          break;
        }
      }
  
      if (!elementoEncontrado) {
        resultado.push([[primeiroElemento], segundoElemento]);
      }
    });
  
    return resultado;
  }


  function arrayParaString(arr) {
    return JSON.stringify(arr);
  }
  


  function insereTable(){

    let dept = document.querySelector("#vtrPlaca")
    let placa = dept.children[dept.selectedIndex]
    let tbody1 = document.querySelector("table[name='tabela'] > tbody")
    //encplaca é a variavel que vai receber os registros de placas e tipos
    let encplaca = document.querySelector('div.col-md-6:nth-child(2) > input:nth-child(1)')
    let encplaca2 = document.querySelector("#idFormDep > div > div:nth-child(1) > div:nth-child(2) > input[type=hidden]:nth-child(2)")
    // Verificação se o campo não está vazio
    if(placa.innerText == 'Selecione uma viatura'){
      return
    }
    // Verificação a placa já não está na tabela
    let campos = document.querySelectorAll('.table > tbody:nth-child(2) > tr > td')
    let cont = campos.length
    if(cont > 0){
      cont = cont - 3
      while (cont >= 0){
        if(campos[cont].innerText == placa.innerText){
          alert("Essa viatura já foi adicionada")
          return
        }
        cont = cont - 3
      }
    }
    

    let fin = document.createElement('tr')
    let dep1 = document.createElement('td')
    dep1.innerText = placa.innerText
    fin.appendChild(dep1)
    let dep2 = document.createElement('td')
    dep2.innerText = dept.value
    fin.appendChild(dep2)
    let dep3 = document.createElement('td')
    dep3.innerHTML = '<a href="#" class="btn btn-danger p-1" onclick="removerElemento(event.target)">X</a>'
    fin.appendChild(dep3)
    tbody1.appendChild(fin)
    document.querySelector('.diplayvtr').classList.add('hidd')
    encplaca.value = encplaca.value+`${dep1.innerText},${dep2.innerText};` 
    
    console.log(arrayParaString(agruparElementos(separarItens(encplaca.value))))
    encplaca2.value = arrayParaString(agruparElementos(separarItens(encplaca.value)))
  }
  
  
  function removerElemento(elementoClicado) {
    
    let tbody2 = document.querySelector("table[name='tabela'] > tbody")
    let encplaca1 = document.querySelector('div.col-md-6:nth-child(2) > input:nth-child(1)')
    let encplaca2 = document.querySelector("#idFormDep > div > div:nth-child(1) > div:nth-child(2) > input[type=hidden]:nth-child(2)")
    let chave = elementoClicado.closest('tr').firstChild.innerText
    let chave2 = elementoClicado.closest('tr').childNodes[1].innerText

    elementoClicado.closest("tr").remove();
    encplaca1.value = encplaca1.value.replace(`${chave},${chave2};`,'')
    console.log(arrayParaString(agruparElementos(separarItens(encplaca1.value))))
    encplaca2.value = arrayParaString(agruparElementos(separarItens(encplaca1.value)))
  
  if(tbody2.children.length == 0){
    document.querySelector('.diplayvtr').classList.remove('hidd')
  }


}
// Gera uma visualização previows de cada imagem carregada
function previewImagens(input) {
  const previewImagens = document.getElementById('preview-imagens');
  previewImagens.innerHTML = '';
  const files = Array.from(input.files);
  selectedFiles = files; // Atualize a variável selectedFiles diretamente com os arquivos selecionados

  files.forEach((file) => {
    const reader = new FileReader();
  
    reader.onloadend = () => {
      const previewContainer = document.createElement('div');
      previewContainer.setAttribute('id', `preview-container-${file.name}`);
      previewContainer.setAttribute('class', 'preview-container');
  
      const imagem = document.createElement('img');
      imagem.setAttribute('src', reader.result);
      imagem.setAttribute('class', 'preview-imagem');
  
      const removerBotao = document.createElement('span');
      removerBotao.innerHTML = '&times;';
      removerBotao.setAttribute('class', 'preview-remover');
      removerBotao.onclick = () => removerImagemPreview(file);
  
      previewContainer.appendChild(imagem);
      previewContainer.appendChild(removerBotao);
      previewImagens.appendChild(previewContainer);
    };
  
    reader.readAsDataURL(file);
  });
  
}

function createFileList(files) {
  const fileList = new DataTransfer();

  for (const file of files) {
    fileList.items.add(file);
  }

  return fileList.files;
}

function removerImagemPreview(file) {
  const previewContainer = document.getElementById(`preview-container-${file.name}`);
  previewContainer.remove();

  // Remova a imagem da lista de arquivos selecionados
  selectedFiles = selectedFiles.filter((f) => f !== file);

  // Atualizar o input com os arquivos selecionados
  updateInputFiles(selectedFiles);
}


function updateInputFiles(files) {
  const inputFile = document.getElementById('imagens');
  const clonedInputFile = inputFile.cloneNode();

  // Limpar o atributo 'onchange' para evitar múltiplos eventos
  clonedInputFile.onchange = null;

  // Adicionar novamente o event listener 'onchange'
  clonedInputFile.addEventListener('change', (event) => {
    previewImagens(event.target);
  });

  // Atualizar os arquivos do novo input
  clonedInputFile.files = createFileList(files);

  // Substituir o input original pelo novo input
  inputFile.parentNode.replaceChild(clonedInputFile, inputFile);
}

function initializeSelect2() {
  const selectElementVtrPlaca = document.getElementById('vtrPlaca');
  const selectElementStatusOcorr = document.getElementById('status_ocorr');
  $(selectElementVtrPlaca).select2();
  $(selectElementStatusOcorr).select2();
}

function resetFormOnLoad() {
  const form = document.getElementById('idFormDep');
  form.reset();
  initializeSelect2();
  $('#vtrPlaca').val(null).trigger('change'); // Atualiza o valor do Select2 (vtrPlaca)
  $('#status_ocorr').val(null).trigger('change'); // Atualiza o valor do Select2 (status_ocorr)
}

window.addEventListener('DOMContentLoaded', () => {
  resetFormOnLoad();
  initializeSelect2();
});


