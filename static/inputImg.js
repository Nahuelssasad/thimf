const input = document.getElementById('file-upload');
const imagenReemplazo = document.getElementById('imagen-reemplazo');
const label = document.querySelector('.custom-file-upload');
input.addEventListener('change', function() {
    const file = this.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function() {
            imagenReemplazo.src = this.result;
            imagenReemplazo.style.display = 'block';
            input.style.display = 'none';
            label.style.display = 'none';

        }   
        reader.readAsDataURL(file);
    }
});