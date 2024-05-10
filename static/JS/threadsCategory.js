$(document).ready(function () 
{
    $('.category-checkbox').change(function () 
    {
        if (this.checked) 
        {
            var checkboxId = $(this).attr('id');
            
            // Récupérer l'URL depuis l'attribut data-url du formulaire
            var url1 = $(this).data('url');
         

            $.ajax({
                type: 'GET',
                url: url1,
                data: {
                    checkboxId: checkboxId
                },

                success: function (response) 
                {
                    // Sélectionnez l'élément où vous souhaitez ajouter les threads
                    var gridContainer = $('.container-futur-threads');

                    // Videz d'abord le conteneur au cas où il contiendrait des éléments précédents
                    gridContainer.empty();

                    // Parcourez les données des threads et construisez la structure HTML pour chaque thread
                    if(response.sorted_threads_info)
                    {
                        response.sorted_threads_info.forEach(function (thread) {
                            
                            if(thread.latest_comment != "None")
                            {
                                date_thread = (thread.latest_comment).substring(0, 10)

                                if(response.today_date == date_thread)
                                {
                                    date_ = (thread.latest_comment).substring(11, 16)
                                    
                                }
                                else
                                {
                                    date_ = date_thread
                                } 
                            }
                            else
                            {
                                date_ = "/"
                            }

                            if(thread.closed_thread == false)
                            {
                                o_c = 'Opened';
                            }
                            else
                            {
                                o_c = "Closed";
                            }
                            
                            
                            var path = `onclick=window.location.href="{% url 'threads_' slug_type=thread.slug_country slug_category=thread.category_selected slug_thread=thread.slug_thread %}"`;
                            

                            gridContainer.append(
                                '<div class="grid-threads-recents" onclick=window.location.href="/fora' + '/' + thread.slug_country + '/' + thread.category_selected + '/' + thread.slug_thread + '">' +
                                    '<div class="element-grid">' +
                                        thread.slug_thread +
                                    '</div>' +
                                    '<div>' +
                                        date_+
                                    '</div>' +
                                    '<div class="element-grid">' +
                                        thread.comments_count +                   
                                    '</div>' +
                                    '<div class="element-grid">' +
                                        o_c +
                                    '</div>' +
                                '</div>')
                        });
                    }
                    else
                    {
                        gridContainer.append(
                            '<div class="no-thread">' +
                                response.no_data +
                            '</div>'
                        )
                    }
                    
                },
                error: function(error) {
                    console.log(error); // Log any errors to the console
                }
            });
        } 
        else 
        {
            
        }
    });
});