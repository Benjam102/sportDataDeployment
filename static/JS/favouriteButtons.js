
function addFavourite()
{
    $.ajax({
        url: url,  // Utiliser l'URL dynamique
        type: 'POST',
        data: {
            'star_id': starId,
            'csrfmiddlewaretoken': '{{ csrf_token }}' // Inclure le token CSRF
        },
        success: function(data) {
            // Faites quelque chose avec les données reçues
            console.log(data);
            // Par exemple, mettre à jour le contenu de la page
        }
    });
}



document.addEventListener('DOMContentLoaded', function() 
{
    var favouriteButtons = document.querySelectorAll('.box-svg');
    
    favouriteButtons.forEach(function(b) 
    {
        b.addEventListener('click', function() 
        {
            var boxIcon = b.querySelector('.star-fav');
            var boxIconType = boxIcon.getAttribute('type');

            if(boxIconType == 'solid')
            {
                boxIcon.setAttribute('type', 'regular');
                boxIcon.setAttribute('color', '#344D59');
            }
            else
            {
                boxIcon.setAttribute('color', '#e9c46a');
                boxIcon.setAttribute('type', 'solid');
            }
        });
    });
});