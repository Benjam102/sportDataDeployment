$(document).ready(function() {
    // When the document is ready, attach a submit event handler to the form with id 'comment-form'
    $('#comment-form').submit(function(e) 
    {
        // Prevent default form submission
        e.preventDefault(); 

        // Retrieve the URL from the data-url attribute of the form
        var url = $(this).data('url');
        
        // Collect form data
        var formData = $(this).serialize();
        
        // Submit form data via AJAX
        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function(response) 
            {
                // Clear the textarea
                $('#comment-content').val('');
                
                // Remove the "No comments" message if it exists
                $('#no-comments-msg').remove();

                // Extract the time from the date
                var commentDate = new Date(response.date);

                // Get hours and minutes
                var hours = commentDate.getHours();
                var minutes = commentDate.getMinutes();

                // Format time as HH:MM
                var formattedTime = (hours < 10 ? '0' : '') + hours + ':' + (minutes < 10 ? '0' : '') + minutes;

                // Append the new comment to the comment list
                $('#comment-list').append(
                    '<div class="grid-comment">' +
                        '<div class="username">' + 
                            '<img src="http://127.0.0.1:8000/static/IMG/joueurRugby.png" alt="">' +
                                response.username +
                        '</div>' +
                        '<div class="com-content">' +
                            response.content +
                        '</div>' +
                        '<div class="com-date">' +
                            formattedTime +
                        '</div>' +
                    '</div>');
            },
            // Log any errors to the console
            error: function(error) 
            {
                console.log(error);
            }
        });
    });
});
