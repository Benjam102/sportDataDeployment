function selectDropDowns(container)
{
    /**
     * Function to manage a select box.
     *
     * @param {string} container id of the subcategory where there is a selectBox.
     */

    const containerD = document.getElementById(container);
    var dropdowns = null;

    if (containerD)
    {
        // Get the dropdown container element within the specified container
        var dropdowns = containerD.querySelector('.container-select');
    }
    
    if (dropdowns)
    {
        // Get all necessary elements within the dropdown container
        const select = dropdowns.querySelector('.select');            // drop box initially
        const caret = dropdowns.querySelector('.caret');              // arrow
        const annees = dropdowns.querySelector('.val');               // drop-down menu
        const li_ = dropdowns.querySelectorAll('.val li');            // marker on this drop down
        const selected = dropdowns.querySelector('.selected');        // Category selected by the user with a default initially

        // Add event listener to the select element
        select.addEventListener('click', function() 
        {
            // When clicking on the select box, toggle the rotation of the caret
            caret.classList.toggle('caret-rotate');
            
            // When clicking on the select box, toggle the dropdown menu
            annees.classList.toggle('val-open');
        });
        
        // Add event listener to each list item in the dropdown
        li_.forEach(function(li) 
        {
            li.addEventListener('click', function() 
            {
                // Set the selected text to the clicked list item's text
                selected.innerText = li.innerText;
        
                // Toggle the rotation of the caret
                caret.classList.toggle('caret-rotate');
        
                // Toggle the dropdown menu
                annees.classList.toggle('val-open');
        
                // Remove the active class from all list items
                li_.forEach(function(li) 
                {
                    li.classList.remove('active');
                });
        
                // Add the active class to the clicked list item
                li.classList.add('active');
            });
        });
    }
}

// Calls the function once the document has been loaded
document.addEventListener('DOMContentLoaded', function() 
{
    selectDropDowns('content-cat3.1');
});


