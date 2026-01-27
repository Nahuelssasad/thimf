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
        const imgUrl = `/static/uploads/${result.img}`;
        html += `
	        <div class="items">
		        <img src=" ${imgUrl}">
                   
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