/**
 * Allows us to add a favourite for a user.
 *
 * @param {string} formButton form of the 'star' pressed corresponding to the competition we want to add in our favourites.
 */
function addFavourite(formButton)
{
    // Retrieve the URL from the data-url attribute of the form
    var url = $(formButton).data('url-add');
    
    // Collect form data. We use it just to have the token CRSF
    var formData = $(formButton).serialize();

    // Making the Ajax request
    $.ajax(
    {
        url: url, 
        type: 'POST',
        data: formData,
        success: function (response)  
        {
            if (response != null)
            {
                // Recovering a CRSF token format to display the new favourite
                var categoryOther = document.getElementById('Other');
                var token = ((categoryOther.firstElementChild).querySelector('form')).querySelector('input');
                var cloneToken = token.cloneNode(true);
                
                var categoryFavourites = document.getElementById('Favourites');
                var previousElement = categoryFavourites.previousElementSibling;

                var html = '';
                // Matching the right colour to the category (International, Club...)
                if (previousElement.classList.contains('odd'))
                {
                    html += '<div class="grid-league-tchat odd">';
                }
                else if(previousElement.classList.contains('even'))
                {
                    html += '<div class="grid-league-tchat even">';
                }

                // Creating favourites (We hardcode the url because js doesn't interpret django tags)
                html +=     '<form method="post" class="box-svg" data-url-add="/accounts/add/favourite/' + response.slug_thread_league + 
                            '" data-url-remove="/accounts/remove/favourite/' + response.slug_thread_league + '">' +
                                cloneToken.outerHTML +
                                '<box-icon name="star" color="#e9c46a" type="solid" class="star-fav" id="fav-' + response.slug_thread_category + '-' + response.slug_thread_league + '"></box-icon>' +
                            '</form>' +
                            '<label class="text-check-box" for="fav-' + response.slug_thread_league + '">' +
                                '<div class="league-tchat">' +
                                    '<div class="name-compe">' + response.thread_league + '</div>' +
                                '</div>' +
                                '<input type="checkbox" class="category-checkbox" id="fav-' + response.slug_thread_league + '" data-url="/display/matches/' + response.slug_thread_league + '">' +
                            '</label>' +
                        '</div>';

                $(categoryFavourites).append(html);
                
                // What to do when a checbox is selected
                $.getScript('/static/JS/matchesCategory.js', function() 
                {
                    
                });
                
                // Adding listener for checkboxes
                $.getScript('/static/JS/dropDownMenu.js', function() 
                {
                    // Removing all listeners before putting them back in
                    removeListenerCheckBox('.container-grid-cate-matches');

                    // Adding listener
                    checkboxOnlyOne('.container-grid-cate-matches', '.container-futur-threads', 'upcoming');
                    checkboxOnlyOne('.container-grid-cate-matches', '.container-futur-threads', 'fora');
                });

                // Adding a listener on the star of the competition we have just set up
                $.getScript('/static/JS/favouriteButtons.js', function() 
                {
                    var categoryNewFavourites = document.getElementById('Favourites');
                    var formAdded = categoryNewFavourites.lastElementChild.querySelector('form');
                    
                    listenerButton(formAdded);
                });
            }
        },
        error: function(error) 
        {
            // Log any errors to the console
            console.log(error); 
        }
    });
}

/**
 * Allows us to remove a favourite for a user.
 *
 * @param {string} formButton form of the 'star' pressed corresponding to the competition we want to remove from our favourites.
 */
function removeFavourite(formButton)
{
    // Retrieve the URL from the data-url attribute of the form
    var url = $(formButton).data('url-remove');

    // Collect form data. We use it just to have the token CRSF
    var formData = $(formButton).serialize();

    // Making the Ajax request
    $.ajax({
        url: url, 
        type: 'POST',
        data: formData,

        success: function (response)  
        {   
            if (response != null)
            {
                var boxIcon = formButton.querySelector('box-icon');
                var idBoxicon = boxIcon.id;
                
                // Case we remove the competition from the category favourite
                if(idBoxicon.startsWith('fav-'))
                {
                    // We need to change the star of the same competition in another category
                    var boxSvg = document.getElementById(response.slug_thread_category + '-' + response.slug_thread_league);
                
                    boxSvg.setAttribute('type', 'regular');     // Just putting back the outline of the star
                    boxSvg.setAttribute('color', '#344D59');    // Put back the blue star outline

                    // Delete the parent DOM element
                    var parentDiv = formButton.parentNode;
                    parentDiv.remove();
                }
                // Case we remove the competition from another favourite
                else
                {
                    var boxSvg = document.getElementById('fav-' + response.slug_thread_category + '-' + response.slug_thread_league);

                    // Delete the parent DOM element
                    var parentDiv = (boxSvg.parentNode).parentNode; // form -> grid-league-tchat
                    parentDiv.remove();
                }
            }
            
        },
        error: function(error) 
        {
            // Log any errors to the console
            console.log(error); 
        }
    });
}

/**
 * Allows us to add a listener to a form containing the 'star'.
 *
 * @param {string} form form of a 'star' (corresponding to a competition).
 */
function listenerButton(form)
{
    form.addEventListener('click', function() 
    {
        var boxIcon = form.querySelector('.star-fav');
        var boxIconType = boxIcon.getAttribute('type');

        // Case we want to remove a competition from our favourites
        if(boxIconType == 'solid') 
        {
            boxIcon.setAttribute('type', 'regular');   // Just putting back the outline of the star pressed
            boxIcon.setAttribute('color', '#344D59');  // Put back the blue star outline pressed
            
            removeFavourite(form);
        }
        // Case we want to add a competition in our favourites
        else if (boxIconType == 'regular')
        {
            boxIcon.setAttribute('type', 'solid');      // Filling out the star
            boxIcon.setAttribute('color', '#e9c46a');   // Yellow star

            addFavourite(form);
        }
    });
}


/**
 * Allows us to Add a listener to all our forms containing a 'star'.
 */
function favouriteButtons() 
{
    var favouriteButtons = document.querySelectorAll('.box-svg');
    
    favouriteButtons.forEach(function(b) 
    {
        listenerButton(b);
    });
}

// Calls the function once the document has been loaded
document.addEventListener('DOMContentLoaded', function() 
{
    favouriteButtons();
});