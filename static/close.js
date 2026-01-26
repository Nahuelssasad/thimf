const modal = document.getElementById('modal');
const openModalBtn = document.getElementById('openModalBtn');
const closeModalBtn = document.getElementById('closeModalBtn');





openModalBtn.addEventListener('click', () => {
    modal.style.display = 'flex';
});
//delete content when user click close
const title = document.getElementById('title');
const description = document.getElementById('description');
const imagen = document.getElementById('imagen-reemplazo');
const labelFile = document.querySelector('.custom-file-upload');

closeModalBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    title.value = '';
    description.value = '';
    imagen.src = '';
    imagen.style.display = 'none';
    
    labelFile.style.display = 'initial'

    
});

