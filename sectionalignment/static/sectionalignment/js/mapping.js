$(function () {


    function setupAutocomplete($element, suggestions) {
        var options = {
	        data: suggestions,
            list: {
		        match: {
			        enabled: true
		        }
	        }
        };

        $element.easyAutocomplete(options);
    }

    setupAutocomplete($('.translation'), window.suggestions);

    $('body').on('click', '#add-more', function (event) {
        var $newBox = $('<div class="translation-box"></div>')
            .append('<input type="text" class="translation" name="translation">');

        $newBox.insertBefore($(event.target));
        setupAutocomplete($newBox.find('input'), window.suggestions);
        event.preventDefault();
    });
} );
