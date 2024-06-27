function selectDropDowns(container)
{
    const containerD = document.getElementById(container);
    const dropdowns = containerD.querySelector('.container-select');
    
    if (dropdowns)
    {
        /* On récupère l'ensemble des class*/
        const select = dropdowns.querySelector('.select');
        const caret = dropdowns.querySelector('.caret');
        const annees = dropdowns.querySelector('.val');
        const li_ = dropdowns.querySelectorAll('.val li');
        const selected = dropdowns.querySelector('.selected');

        select.addEventListener('click', function() 
        {
            /* Quand je clique sur la drop box la flèche fait une rotation */ 
            caret.classList.toggle('caret-rotate');
            /* Quand je clique sur la drop box le menu déroulant apparaît */
            annees.classList.toggle('val-open');
        });
        
        li_.forEach(function(li) 
        {
            li.addEventListener('click', function() 
            {
                selected.innerText = li.innerText;
        
                caret.classList.toggle('caret-rotate');
        
                annees.classList.toggle('val-open');
        
                li_.forEach(function(li) {
                    li.classList.remove('active');
                });
        
                li.classList.add('active');
            });
        });
    }
}

selectDropDowns('content-cat3.1');
selectDropDowns('content-cat3.2');
selectDropDowns('content-predic1-1');
selectDropDowns('content-predic1-2');


