
// For categories
document.addEventListener('DOMContentLoaded', function() 
{
    const liElements = document.querySelectorAll('.details li');
    const sideMenu = document.querySelector('.side-menu');
    const sideCaret = document.querySelector('.side-caret');
    const sideBar = document.querySelector('.side-bar');
    
    function showContentById(id) {
        const contentId = `content-${id}`;

        const allContent = document.querySelectorAll('.category-content');
        allContent.forEach(function(content) 
        {
            content.style.display = 'none';
        });

        const selectedContent = document.getElementById(contentId);
        if (selectedContent) {
            selectedContent.style.display = 'block';
        }

        liElements.forEach(function(li) 
        {
            if (li.getAttribute('id') === id) 
            {
                li.classList.add('active');
                
                sideMenu.classList.remove('open');
                sideCaret.classList.remove('side-caret-rotate');
                sideBar.style.display = 'none';
            } 
            else 
            {
                li.classList.remove('active');
            }
        });

        // Save the selected category ID in localStorage
        localStorage.setItem('selectedCategoryId', id);
    }

    // Retrieve the selected category ID from localStorage
    const selectedCategoryId = localStorage.getItem('selectedCategoryId');

    // Display the content corresponding to the ID stored in localStorage
    if (selectedCategoryId !== null && selectedCategoryId !== '') 
    {
        showContentById(selectedCategoryId);
    } 
    else 
    {
        // By default, display the content corresponding to ID "1"
        showContentById('1');
    }

    liElements.forEach(function(li) 
    {
        li.addEventListener('click', function() 
        {
            const id = li.getAttribute('id');
            showContentById(id);
        });
    });
});

// For subcategories
document.addEventListener('DOMContentLoaded', function() 
{
    const sideMenu = document.querySelector('.side-menu');
    const sideCaret = document.querySelector('.side-caret');
    const sideBar = document.querySelector('.side-bar');
    
    // Select all categories and initialize default contents
    const categories = document.querySelectorAll('.category-content');

    function showContentById(categoryId, id) 
    {
        const contentId = 'content-' + id;

        // Hide all contents of the specific category
        const allContent = document.querySelectorAll('#' + categoryId + ' .under-category-content');

        allContent.forEach(function(content) {
            content.style.display = 'none';
        });

        // Display the specific content corresponding to the id
        const selectedContent = document.getElementById(contentId);
        if (selectedContent) {
            selectedContent.style.display = 'block';
        }

        // Manage active classes for <li> elements
        const liElements = document.querySelectorAll('#' + categoryId + ' .informations-matches li');
        //console.log(liElements)
        liElements.forEach(function(li) {
            if (li.getAttribute('id') === id) 
            {
                li.classList.add('active');
                sideMenu.classList.remove('open');
                sideCaret.classList.remove('side-caret-rotate');
                sideBar.style.display = 'none';
            } 
            else {
                li.classList.remove('active');
            }
        });
    }

    // Iterate through all categories and set up behaviors for <li> elements
    categories.forEach(function(category) 
    {
        const liElements = category.querySelectorAll('.informations-matches li');

        if (liElements.length > 0) 
        {
            // Display default content for each category
            const defaultContentId = liElements[0].getAttribute('id');
            showContentById(category.id, defaultContentId);

            // Add event listener to each <li> element
            liElements.forEach(function(li) {
                li.addEventListener('click', function() {
                    const id = li.getAttribute('id');
                    showContentById(category.id, id);
                });
            });
        }
        
    });
});





