$(function () {
    $('body').on('click', 'button[type="submit"]', function (event) {
        var source = $('select[name="s"]').val(),
            destination = $('select[name="d"]').val();

        // check if source and destination are valid
        if (!source || !destination || source === destination) {
            $('.alert').text(
                'Make sure to select different source and destination languages.'
            ).removeClass('hidden');

            event.preventDefault();
            return false;
        }
    });
});
