const div = document.querySelector('.slider'); 
const items = div.querySelectorAll('table');
const nbSlide = items.length;                           /* Nb d'image qu'on a dans le tableau items */
const suivant = document.querySelector('.right');
const precedent = document.querySelector('.left');
let count = 0;

function slideSuivante()
{
    items[count].classList.remove('active');            /* On retire la propriété active */

    if(count < nbSlide - 1)                             /* On défile */
    {
        count++;
    } 
    else                                                /* On revient à l'image du début */
    {
        count = 0;
    }

    items[count].classList.add('active')                /* On ajoute la classe active à l'image */
    // console.log(count);
}

/* Quand on clique, on envoie la slide suivante */
suivant.addEventListener('click', slideSuivante)


function slidePrecedente()
{
    items[count].classList.remove('active');

    if(count > 0)
    {
        count--;
    } 
    else 
    {
        count = nbSlide - 1;
    }

    items[count].classList.add('active')
    // console.log(count); 
}

/* Quand on clique, on renvoie sur la slide précédente */
precedent.addEventListener('click', slidePrecedente)
