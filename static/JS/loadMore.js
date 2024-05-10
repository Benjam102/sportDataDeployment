document.addEventListener('DOMContentLoaded', function() {
    // Sélectionnez tous les boutons "Voir plus" par leur classe
    const loadMoreButtons = document.querySelectorAll('.under-category-content .button-more');
    const matchesPerPage = 1; // Nombre de matches à afficher par page

    // Parcourez chaque bouton "Voir plus" et ajoutez un gestionnaire d'événements
    loadMoreButtons.forEach(function(button) {
        const targetContainerId = button.getAttribute('data-target');
        const targetContainer = document.getElementById(targetContainerId);

        if (targetContainer) {
            // Fonction pour afficher les matches en fonction du nombre visible actuel
            function displayMatches() {
                const matches = targetContainer.querySelectorAll('.grid-tab');

                visibleMatches = 0; // Nombre initial de matches visibles

                matches.forEach(function(match) {
                    if (match.style.display == 'grid') {
                        visibleMatches++;
                    }
                });

                visibleMatches += matchesPerPage;

                matches.forEach((match, index) => {
                    if (index < visibleMatches) {
                        match.style.display = 'grid'; // Afficher le match
                    } else {
                        match.style.display = 'none'; // Masquer les matches supplémentaires
                    }
                });

                // Afficher le bouton "Voir plus" uniquement s'il y a des matches cachés à afficher
                button.style.display = (visibleMatches < matches.length) ? '' : 'none';
            }

            // Afficher les premiers matches lors du chargement initial
            displayMatches();

            // Gérer le clic sur le bouton "Voir plus"
            button.addEventListener('click', function() {
                visibleMatches += matchesPerPage; // Augmenter le nombre de matches visibles
                displayMatches(); // Actualiser l'affichage des matches
            });
        }
    });
});







/*document.addEventListener('DOMContentLoaded', function() {
    const matchesContainer = document.getElementById('matchesContainer');
    const loadMoreButton = document.getElementById('loadMoreButton');
    const matchesPerPage = 1; // Nombre de matches à afficher par page
    let visibleMatches = matchesPerPage; // Nombre initial de matches visibles

    // Fonction pour afficher les matches en fonction du nombre visible actuel
    function displayMatches() {
        const matches = matchesContainer.querySelectorAll('.grid-tab');
        matches.forEach((match, index) => {
            if (index < visibleMatches) {
                match.style.display = 'grid'; // Afficher le match
            } else {
                match.style.display = 'none'; // Masquer les matches supplémentaires
            }
        });

        // Afficher le bouton "Voir plus" uniquement s'il y a des matches cachés à afficher
        loadMoreButton.style.display = (visibleMatches < matches.length) ? '' : 'none';
    }

    // Afficher les premiers matches lors du chargement initial
    displayMatches();

    // Gérer le clic sur le bouton "Voir plus"
    loadMoreButton.addEventListener('click', function() {
        visibleMatches += matchesPerPage; // Augmenter le nombre de matches visibles
        displayMatches(); // Actualiser l'affichage des matches
    });
});

Pour 1 */