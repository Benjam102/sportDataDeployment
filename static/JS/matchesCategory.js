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
                
                // Make an AJAX GET request to the URL
                success: function (response) 
                {
                    console.log(response);
                    // Case where we want to diplay a tchat
                    if(response.upcoming_matches_list != null)
                    {
                        // Choose the container
                        console.log('oui');
                        var gridContainer = $('.container-futur-matches');
    
                        // First, empty the container in case it contains previous elements
                        gridContainer.empty();
                        
                        var date = '';
                        var html = '';
                        
                        (response.upcoming_matches_list).forEach(function(match)
                        {
                            if (response.today_date == match.date)
                            {
                                date = 'Today';
                            }
                            else if (response.tomorrow_date == match.date)
                            {
                                date = 'Tomorrow';
                            }
                            else
                            {
                                date = match.date;
                            }
                            
                            html = '<a href="/match/' + match.key_id + '/" class="grid-match">' + // on peut pas passer par des url
                                        '<div class="illustration">' +
                                            '<img src="/static/IMG/rugbyBut.png" alt="">' +
                                        '</div>' +
                                        '<div class="date">' +
                                            date +
                                        '</div>' +
                                        '<div class="hour"> ' +
                                            match.kickoff +
                                        '</div>';
                            
                            if (match.logo_home_team != null)
                            {
                                html += '<div class="team-home">' +
                                            '<img src="' + match.logo_home_team + '" alt="">' +                                        
                                            match.home_team +
                                        '</div>';
                            }
                            else 
                            {
                                html += '<div class="team-home">' + 
                                            '<img></img>' +                                      
                                            match.home_team +
                                        '</div>';
                            }

                            if(match.logo_away_team != null)
                            {
                                html += '<div class="team-away">' +
                                            '<img src="' + match.logo_away_team + '" alt="">' +
                                            match.away_team +
                                        '</div>';
                            }
                            else
                            {
                                html += '<div class="team-away">' +
                                            '<img></img>' + 
                                            match.away_team +
                                        '</div>';
                            }

                            html += '</a>';
                            gridContainer.append(html);
                        });
                    }
                    else
                    {
                        // Choose the container
                        var gridContainer = $('.container-futur-matches');

                        // First, empty the container in case it contains previous elements
                        gridContainer.empty();

                        // If no competition are selected, show a message
                        gridContainer.append(
                            '<div class="no-match">' +
                                'Nothing is selected.' +
                            '</div>'
                        )
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