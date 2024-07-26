function clickMenu() 
{
     /**
     * Function to handle the click on the small dropdown menu.
     *
     */

    /* Select the element with the class "petit-menu" in the HTML document */
    var petit_menu = document.querySelector(".petit-menu");

    /* Select the element with the class "menu" in the HTML document */
    var menu = document.querySelector(".menu");
    
    /* Attach a function to the "onclick" event of the petit_menu element */
    petit_menu.onclick = 
    function() 
    {
        /* On click on the petit_menu element, toggle the 'croix' class of this element */
        petit_menu.classList.toggle('croix');
        
        /* On click on the petit_menu element, toggle the 'appui-rond' class of the menu element */
        menu.classList.toggle('appui-rond');
    }
}
  
/* Call the function to activate the small menu handling */
document.addEventListener('DOMContentLoaded', function() 
{
    clickMenu();
});

  