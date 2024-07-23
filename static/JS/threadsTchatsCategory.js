$(document).ready(function () 
{
    $('.category-checkbox').change(function () 
    {
        if (this.checked) 
        {
            var checkboxId = $(this).attr('id');
            
            // Get the URL from the data-url attribute of the form
            var url1 = $(this).data('url');
        
            $.ajax({
                type: 'GET',
                url: url1,
                data: {
                    checkboxId: checkboxId
                },
                // Make an AJAX GET request to the URL
                success: function (response) 
                {
                    if (response != null)
                    {
                        // Case where we want to diplay a tchat
                        if(checkboxId.substring(0, 5) == 'tchat')
                        {
                            // Choose the container
                            var gridContainer = $('.container-futur-tchats');
        
                            // First, empty the container in case it contains previous elements
                            gridContainer.empty();
    
                            if(response.latest_post_date != "None")
                            {
                                // Get the date from the latest post date in the response
                                date_tchat = (response.latest_post_date).substring(0, 10)
                                
                               // If the date is today, just show the time
                               if(response.today_date == date_thread)
                                {
                                    date_ = (thread.latest_comment).substring(11, 16)
                                }
                                else if (response.yesterday_date == date_thread)
                                {
                                    date_ = 'Yesterday'
                                }
                                else
                                {
                                    // Otherwise, show the full date
                                    date_ = date_thread
                                } 
                            }
                            else
                            {
                                // If there is no latest post date, show a slash
                                date_ = "/"
                            }
                            
                            // Append the new chat element to the container
                            gridContainer.append(
                                '<div class="grid-tchat" onclick=window.location.href="/fora' + '/tchats/' + response.tchat_slug_category + '/' + response.tchat_slug_name + '">' +
                                    '<div class="element-grid">' +
                                        response.tchat_slug_name +
                                    '</div>' +
                                    '<div>' +
                                        date_ + 
                                    '</div>' +
                                    '<div class="element-grid">' +
                                        response.post_count +                   
                                    '</div>' +
                                '</div>'
                            )
    
                        }
                        // Case where we want to diplay threads
                        else if ((checkboxId.substring(0, 9) == 'fav-threa') || (checkboxId.substring(0, 5) == 'threa'))
                        {
                            // Choose the container
                            var gridContainer = $('.container-futur-threads');
    
                            // First, empty the container in case it contains previous elements
                            gridContainer.empty();

                            // Iterate over the threads data and build the HTML structure for each thread
                            if(response.sorted_threads_info)
                            {
                                response.sorted_threads_info.forEach(function (thread) {
                                    
                                    if(thread.latest_comment != "None")
                                    {
                                        // Get the date from the latest comment in the thread
                                        date_thread = (thread.latest_comment).substring(0, 10)
                                    
                                        // If the date is today, just show the time
                                        if(response.today_date == date_thread)
                                        {
                                            date_ = (thread.latest_comment).substring(11, 16)
                                        }
                                        else if (response.yesterday_date == date_thread)
                                        {
                                            date_ = 'Yesterday'
                                        }
                                        else
                                        {
                                            // Otherwise, show the full date
                                            date_ = date_thread
                                        } 
                                    }
                                    else
                                    {
                                        // If there is no latest comment, show a slash
                                        date_ = "/"
                                    }
                                    
                                    // Check if the thread is closed or open
                                    if(thread.closed_thread == false)
                                    {
                                        o_c = 'Opened';
                                    }
                                    else
                                    {
                                        o_c = "Closed";
                                    }
                                                                        
                                    // Append the new thread element to the container
                                    gridContainer.append(
                                        '<div class="grid-thread" onclick=window.location.href="/fora' + '/threads/' + thread.slug_country + '/' + thread.category_selected + '/' + thread.slug_thread + '">' +
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
                                // If no threads are selected, show a message
                                gridContainer.append(
                                    '<div class="no-thread">' +
                                        'Nothing is selected.' +
                                    '</div>'
                                )
                            }
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
    });
});