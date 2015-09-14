//$(document).on('click', ".button123", function(){
//    $row = $(this).closest(".123");   // Find the row
//    var $text = $row.find(".nr").text(); // Find the text
//  alert($text);
// });


$( window ).load(function(e) {
    e.preventDefault();
   $(document).on('click', ".button123", function(){
   $row = $(this).closest(".123");   // Find the row
    var $text = $row.find(".nr").text(); // Find the text
  alert($text);
 });
 });
