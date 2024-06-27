function sideBarUnderContent(c, underC)
{
    /**
     * Allows us to manage the elements of the sidebar for categories (H2H, Standings) with sub-categories (Overall, Home...).
     *
     * @param {object} c Principal category.
     * @param {object} underC sub-category of the category c.
     */

    // For display the principal category and the sub-category
    var html = '<a href="#debut" class="grid-section">' +        // #debut allows us to go on the top of the page
                    '<span class="section">' +
                        c.getAttribute('name') +
                    '</span>' +
                    '<span class="subsection">' +
                        underC.getAttribute('name') +
                    '</span>' +
                '</a>';

                // For display all parts of my sub-category
                const sumUnderBanners = underC.querySelectorAll('.banner');

                sumUnderBanners.forEach(function(underTitle) 
                {
                    html += '<a href="#'+ underTitle.id + '" ' + 'class="grid-side-bar">' +
                                underTitle.id +
                            '</a>';
                });

    return html;
}

function sideBarContent(c)
{
    /**
     * Allows us to manage the elements of the sidebar for categories (H2H, Standings) without sub-categories (Overall, Home...).
     *
     * @param {object} c Principal category without sub-categories.
     */

    // For display the principal category
    var html = '<a href="#debut" class="grid-section">' + // #debut allows us to go on the top of the page
                    '<span class="section">' +
                            c.getAttribute('name') +
                    '</span>' +
                '</a>';

                // For display all parts of my category
                const sumBanners = c.querySelectorAll('.banner');
                
                sumBanners.forEach(function(title) 
                {
                    html += '<a href="#'+ title.id + '" ' + 'class="grid-side-bar">' +
                                title.id +
                            '</a>';
                });
    
    return html;
}

function sidebar()
{
    /**
     * Allows us to manage the the sidebar of the match page.
     */

    const sideMenu = document.querySelector('.side-menu');
    const sideCaret = sideMenu.querySelector('.side-caret');
    const sideBar = document.querySelector('.side-bar');

    var html = '';

    sideMenu.addEventListener('click', function() 
    {
        // When we click on the arrow, the arrow rotates and the menu is displayed alongside the side bar. 
        sideCaret.classList.toggle('side-caret-rotate');
        sideMenu.classList.toggle('open');

        // We display the sidebar if sideMenu is open
        if (sideMenu.classList.contains('open')) 
        {
            sideBar.style.display = 'block';
        } else 
        {
            sideBar.style.display = 'none';
        }

        // Principal categories (Summary, H2H, Standings)
        const allContent = document.querySelectorAll('.category-content');
        
        allContent.forEach(function(c)
        {
            if (c.style.display == 'block')
            {
                const allUnderContent = c.querySelectorAll('.under-category-content');
                
                // Sub-categories or not
                if(allUnderContent.length > 0)
                {
                    $(sideBar).empty();

                    allUnderContent.forEach(function(underC) 
                    {
                        if (underC.style.display == 'block')
                        {
                            html = sideBarUnderContent(c, underC);
                        }
                    });

                    $(sideBar).append(html);
                }
                else
                {
                    $(sideBar).empty();

                    html = sideBarContent(c);
                    
                    $(sideBar).append(html);
                }
                
            }
        });

    });
}

$(document).ready(function()
{ 
    sidebar();
});
