

//Modal for  publicate
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
//Modal for look a post

const btnOpen = document.querySelectorAll('.btn-open');
const btnClose = document.getElementById('btn-close');
const modalPost = document.getElementById('modalPost');

//Elements of Modal

const modalTitle = document.getElementById('modal-post-title');
const modalDescription = document.getElementById('modal-post-description');
const modalUsername = document.getElementById('modal-post-username');
const modalMedia = document.getElementById('modal-post-media');

// Click container father
const resultsDiv = document.getElementById('results')




btnOpen.forEach( post => {

    post.addEventListener('click',() =>
        {
            //  Get data of post cliked
        const postTitle = post.dataset.title;
        const postDescription = post.dataset.description;
        const postImg = post.dataset.img;
        const postUsername = post.dataset.username;
        const postType = post.dataset.type;


        //Update modal content

        modalTitle.textContent = postTitle;
        modalDescription.textContent = postDescription;
        modalUsername.textContent = postUsername;

        // imagen o video) Clean and add media (image o video)
        modalMedia.innerHTML = '';
        if (postType === 'video') {
            modalMedia.innerHTML = `<video src="${postImg}" controls class="btn-open" style="width: 100%;"></video>`;
        } else {
            modalMedia.innerHTML = `<img src="${postImg}" class="btn-open" style="width: 100%;">`;
        }
        
        modalPost.style.display = 'flex';


        });



}    );

btnClose.addEventListener('click', () => {
    modalPost.style.display = 'none';
});

