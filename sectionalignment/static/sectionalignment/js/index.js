$(function () {
    $('form').on('submit', function (event) {
        var source = $('select[name="s"]').val(),
            destination = $('select[name="d"]').val();

        // check if source and destination are valid
        if (!source || !destination || source === destination) {
            $('.error').text(
                'Make sure to select different source and destination languages.'
            ).removeClass('d-none');

            event.preventDefault();
            return false;
        }
    });
});
