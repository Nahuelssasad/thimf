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
const resultConteiner = document.getElementById('results');


resultConteiner.addEventListener('click',e =>{

    const btnOpenSearch =   e.target.closest('.btn-open');

    if (btnOpenSearch){
            //  Get data of post cliked
        const postTitle = btnOpenSearch.dataset.title;
        const postDescription = btnOpenSearch.dataset.description;
        const postImg = btnOpenSearch.dataset.img;
        const postUsername = btnOpenSearch.dataset.username;
        const postType = btnOpenSearch.dataset.type;


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






    };








});

btnClose.addEventListener('click', () => {
    modalPost.style.display = 'none';
});

