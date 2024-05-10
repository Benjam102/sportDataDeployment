
/* Fonction pour gérer le clic sur le petit menu déroulant */
function clickMenu() 
{
    /* Sélectionne l'élément ayant la classe "petit-menu" dans le document HTML */
    var petit_menu = document.querySelector(".petit-menu");

    /* Sélectionne l'élément ayant la classe "menu" dans le document HTML */
    var menu = document.querySelector(".menu");
    
    /* Attache une fonction à l'événement "onclick" de l'élément petit menu */
    petit_menu.onclick = 
    function() 
    {
        /* Au clic sur l'élément petit menu, on bascule sur la classe 'croix' de cet élément */
        petit_menu.classList.toggle('croix');
        
        /* Au clic sur l'élément petit menu, on bascule sur la classe 'appui-rond' de l'élément menu */
        menu.classList.toggle('appui-rond');
    }
}
  
/*Appel de la fonction pour activer la gestion du petit menu */
clickMenu();
  