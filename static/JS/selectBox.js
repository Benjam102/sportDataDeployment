const dropdowns = document.querySelector('.container-select')
console.log(dropdowns)
/* On récupère l'ensemble des class*/
const select = dropdowns.querySelector('.select')
const caret = dropdowns.querySelector('.caret')
const annees = dropdowns.querySelector('.years')
const li_ = dropdowns.querySelectorAll('.years li')
const selected = dropdowns.querySelector('.selected')

select.addEventListener('click', function() {
    /* Quand je clique sur la drop box la flèche fait une rotation */ 
    caret.classList.toggle('caret-rotate');
    /* Quand je clique sur la drop box le menu déroulant apparaît */
    annees.classList.toggle('years-open');
});

li_.forEach(function(li) {
    li.addEventListener('click', function() {
        selected.innerText = li.innerText;

        caret.classList.toggle('caret-rotate');

        annees.classList.toggle('years-open');

        li_.forEach(function(li) {
            li.classList.remove('active');
        });

        li.classList.add('active');
    });
});
