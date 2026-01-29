const searchInput = document.getElementById('searchInput');
const resultsDiv = document.getElementById('results');
let timeoutId = null;

searchInput.addEventListener('input',function()
{
    const query = this.value.trim();
    clearTimeout(timeoutId);

    if (query.length === 0)
    {
        resultsDiv.innerHTML = '';
        return;
    }
    timeoutId = setTimeout(()=>{
        performSearch(query)
    },
    300);

});

function performSearch(query)
{
    resultsDiv.innerHTML = '<div class = "loading">Buscando ...</div>';

    fetch(`/searchAjax?q=${encodeURIComponent(query)}`)

            .then(response => response.json())
            .then(data => {
                displayResults(data); })
            .catch(error => {
                console.error('Error:', error);
                resultsDiv.innerHTML = '<div class="no-results">Error al realizar la búsqueda</div>';
            });
}

function displayResults(results){

    if (results.length === 0)
    {
        resultsDiv.innerHTML = '<div class="no-results">No se encontraron resultados</div>';
        return;
    }

    let html = '' ;
    results.forEach(result =>{
       let mediaHTML = '';

       if (result.media_type === 'image')
        {
            mediaHTML = `<img src = "/static/uploads/${result.img}" alt = "${result.title}   " 
            
            class = "btn-open"
            data-title = "${result.title}"
            data-description = "${result.description}"
            data-username = "${result.username}"
            data-img = "/static/uploads/${result.img}"
            data-type = "image"
            
            >`;
        }
        else if (result.media_type === 'video') 
        {
            mediaHTML = `<video src = "/static/uploads/${result.img}" 
            
            class = "btn-open"
            data-title = "${result.title}"
            data-description = "${result.description}"
            data-username = "${result.username}"
            data-img = "/static/uploads/${result.img}" 
            data-type = "video"
            
            
            ></video>`;
        }
        else
        {
            mediaHTML = `<img src = "/static/uploads/none.jpg" alt = "No disponible"
            
            class = "btn-open"
            data-title = "${result.title}"
            data-description = "r${result.description}"
            data-username = "${result.username}"
            data-img = "/static/uploads/none.jpg"
            data-type = "image"    
            
            >`;
        }


        html += `
	        <div class="items">
		        ${mediaHTML}
                   
	            <div class="info">
		            <h3>${result.title}</h3>
	                <p>${result.description}</p>
	            </div>
		        <p>${result.username}<p/>
		    </div>           
        ` ;
    });
    resultsDiv.innerHTML = html;

}