function generalStandingNoPools(response, containerRanks)
{
    var html =  '<div></div>' +
                '<div class="grid-tab-ranking">' +
                    '<div></div>' +
                    '<div></div>' +
                    '<div class="container-nb-ranking-passed-match">MP</div>' +
                    '<div class="container-nb-ranking-passed-match">W</div>' +
                    '<div class="container-nb-ranking-passed-match">D</div>' +
                    '<div class="container-nb-ranking-passed-match">L</div>' +
                    '<div class="container-nb-ranking-passed-match">P</div>' +
                    '<div class="container-nb-ranking-passed-match">PD</div>' +
                    '<div class="container-nb-ranking-passed-match">B</div>' +
                    '<div class="container-nb-ranking-passed-match">Form</div>' +
                '</div>';

    response.ranks_list.forEach(function(standing) {
        html +=     '<div class="grid-tab-ranking">' +
                        '<div class="rank">' +
                            standing.rank +
                        '</div>' +
                        '<div class="team-ranking">'+
                            '<img src="' + standing.logo + '" alt="">' +
                            standing.team_id +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.played +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.won +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.draw +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.lost +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.points +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.points_difference +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.bonus +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' ;

        var tendencyList = standing.tendency.split(' ');

        tendencyList.slice(0, 4).forEach(function(r) 
        {
            if (r === 'V') {
                html += '<div class="carre V">' +
                            'V' +
                        '</div>';
            } 
            else if (r === 'D') 
                {
                html += '<div class="carre D">' +
                            'D' +
                        '</div>';
            } 
            else 
            {
                html += '<div class="carre N">' +
                            'N' +
                        '</div>';
            }
        });
        
        html += `</div></div>`;
    });

    containerRanks.append(html);    
}

function moreInformationsStandingNoPools(response, containerRanks)
{
    var html =  '<div></div>' +
                '<div class="grid-rank-more-informations">' +
                    '<div></div>' +
                    '<div></div>' +
                    '<div class="container-nb-ranking-passed-match">F</div>' +
                    '<div class="container-nb-ranking-passed-match">AF</div>' +
                    '<div class="container-nb-ranking-passed-match">A</div>' +
                    '<div class="container-nb-ranking-passed-match">AA</div>' +
                    '<div class="container-nb-ranking-passed-match">TF</div>' +
                    '<div class="container-nb-ranking-passed-match">TA</div>' +
                    '<div class="container-nb-ranking-passed-match">AB</div>' +
                    '<div class="container-nb-ranking-passed-match">DB</div>' +
                '</div>';

    response.ranks_list.forEach(function(standing) {
        html +=     '<div class="grid-rank-more-informations">' +
                        '<div class="rank">' +
                            standing.rank +
                        '</div>' +
                        '<div class="team-ranking">'+
                            '<img src="' + standing.logo + '" alt="">' +
                            standing.team_id +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.points_for +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.avg_points_for +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.points_against+
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.avg_points_against +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.try_for +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.try_against +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.att_bonus +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.def_bonus +
                        '</div>' +
                    '</div>';
    });

    containerRanks.append(html);    
}

function generalStandingPools(response, containerRanks)
{
    var isFirst = true;
    var html =  '<div class="slider">';
    
    Object.entries(response.pools_teams).forEach(([key, standingsArray]) => 
    {                
                    
        if (isFirst == true)
        {
            html += '<div class="c slider-active">';
            isFirst = false;
        }
        else
        {
            html += '<div class="c">';
        }

        html += '<div class="grid-league-pool">Pool ' + key + ':</div>' +
                    '<div class="grid-tab-ranking">' +
                        '<div></div>' +
                        '<div></div>' +
                        '<div class="container-nb-ranking-passed-match">MP</div>' +
                        '<div class="container-nb-ranking-passed-match">W</div>' +
                        '<div class="container-nb-ranking-passed-match">D</div>' +
                        '<div class="container-nb-ranking-passed-match">L</div>' +
                        '<div class="container-nb-ranking-passed-match">P</div>' +
                        '<div class="container-nb-ranking-passed-match">PD</div>' +
                        '<div class="container-nb-ranking-passed-match">B</div>' +
                        '<div class="container-nb-ranking-passed-match">Form</div>' +
                    '</div>';
        
        standingsArray.forEach(standing => 
        {
            html +=     '<div class="grid-tab-ranking">' +
                            '<div class="rank">' +
                                standing.rank +
                            '</div>' +
                            '<div class="team-ranking">'+
                                '<img src="' + standing.logo + '" alt="">' +
                                standing.team_id +
                            '</div>' +
                            '<div class="container-nb-ranking-passed-match">' +
                                standing.played +
                            '</div>' +
                            '<div class="container-nb-ranking-passed-match">' +
                                standing.won +
                            '</div>' +
                            '<div class="container-nb-ranking-passed-match">' +
                                standing.draw +
                            '</div>' +
                            '<div class="container-nb-ranking-passed-match">' +
                                standing.lost +
                            '</div>' +
                            '<div class="container-nb-ranking-passed-match">' +
                                standing.points +
                            '</div>' +
                            '<div class="container-nb-ranking-passed-match">' +
                                standing.points_difference +
                            '</div>' +
                            '<div class="container-nb-ranking-passed-match">' +
                                standing.bonus +
                            '</div>' +
                            '<div class="container-nb-ranking-passed-match">' ;

            var tendencyList = standing.tendency.split(' ');

            tendencyList.slice(0, 4).forEach(function(r) 
            {
                if (r === 'V') {
                    html += '<div class="carre V">' +
                                'V' +
                            '</div>';
                } 
                else if (r === 'D') 
                    {
                    html += '<div class="carre D">' +
                                'D' +
                            '</div>';
                } 
                else 
                {
                    html += '<div class="carre N">' +
                                'N' +
                            '</div>';
                }
            });

            html += '</div></div>';
            
        });
        
        html += '</div>'; 
    });

    html += '</div>'; // slider 
    
    html += '<div class="container-button">' +
                '<div class="button-nav left">' +
                    '<img src="/static/IMG/homePageRight/flecheGauche.png" alt="">' +
                '</div>' +
                '<div class="button-nav right">' +
                    '<img src="/static/IMG/homePageRight/flecheDroite.png" alt="">' +
                '</div>'+
            '</div>';
            
    containerRanks.append(html);
}

function moreInformationsStandingPools(response, containerRanks)
{
    var isFirst = true;
    var html =  '<div class="slider2">';
    
    Object.entries(response.pools_teams).forEach(([key, standingsArray]) => 
    {                
                    
        if (isFirst == true)
        {
            html += '<div class="c slider-active">';
            isFirst = false;
        }
        else
        {
            html += '<div class="c">';
        }

        html += '<div class="grid-league-pool">Pool ' + key + ':</div>' +
                '<div class="grid-rank-more-informations">' +
                    '<div></div>' +
                    '<div></div>' +
                    '<div class="container-nb-ranking-passed-match">F</div>' +
                    '<div class="container-nb-ranking-passed-match">AF</div>' +
                    '<div class="container-nb-ranking-passed-match">A</div>' +
                    '<div class="container-nb-ranking-passed-match">AA</div>' +
                    '<div class="container-nb-ranking-passed-match">TF</div>' +
                    '<div class="container-nb-ranking-passed-match">TA</div>' +
                    '<div class="container-nb-ranking-passed-match">AB</div>' +
                    '<div class="container-nb-ranking-passed-match">DB</div>' +
                '</div>';
        
        standingsArray.forEach(standing => 
        {
            html += '<div class="grid-rank-more-informations">' +
                        '<div class="rank">' +
                            standing.rank +
                        '</div>' +
                        '<div class="team-ranking">'+
                            '<img src="' + standing.logo + '" alt="">' +
                            standing.team_id +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.points_for +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.avg_points_for +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.points_against+
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.avg_points_against +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.try_for +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.try_against +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.att_bonus +
                        '</div>' +
                        '<div class="container-nb-ranking-passed-match">' +
                            standing.def_bonus +
                        '</div>' +
                    '</div>';
        });
        
        html += '</div>'; 
    });

    html += '</div>'; // slider 
    
    html += '<div class="container-button">' +
                '<div class="button-nav left2">' +
                    '<img src="/static/IMG/homePageRight/flecheGauche.png" alt="">' +
                '</div>' +
                '<div class="button-nav right2">' +
                    '<img src="/static/IMG/homePageRight/flecheDroite.png" alt="">' +
                '</div>'+
            '</div>';
            
    containerRanks.append(html);
}

function getInformationLeague(containerId, containerOfAddId1, containerOfAddId2) 
{
    var containerSelect = document.getElementById(containerId);

    var selectLi = containerSelect.querySelectorAll('.val li');

    selectLi.forEach(function(li) 
    {
        li.addEventListener('click', function() 
        {
            var idLi = li.id;
            console.log(idLi);
            // Make an AJAX request to get the info based on the selected competition
            $.ajax({
                url: idLi, // URL to your server endpoint
                type: 'GET',

                success: function(response) 
                {
                    var containerRanks1 = $(document.getElementById(containerOfAddId1));
                    var containerRanks2 = $(document.getElementById(containerOfAddId2));
                    containerRanks1.empty();
                    containerRanks2.empty();
                   
                    if (response.nb_teams_pool == 0)
                    {
                        generalStandingNoPools(response, containerRanks1);
                        moreInformationsStandingNoPools(response, containerRanks2);

                        $.getScript('/static/JS/slider.js', function() {
                            // Pour reattacher les bons trucs 
                            sliderCompetition('.slider', '.right', '.left');
                            sliderCompetition('.slider2', '.right2', '.left2');
                        });
                    }
                    else
                    {
                        generalStandingPools(response, containerRanks1);
                        moreInformationsStandingPools(response, containerRanks2);

                        $.getScript('/static/JS/slider.js', function() {
                            // Pour reattacher les bons trucs 
                            sliderCompetition('.slider', '.right', '.left');
                            sliderCompetition('.slider2', '.right2', '.left2');
                        });
                    }
                },

                error: function(xhr, status, error) 
                {
                    console.error('AJAX Error: ' + status + error);
                }
            });
        });
    }); 
}

// Initialize the click handler for all containers with the class 'under-category-content'
$(document).ready(function() 
{   
    getInformationLeague('content-cat3.1', 'container-add-standing1', 'container-add-standing2');
});