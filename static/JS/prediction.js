function validate(idMargin, idTotal, idButton) 
{
    /**
     * Allows us to send the user's prediction when he clicked on the button validate.
     *
     * @param {string} idMargin Id of the input which contain the user's margin prediction.
     * @param {string} idTotal Id of the input which contain the user's total prediction.
     * @param {string} idButton Id of the form to know if the user make his early or his final prediction.
     */

    const margin = document.getElementById(idMargin).innerText;
    const total = document.getElementById(idTotal).innerText;
    
    // When the document is ready, attach a submit event handler to the form with id 'comment-form'
    $('#' + idButton).submit(function(e) 
    {
            // Prevent default form submission
            e.preventDefault(); 

            // Retrieve the URL from the data-url attribute of the form
            var url = $(this).data('url');

            // Creation of a FormData object to send data via AJAX. It collects the hidden inputs and the crsf token.
            var formData = $(this).serialize();
            
            // Add an additional variable to the serialized string to manage whether or not the table is created
            formData += '&button=' + encodeURIComponent(idButton);

            // Submit form data via AJAX
            $.ajax({
                type: 'POST',
                url: url,
                data: formData,
                success: function(response) // response contains : margin, total and button (from the view)
                {
                    const containerPrediction = document.getElementById(idButton);
                    const containerCursor = containerPrediction.querySelectorAll('.grid-form'); // there are two
                    
                    // Removing cursors
                    containerCursor.forEach(function(gridCursor)
                    {
                        containerPrediction.removeChild(gridCursor);
                    });
                    
                    // Adding the response of the user
                    var html = '<div class="grid-response">' +
                                    '<span class="second-col">Margin:</span>' +
                                    '<span class="cursor-value">' + response.margin + '</span>' +
                                '</div>' +
                                '<div class="grid-response">' +               
                                    '<span class="second-col">Total:</span>' +
                                    '<span class="cursor-value">' + response.total + '</span>' +
                                '</div>';
                    
                    const containerTitle = containerPrediction.querySelector('.grid-form-title');
                    containerTitle.insertAdjacentHTML('afterend', html);

                    // Deactivating the validation button
                    const button = containerPrediction.querySelector('.button');
                    button.disabled = true;
                },
                // Log any errors to the console
                error: function(error) 
                {
                    console.log(error);
                }
            });
    });
}


function confirmationPhrase(containerInput1Id, containerInput2Id, inputMId, inputTId, button)
{
    /**
     * Allows us to send the user's prediction when he clicked on the button validate.
     *
     * @param {string} containerInput1Id Id of the container that contains the input for the user's margin prediction.
     * @param {string} containerInput2Id Id of the container that contains the input for the user's total prediction.
     * @param {string} inputMId Id of the container where the value of the cursor for margin is displayed.
     * @param {string} inputTId Id of the container where the value of the cursor for total is displayed.
     * @param {string} Button Id of the form to add listener on cursors for early or final predictions.
     */

    const containerS1 = document.getElementById(containerInput1Id);
    const containerS2 = document.getElementById(containerInput2Id);

    const containerM = document.getElementById(inputMId);
    const containerT = document.getElementById(inputTId);

    const containerFuzzy = document.querySelector('.fuzzy');

    // I run the file script when the user is logged in. 
    // Therefore, the veil must be removed for the user to have access to the predictions.
    if (containerFuzzy != null)
    {
        containerFuzzy.style.display = 'none';
    }

    // Retrieve the button element by its ID
    const form = document.getElementById(button);
    const submitButton = form.querySelector('.button');
    
    if ((containerS1 != null) || (containerS2 != null)) // When the user has already made a prediction
    {
        containerS1.addEventListener('change', function() // We listened changes in the container with the cursor for margin
        {
            if (containerM.innerText != '/' && containerT.innerText != '/') 
            {
                // Resolution of the system to determine the predicted scores of the two teams
                const home_score = (parseInt(containerM.textContent) + parseInt(containerT.textContent))/2;
                const away_score = parseInt(containerT.textContent) - home_score;
                
                var containerMsg = $(form.getElementsByClassName('grid-form-message'));
                containerMsg.empty();

                var html = '<div> Prediction: ' + home_score + ' - ' + away_score + '</div>';

                containerMsg.append(html);
                
                if(submitButton.disabled = true)
                {
                    // Activate the validate button
                    submitButton.disabled = false;
                }
                
                validate(containerM.id, containerT.id, button);
            } 
        });

        containerS2.addEventListener('change', function() // We listened changes in the container with the cursor for total
        {
            if (containerM.innerText != '/' && containerT.innerText != '/') 
            {
                // Resolution of the system to determine the predicted scores of the two teams
                const home_score = (parseInt(containerM.textContent) + parseInt(containerT.textContent))/2;
                const away_score = parseInt(containerT.textContent) - home_score;
                
                var containerMsg = $(form.getElementsByClassName('grid-form-message'));
                containerMsg.empty();

                var html = '<div> Prediction: ' + home_score + ' - ' + away_score + '</div>';

                containerMsg.append(html);

                if(submitButton.disabled = true)
                {
                    // Activate the validate button
                    submitButton.disabled = false;
                }

                validate(containerM.id, containerT.id, button);
            } 
        });
    }
}


function to_kickoff(kickoff)
{
    /**
     * Allows us to edit the format of a date (-> '1:05 p.m.' to hours='13', minutes='5', seconds='0').
     *
     * @param {string} kickoff Date that we want to edit.
     */

    const [time, period] = kickoff.split(' ');
    var [hours, minutes, seconds] = time.split(":");

    if (period === "p.m." && hours !== "12") 
    {
        hours = String(Number(hours) + 12);
    }
    else if (period === "a.m." && hours === "12") 
    {
        hours = "00";
    }

    if (minutes == undefined) // When we have '1:00 p.m.')
    {
        minutes = "0";
    }

    if (seconds == undefined) // We don't have seconds
    {
        seconds == "0";
    }

    return {hours, minutes, seconds};
}


function to_date(date)
{
    /**
     * Allows us to break down the date.
     *
     * @param {string} date Date that we want to collect separely the year, month and day.
     */

    const matchDate = new Date(date); // We transform our string into a data object

    var year = matchDate.getFullYear();
    var month = matchDate.getMonth(); 
    var day = matchDate.getDate();

    return {year, month, day};
}


function add_zero_date(nb)
{
    /**
     * Allows us to add a '0' in front of a figure.
     *
     * @param {Number} nb Number that we want to add a '0' if it is a figure.
     */

    if (nb < 10 && nb >= 0)
    {
        return '0' + nb;
    }
    else
    {
        return nb;
    }
}


function subtractionDays(date, days) 
{
    /**
     * Function for subtracting a certain number of days from a given date.
     *
     * @param {Date} date Original date.
     * @param {days} nb Number of days we want to subtract.
     */

    
    let nouvelleDate = new Date(date);
    nouvelleDate.setDate(nouvelleDate.getDate() - days);

    return nouvelleDate;
}


function accessPrediction(idButton)
{
    /**
     * Function to manage the access of the prediction.
     *
     * @param {string} date Id of the form to manage (early or final prediction).
     */

    const form_ = document.getElementById(idButton);
    const fuzzy_prediction_time = form_.querySelector('.fuzzy-prediction-time');
    const grid_title = form_.querySelector('.grid-form-title');
    const submitButton = form_.querySelector('.button');

    const matchDate = form_.getAttribute('data-match-date');         // Date of the match
    const matchKickoff = form_.getAttribute('data-match-time');      // Kickoff of the match

    const matchDateElement = to_date(matchDate);
    const matchKickoffElement = to_kickoff(matchKickoff);

    const matchD = new Date(matchDateElement.year, matchDateElement.month, matchDateElement.day, 
                            matchKickoffElement.hours, matchKickoffElement.minutes);
                            
    const today = new Date();
    var untilData = null;

    // Calculate the difference in days between today and the date of the match
    const timeDifference = matchD - today;                           // in milliseconds
    const dayDifference = timeDifference / (1000 * 60 * 60 * 24);    // Convert to days

    if (idButton == 'button1')
    {
        if (fuzzy_prediction_time != null)
        {
            // Check if the difference is between 3 and 7 days -> ok to display the prediction
            if (dayDifference >= 3 && dayDifference <= 7) 
            {
                fuzzy_prediction_time.style.display = 'none';
                untilData = to_date(subtractionDays(matchD, 3));
                $(grid_title).append('(until ' + add_zero_date(untilData.day) + '/' + add_zero_date((untilData.month + 1)) + '/' +  untilData.year + ')');
            } 
            else 
            {
                // Check if the difference is < 3 -> too late for the prediction
                if (dayDifference < 3)
                {
                    var html = '<div class="grid-warning-prediction"><span>Too late !</span></div>';
                    $(fuzzy_prediction_time).append(html);
                }

                // Check if the difference is > 3 -> user can't have access to the prediction for the moment
                if(dayDifference > 7)
                {
                    var untilData = to_date(subtractionDays(matchD, 7));
                    var html = '<div class="grid-warning-prediction">From ' + add_zero_date(untilData.day) + '/' + add_zero_date((untilData.month + 1)) + '/' +  untilData.year + '</div>';
                    $(fuzzy_prediction_time).append(html);
                }

                fuzzy_prediction_time.style.display = 'flex';
                submitButton.disabled = true;                        // For security
            }
        }
        
    }
    else if (idButton == 'button2')
    {
        if (fuzzy_prediction_time != null)
        {
            // Check if the difference is between 3 days and 1 hours before the match -> ok to display the prediction
            if(dayDifference <= 3 && dayDifference > 0.04)
            {
                fuzzy_prediction_time.style.display = 'none';
                $(grid_title).append('(until 1 hours before)');
            } 
            else 
            {
                // Check if the difference is below 1 hours -> too late for the prediction
                if(dayDifference < 0.04)
                {
                    var html = '<div class="grid-warning-prediction"><span>Too late !</span></div>';
                    $(fuzzy_prediction_time).append(html);
                }
                
                // Check if the difference is above 3 days -> user can't have access to the prediction for the moment
                if(dayDifference > 3)
                {
                    untilData = to_date(subtractionDays(matchD, 3));
                    var html = '<div class="grid-warning-prediction">From ' + add_zero_date(untilData.day) + '/' + add_zero_date((untilData.month + 1)) + '/' +  untilData.year + '</div>';
                    $(fuzzy_prediction_time).append(html);
                }
                
                fuzzy_prediction_time.style.display = 'flex';
                submitButton.disabled = true;                          // For security
            }
        }
    }
}


document.addEventListener('DOMContentLoaded', function() 
{
    // Deals with the prediction of the user
    confirmationPhrase('content-predic1-1', 'content-predic1-2', 'rangeValueM1', 'rangeValueT1', 'button1');
    confirmationPhrase('content-predic2-1', 'content-predic2-2', 'rangeValueM2', 'rangeValueT2', 'button2');

    // Manage the access of the prediction
    accessPrediction('button1');
    accessPrediction('button2');
});
