$(document).ready(function() {
    $('#comment-form').submit(function(e) {
    e.preventDefault(); // Prevent default form submission

    // Récupérer l'URL depuis l'attribut data-url du formulaire
    var url = $(this).data('url');
    //console.log(url)
    // Collect form data
    var formData = $(this).serialize();
    
    // Submit form data via AJAX
    $.ajax({
        type: 'POST',
        url: url,
        data: formData,
        success: function(response) {
            // Clear the textarea
            $('#comment-content').val('');
            
            // Remove the "No comments" message if it exists
            $('#no-comments-msg').remove();

            // Extraction de l'heure à partir de la date
            var commentDate = new Date(response.date);

            // Obtention de l'heure et des minutes
            var hours = commentDate.getHours();
            var minutes = commentDate.getMinutes();

            // Formater l'heure au format HH:MM
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
        error: function(error) {
            console.log(error); // Log any errors to the console
        }
    });
});
});