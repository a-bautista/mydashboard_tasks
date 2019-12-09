// Compose new tweet highlighting, easy.
(function($) {
  function onTweetCompose(event) {
    var $textarea = $(".js-keeper-editor"),
      $placeholderBacker = $(".js-keeper-placeholder-back"),
      currentValue = $textarea.val();

    // realLength is not 140, links counts for 23 characters always.
    var realLength = 140;
    var remainingLength = 140 - currentValue.length;

    if (0 > remainingLength) {
      // Split value if greater than
      var allowedValuePart = currentValue.slice(0, realLength),
        refusedValuePart = currentValue.slice(realLength);
      // Fill the hidden div.
      $placeholderBacker.html(
        allowedValuePart + "<em>" + refusedValuePart + "</em>"
      );
    } else {
      $placeholderBacker.html("");
    }
  }

  $(document).ready(function() {
    $textarea = $("textarea");

    // Create a pseudo-element that will be hidden behind the placeholder.
    var $placeholderBacker = $(
      '<div class="js-keeper-placeholder-back"></div>'
    );
    $placeholderBacker.insertAfter($textarea);

    onTweetCompose();
    $textarea.on(
      "selectionchange copy paste cut mouseup input",
      onTweetCompose
    );
  });
})(jQuery);
