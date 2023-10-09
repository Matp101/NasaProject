document.getElementById("clearFilters").addEventListener("click", function() {
  document.getElementById("postedAfter").value = '';
  document.getElementById("postedBefore").value = '';
  document.getElementById("experience").selectedIndex = 0;
  document.getElementById("skill").selectedIndex = 0;
  document.getElementById("filterForm").submit(); // Submit the form after clearing the fields
});


// $('option').mousedown(function(e) {
//   e.preventDefault();
//   var originalScrollTop = $(this).parent().scrollTop();
//   console.log("WHY");
//   $(this).prop('selected', $(this).prop('selected') ? false : true);
//   var self = this;
//   $(this).parent().focus();
//   setTimeout(function() {
//       $(self).parent().scrollTop(originalScrollTop);
//   }, 0);
  
//   return false;
// });
