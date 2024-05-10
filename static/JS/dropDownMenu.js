window.addEventListener('DOMContentLoaded', function() 
{
    /* Permet d'avoir les bords inférieurs de la dernière catégorie arrondis */
    var gridCountryElements = document.querySelectorAll('.container-grid-cate .grid-country');
    var lastGridCountryElement = gridCountryElements[gridCountryElements.length - 1];
    lastGridCountryElement.classList.add('last-border')
   
    /* Permet d'avoir une alternance de couleurs pour les catégories des leagues */
    gridCountryElements.forEach(function(grid, index) 
    {
        // Permet d'avoir une couleur uniforme avec la catégorie lors du défilement
        var nextElement = grid.nextElementSibling; 
        var leagues = nextElement.querySelectorAll('.grid-cate.text-check-box');

        if (index % 2 === 0) 
        {
            grid.classList.add('even');
            
            leagues.forEach(function(league)
            {
                league.classList.add('even');
            });
        } 
        else 
        {
            
            grid.classList.add('odd');
            
            leagues.forEach(function(league)
            {
                league.classList.add('odd');
            });
        }
    });

    /* Permet de dérouler la liste des leagues lorsqu'on clique sur une catégorie */
    gridCountryElements.forEach(function(countryElement) 
    {
        countryElement.addEventListener('click', function() 
        {
            /* Permet à la flèche de tourner */
            var arrow = countryElement.querySelector('.caret')
            arrow.classList.add('caret-rotate')

            /* Texte correspondant à l'identifiant des leagues */
            var countryId = this.textContent.trim();   //trim() supprimer les espaces blancs debut/fin

            /* On cherche les leagues correspondant à l'id */
            var selectedCategoryGrid = document.getElementById(countryId);
            
            if (selectedCategoryGrid.classList.contains('grid-categories-none')) 
            {
                selectedCategoryGrid.classList.remove('grid-categories-none');
                selectedCategoryGrid.classList.add('grid-categories-display');

                /* Changer la catégorie s'il y en a une autre en dessous de Other */
                if (countryId == 'Other')
                {
                    // Récupérer la dernière league avec l'id world
                    var lastCate = selectedCategoryGrid.lastElementChild
                
                    lastGridCountryElement.classList.remove('last-border');
                    lastCate.classList.add('last-border');
                }
            }
            else
            {
                selectedCategoryGrid.classList.remove('grid-categories-display');
                selectedCategoryGrid.classList.add('grid-categories-none');

                /* Permet à la flèche de tourner */
                var arrow = countryElement.querySelector('.caret')
                arrow.classList.remove('caret-rotate')

                if (countryId == 'Other')
                {
                    // Récupérer la dernière league avec l'id world
                    var lastCate = selectedCategoryGrid.lastElementChild
                
                    lastCate.classList.remove('last-border');
                    lastGridCountryElement.classList.add('last-border');
                }
        }
        });
    });

    /* Permet de sélectionner qu'une seule checkbox à la fois */
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');

    checkboxes.forEach(function(checkbox) 
    {
        checkbox.addEventListener('change', function() 
        {
            // Désélectionne toutes les autres cases à cocher
            checkboxes.forEach(function(cb) 
            {
                if (cb !== checkbox) 
                {
                    cb.checked = false;
                }
            });

            // Vérifiez si aucune case n'est cochée
            var aucunCoche = true;
            checkboxes.forEach(function(cb) 
            {
                if (cb.checked) 
                {
                    aucunCoche = false;
                }
            });

            // Si aucune case n'est cochée, nettoyez le conteneur
            if (aucunCoche) 
            {
                // Sélectionnez l'élément où vous souhaitez ajouter les threads
                var gridContainer = $('.container-futur-threads');

                // Videz d'abord le conteneur au cas où il contiendrait des éléments précédents
                gridContainer.empty();

                gridContainer.append(
                    '<div class="no-thread">' +
                        'No threads '+
                    '</div>'
                );
            }
            });
    });
});



