(function ($, GT) {
    $(function () {
        var $translation = $('.translation');

        function setupAutocomplete($element, suggestions) {
            var options = {
	            data: suggestions,
                adjustWidth: false,
                list: {
		            match: {
			            enabled: true
		            }
	            }
            };

            $element.easyAutocomplete(options);
        }

        setupAutocomplete($translation, GT.suggestions);

        $translation.focus();

        if (GT.userProgress > 0) {
            $('html,body').animate({scrollTop: $translation.offset().top});
        }

        $('body').on('click', '#add-more', function (event) {
            var $newBox = $('<div class="translation-box"></div>')
                .append('<input type="text" class="translation form-control" name="translation">');

            $newBox.insertBefore($(event.target));
            setupAutocomplete($newBox.find('input'), GT.suggestions);
            event.preventDefault();
        });
    } );
}(window.jQuery, window.GT));
