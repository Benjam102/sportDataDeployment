function displayMatches(targetContainer, matchesPerPage, button) 
{
    /**
     * Allows us to display more matches by a click on the button.
     *
     * @param {string} targetContainer Container containing the show more button.
     * @param {string} matchesPerPage Number of match to show initially.
     * @param {string} button button "Show more".
     */

    // Select all match elements within the target container
    const matches = targetContainer.querySelectorAll('.grid-h2h');

    // Initial number of visible matches
    let visibleMatches = 0; 

    // Count how many matches are currently visible
    matches.forEach(function(match) 
    {
        if (match.style.display == 'grid') 
        {
            visibleMatches++;
        }
    });

    // Increase the number of visible matches by the specified number per page
    visibleMatches += matchesPerPage;

    // Loop through each match element and update its display status
    matches.forEach((match, index) => 
    {
        if (index < visibleMatches) 
        {
            // Display the match if its index is within the number of visible matches
            match.style.display = 'grid'; 
        } 
        else 
        {
            // Hide any additional matches beyond the visible matches count
            match.style.display = 'none'; 
        }
    });

    // Show the "Show more" button only if there are hidden matches remaining to be displayed
    button.style.display = (visibleMatches < matches.length) ? '' : 'none';
}


function showMore(classButton, matchesPerPage)
{
    /**
     * Allows us to add an event on the buttons "Show more" in the section H2H of the match page.
     *
     * @param {string} classButton Container containing all the "Show more" button.
     * @param {string} matchesPerPage Number of match to show initially.
     */

    // Select all "See More" buttons by their class
    const loadMoreButtons = document.querySelectorAll(classButton);

    // Iterate through each "See More" button and add an event listener
    loadMoreButtons.forEach(function(button) 
    {
        // Get the target container ID from the button's data attribute
        const targetContainerId = button.getAttribute('data-target');
        // Get the target container element by its ID
        const targetContainer = document.getElementById(targetContainerId);

        if (targetContainer) 
        {
            // Display the initial set of matches when the page loads
            displayMatches(targetContainer, matchesPerPage, button);

            // Handle the click event on the "See More" button
            button.addEventListener('click', function() 
            {
                // Update the display of matches
                displayMatches(targetContainer, matchesPerPage, button);
            });
        }
    });
}


document.addEventListener('DOMContentLoaded', function() 
{
    showMore('.under-category-content .button-more', 3);
});