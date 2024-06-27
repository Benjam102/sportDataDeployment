function sliderCompetition(sliderDoc, nextButton, precedentButton)
{
    let slider = document.querySelector(sliderDoc); 

    if(slider)
    {
        let items = slider.querySelectorAll('.c');
        let nbSlide = items.length;                           /* Nb d'image qu'on a dans le tableau items */
        let suivant = document.querySelector(nextButton);
        let precedent = document.querySelector(precedentButton);
        let count = 0;

        function slideSuivante()
        {
            items[count].classList.remove('slider-active');            /* On retire la propriété active */

            if(count < nbSlide - 1)                             /* On défile */
            {
                count++;
            } 
            else                                                /* On revient à l'image du début */
            {
                count = 0;
            }

            items[count].classList.add('slider-active');                /* On ajoute la classe active à l'image */
            // console.log(count);
        }

        /* Quand on clique, on envoie la slide suivante */
        suivant.addEventListener('click', slideSuivante);


        function slidePrecedente()
        {
            items[count].classList.remove('slider-active');

            if(count > 0)
            {
                count--;
            } 
            else 
            {
                count = nbSlide - 1;
            }

            items[count].classList.add('slider-active');
            // console.log(count); 
        }

        /* Quand on clique, on renvoie sur la slide précédente */
        precedent.addEventListener('click', slidePrecedente);
    }
}


sliderCompetition('.slider', '.right', '.left');
sliderCompetition('.slider2', '.right2', '.left2');
                                
                                       
                                    
                                        
                            
