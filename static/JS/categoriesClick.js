
// Pour les categories 
document.addEventListener('DOMContentLoaded', function() {
    const liElements = document.querySelectorAll('.details li');

    function showContentById(id) {
        const contentId = `content-${id}`;

        const allContent = document.querySelectorAll('.category-content');
        allContent.forEach(function(content) {
            content.style.display = 'none';
        });

        const selectedContent = document.getElementById(contentId);
        if (selectedContent) {
            selectedContent.style.display = 'block';
        }

        liElements.forEach(function(li) {
            if (li.getAttribute('id') === id) {
                li.classList.add('active');
            } else {
                li.classList.remove('active');
            }
        });

        // Enregistrer l'ID de la catégorie sélectionnée dans localStorage
        localStorage.setItem('selectedCategoryId', id);
    }

    // Récupérer l'ID de la catégorie sélectionnée depuis localStorage
    const selectedCategoryId = localStorage.getItem('selectedCategoryId');
    //console.log(selectedCategoryId)

    // Afficher le contenu correspondant à l'ID stocké dans localStorage
    if (selectedCategoryId !== null && selectedCategoryId !== '') {
        showContentById(selectedCategoryId);
    } else {
        // Par défaut, afficher le contenu correspondant à l'ID "1"
        showContentById('1');
    }

    liElements.forEach(function(li) {
        li.addEventListener('click', function() {
            const id = li.getAttribute('id');
            showContentById(id);
        });
    });
});

// Pour les sous categories
document.addEventListener('DOMContentLoaded', function() 
{
    // Sélectionner toutes les catégories et initialiser les contenus par défaut
    const categories = document.querySelectorAll('.category-content');

    function showContentById(categoryId, id) 
    {
        const contentId = 'content-' + id;

        // Masquer tous les contenus de la catégorie spécifique
        const allContent = document.querySelectorAll('#' + categoryId + ' .under-category-content');

        allContent.forEach(function(content) {
            content.style.display = 'none';
        });

        // Afficher le contenu spécifique correspondant à l'id
        const selectedContent = document.getElementById(contentId);
        if (selectedContent) {
            selectedContent.style.display = 'block';
        }

        // Gérer les classes actives pour les éléments <li>
        const liElements = document.querySelectorAll('#' + categoryId + ' .informations-matches li');
        //console.log(liElements)
        liElements.forEach(function(li) {
            if (li.getAttribute('id') === id) {
                li.classList.add('active');
            } else {
                li.classList.remove('active');
            }
        });
    }

    // Parcourir toutes les catégories et définir les comportements des éléments <li>
    categories.forEach(function(category) 
    {
        const liElements = category.querySelectorAll('.informations-matches li');

        if (liElements.length > 0) 
        {
            // Afficher le contenu par défaut pour chaque catégorie
            const defaultContentId = liElements[0].getAttribute('id');
            showContentById(category.id, defaultContentId);

            // Ajouter un écouteur d'événement à chaque élément <li>
            liElements.forEach(function(li) {
                li.addEventListener('click', function() {
                    const id = li.getAttribute('id');
                    showContentById(category.id, id);
                });
            });
        }
        
    });
});

/*document.addEventListener('DOMContentLoaded', function() {
    // Sélectionnez tous les éléments <li> sous la classe 'details'
    const liElements = document.querySelectorAll('.details li');

    // Fonction pour afficher le contenu correspondant à un ID donné
    function showContentById(id) {
        const contentId = `content-${id}`;

        // Sélectionnez tous les éléments de contenu et cachez-les
        const allContent = document.querySelectorAll('.category-content');
        allContent.forEach(function(content) {
            content.style.display = 'none';
        });

        // Affichez uniquement le contenu correspondant à l'ID spécifié
        const selectedContent = document.getElementById(contentId);
        if (selectedContent) {
            selectedContent.style.display = 'block';
        }

        // Ajoutez la classe 'active' à l'élément <li> correspondant à l'ID sélectionné
        liElements.forEach(function(li) {
            if (li.getAttribute('id') === id) {
                li.classList.add('active');
            } else {
                li.classList.remove('active');
            }
        });
    }

    // Par défaut, affichez le contenu correspondant à l'ID "1"
    showContentById('1');

    // Ajoutez un gestionnaire d'événement 'click' à chaque élément <li>
    liElements.forEach(function(li) {
        li.addEventListener('click', function() {
            const id = li.getAttribute('id');
            showContentById(id); // Affichez le contenu correspondant à l'ID cliqué
        });
    });
});
*/