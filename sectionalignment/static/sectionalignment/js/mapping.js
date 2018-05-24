$(function () {
    function setupAutocomplete(selector, suggestions) {
        var options = {
	        data: suggestions,
            list: {
		        match: {
			        enabled: true
		        }
	        }
        };

        $(selector).easyAutocomplete(options);
    }

    setupAutocomplete('.translation', window.suggestions);

    $('body').on('click', '#add-more', function (event) {
        event.preventDefault();
    });
} );
