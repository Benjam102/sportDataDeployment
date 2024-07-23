function sliderCompetition(sliderDoc, nextButton, precedentButton)
{
    /**
     * Function to manage a slider.
     *
     * @param {string} sliderDoc Class of the slider.
     * @param {string} nextButton Class Right scroll button.
     * @param {string} precedentButton class Left scroll button.
     */

    let slider = document.querySelector(sliderDoc); 

    if(slider)
    {
        // Get all items within the slider
        let items = slider.querySelectorAll('.c');
        let nbSlide = items.length;                                 // Number of images in the items array
        let suivant = document.querySelector(nextButton);           // Right scroll button
        let precedent = document.querySelector(precedentButton);    // Left scroll button
        let count = 0;

        function slideSuivante()
        {
            // Remove the active class from the current item
            items[count].classList.remove('slider-active');

            // Increment the count or reset to 0 if at the end
            if(count < nbSlide - 1)                                 // Scroll forward
            {
                count++;
            } 
            // Return to the first image
            else 
            {
                count = 0;
            }

            // Add the active class to the new current item
            items[count].classList.add('slider-active');
        }

        // Add event listener for the right scroll button
        suivant.addEventListener('click', slideSuivante);

        function slidePrecedente()
        {
            // Remove the active class from the current item
            items[count].classList.remove('slider-active');

            // Decrement the count or set to last item if at the beginning
            if(count > 0)
            {
                count--;
            } 
            else 
            {
                count = nbSlide - 1;
            }

            // Add the active class to the new current item
            items[count].classList.add('slider-active');
        }

        // Add event listener for the left scroll button
        precedent.addEventListener('click', slidePrecedente);
    }
}

// Calls the function once the document has been loaded
document.addEventListener('DOMContentLoaded', function() 
{
    sliderCompetition('.slider', '.right', '.left');
    sliderCompetition('.slider2', '.right2', '.left2');
});

                                
                                       
                                    
                                        
                            
