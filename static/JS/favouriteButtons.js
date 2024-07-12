
function addFavourite(formButton)
{
    // Retrieve the URL from the data-url attribute of the form
    var url = $(formButton).data('url-add');
    
    // Collect form data
    var formData = $(formButton).serialize();

    $.ajax({
        url: url,  // Utiliser l'URL dynamique
        type: 'POST',
        data: formData,
        success: function (response)  
        {
            //Recuperation d un format de token
            var categoryOther = document.getElementById('Other');
            var token = ((categoryOther.firstElementChild).querySelector('form')).querySelector('input');
            
            var cloneToken = token.cloneNode(true);
            console.log(cloneToken);
            var categoryFavourites = document.getElementById('Favourites');
            
            var html = '<div class="grid-league-tchat">' +
                            '<form method="post" class="box-svg" data-url-add="/accounts/add/favourite/' + response.slug_thread_league + 
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

            categoryFavourites = (document.getElementById('Favourites')).lastElementChild;

            $.getScript('/static/JS/dropDownMenu.js', function() {
                initializeDropDownMenu('.container-grid-cate-matches', '.container-futur-matches', 'Recent', 'upcoming');
            });
            
            $.getScript('/static/JS/matchesCategory.js', function() {
                
            });
            
            
            $.getScript('/static/JS/favouriteButtons.js', function() {
                
                var categoryNewFavourites = document.getElementById('Favourites');
                var formAdded = categoryNewFavourites.lastElementChild.querySelector('form');
                console.log(formAdded);
                
                listenerButton(formAdded);
            });
            
        },
        error: function(error) 
        {
            // Log any errors to the console
            console.log(error); 
        }
    });
}


function removeFavourite(formButton)
{
    // Retrieve the URL from the data-url attribute of the form
    var url = $(formButton).data('url-remove');

    // Collect form data
    var formData = $(formButton).serialize();

    $.ajax({
        url: url,  // Utiliser l'URL dynamique
        type: 'POST',
        data: formData,
        success: function (response)  
        {   
            var boxIcon = formButton.querySelector('box-icon');
            var idBoxicon = boxIcon.id;
    
            if(idBoxicon.startsWith('fav-'))
            {
                var boxSvg = document.getElementById(response.slug_thread_category + '-' + response.slug_thread_league);
               
                boxSvg.setAttribute('type', 'regular');
                boxSvg.setAttribute('color', '#344D59');

                var parentDiv = formButton.parentNode;
                console.log(parentDiv);
                // Supprimer l'élément parent du DOM
                parentDiv.remove();
            }
            else
            {
                var boxSvg = document.getElementById('fav-' + response.slug_thread_category + '-' + response.slug_thread_league);
            
                boxSvg.setAttribute('type', 'regular');
                boxSvg.setAttribute('color', '#344D59');
            }
            
            
            //var categoryFavourites = document.getElementById('Favourites');

        },
        error: function(error) 
        {
            // Log any errors to the console
            console.log(error); 
        }
    });
}

function listenerButton(form)
{
    form.addEventListener('click', function() 
    {
        var boxIcon = form.querySelector('.star-fav');
        var boxIconType = boxIcon.getAttribute('type');
        console.log(boxIcon);

        if(boxIconType == 'solid') // jaune
        {
            boxIcon.setAttribute('type', 'regular');
            boxIcon.setAttribute('color', '#344D59');
            
            removeFavourite(form);
        }
        else if (boxIconType == 'regular')
        {
            boxIcon.setAttribute('type', 'solid');
            boxIcon.setAttribute('color', '#e9c46a');

            addFavourite(form);
        }
    });
}


function favouriteButtons() 
{
    var favouriteButtons = document.querySelectorAll('.box-svg');
    
    favouriteButtons.forEach(function(b) 
    {
        listenerButton(b);
    });
}


document.addEventListener('DOMContentLoaded', function() {
    // Appeler votre fonction une fois que le document est chargé
    favouriteButtons();
});