/**
 * Allows us to have only one checkboxe that can be selected at a time.
 *
 * @param {string} containerGeneral Principal container of the drop down menu.
 * @param {string} containerTheadsTchats Container of the leagues/threads/tchats that are displayed when you check a checkbox.
 * @param {string} page Indicate the page (upcoming or fora).
 */
function checkboxOnlyOne(containerGeneral, containerTheadsTchats, page)
{
    var checkboxes = document.querySelectorAll(containerGeneral + ' input[type="checkbox"]');

    checkboxes.forEach(function(checkbox) 
    {
        checkbox.addEventListener('change', function() 
        {
            // Deselects all checkboxes except the selected one
            checkboxes.forEach(function(cb) 
            {
                if (cb !== checkbox) 
                {
                    cb.checked = false;
                }
            });

            // Verify that no checkbox is checked
            var aucunCoche = true;
            checkboxes.forEach(function(cb) 
            {
                if (cb.checked) 
                {
                    aucunCoche = false;
                }
            });

            if (aucunCoche) 
            {
                // Select containerTheadsTchats where we want to add the threads/tchats
                var gridContainer = $(containerTheadsTchats);

                // Empty the container first
                gridContainer.empty();

                // Add 'Nothing is selected.'
                if(page == 'fora')
                {
                    gridContainer.append(
                        '<div class="no-thread">' +
                            'Nothing is selected.'+
                        '</div>'
                    );
                }
                else if (page == 'upcoming')
                {
                    gridContainer.append(
                        '<div class="no-match">' +
                            'Nothing is selected.'+
                        '</div>'
                    );
                }
            }
        });
    });
}

/**
 * Allows us to remove all event listeners of checkboxes to avoid conflicts.
 *
 * @param {string} containerGeneral Principal container of the drop down menu.
 */
function removeListenerCheckBox(containerGeneral)
{
    var checkboxes = document.querySelectorAll(containerGeneral + ' input[type="checkbox"]');

    // Remove all event listeners by replacing each checkbox with a clone of itself
    checkboxes.forEach(function(checkbox) 
    {
        var newCheckbox = checkbox.cloneNode(true);
        checkbox.parentNode.replaceChild(newCheckbox, checkbox);
    });
}

/**
 * Allows parts containing checkboxes to function properly (drop down menu).
 *
 * @param {string} containerGeneral Principal container of the drop down menu.
 * @param {string} containerTheadsTchats Container of the threads/tchats that are displayed when you check a checkbox.
 * @param {string} lastId Id of the last container in the drop-down menu.
 * @param {string} page Indicate the page (upcoming or fora).
 */
function initializeDropDownMenu(containerGeneral, containerTheadsTchats, lastId, page) 
{
    // Allows the bottom edges of the last category (id = lastId) to be rounded off  
    var gridCategoryElements = document.querySelectorAll(containerGeneral + ' .grid-category');
    var lastGridCategoryElement = gridCategoryElements[gridCategoryElements.length - 1];

    if (lastGridCategoryElement != null)
    {
        lastGridCategoryElement.classList.add('last-border');
    }
    
    // Alternating colours for categories : International, Club...
    gridCategoryElements.forEach(function(categoryElement, index) 
    {
        var nextElement = categoryElement.nextElementSibling; 
        var leagues = nextElement.querySelectorAll('.grid-league-tchat');
    
        if (index % 2 === 0) 
        {
            categoryElement.classList.add('even');
            
            // Enables the colour of the leagues/tchats to be consistent with their category when scrolling the menu
            leagues.forEach(function(league)
            {
                league.classList.add('even');
            });
        } 
        else 
        {
            
            categoryElement.classList.add('odd');
            
            // Enables the colour of the leagues/tchats to be consistent with their category when scrolling the menu
            leagues.forEach(function(league)
            {
                league.classList.add('odd');
            });
        }
    });

    // Scrolls the list of leagues/tchat when you click on a category 
    gridCategoryElements.forEach(function(categoryElement) 
    {
        categoryElement.addEventListener('click', function() 
        {
            // Allows the arrow to turn through 180°
            var arrow = categoryElement.querySelector('.caret');
            arrow.classList.add('caret-rotate');

            // Text corresponding to the leagues/tchats identifier 
            var countryId = this.textContent.trim();                        //trim() remove leading/trailing white spaces

            // Search for leagues/tchats matching the id
            var selectedCategoryGrid = document.getElementById(countryId);
            
            if (selectedCategoryGrid.classList.contains('leagues-tchats-none')) 
            {
                selectedCategoryGrid.classList.remove('leagues-tchats-none');
                selectedCategoryGrid.classList.add('leagues-tchats-display');

                // Change the rounding if the last class in the drop-down menu is no longer recent/general 
                if (countryId == lastId)
                {
                    // Retrieve the latest league/tchat
                    var lastCate = selectedCategoryGrid.lastElementChild
                
                    lastGridCategoryElement.classList.remove('last-border');
                    lastCate.classList.add('last-border');
                }
            }
            else
            {
                selectedCategoryGrid.classList.remove('leagues-tchats-display');
                selectedCategoryGrid.classList.add('leagues-tchats-none');

                // Allows the arrow to turn through 180° 
                var arrow = categoryElement.querySelector('.caret')
                arrow.classList.remove('caret-rotate')

                // Change the rounding if the last class in the drop-down menu is no longer other/general
                if (countryId == lastId)
                {
                    // Retrieve the latest league/tchat
                    var lastCate = selectedCategoryGrid.lastElementChild
                
                    lastCate.classList.remove('last-border');
                    lastGridCategoryElement.classList.add('last-border');
                }
            }
        });      
    });

    // For each group of checkboxes in their containerGeneral, only one can be selected at a time   
    checkboxOnlyOne(containerGeneral, containerTheadsTchats, page);
}

// Calls the function once the document has been loaded
document.addEventListener('DOMContentLoaded', function() 
{
    // Threads
    initializeDropDownMenu('.container-grid-cate', '.container-futur-threads', 'Closest', 'fora');

    // Tchats
    initializeDropDownMenu('.container-grid-cate-tchat', '.container-futur-tchats', 'General', 'fora');

    // Matches
    initializeDropDownMenu('.container-grid-cate-matches', '.container-futur-matches', 'Closest', 'upcoming');
});


