const textarea = document.querySelectorAll('textarea');
textarea.forEach(textarea => {
    textarea.addEventListener('input', e => {
        textarea.style.height = '18px'    
        textarea.style.height = `${textarea.scrollHeight}px`;
        
    });
});