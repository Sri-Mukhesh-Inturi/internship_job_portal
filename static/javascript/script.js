//for navbar
  $(document).ready(function(){
    $('.sidenav').sidenav();
  });

//for active class in navbar
$(document).ready(function() {
	// get current URL path and assign 'active' class
	var pathname = window.location.pathname;
	$('.nav_active > li > a[href="'+pathname+'"]').parent().addClass('active');
})
//for tooltip
  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems, {});
  });

 //for datepicker
   document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems, {});
  });

//for slider
 var array_of_dom_elements = document.querySelectorAll("input[type=range]");
 M.Range.init(array_of_dom_elements);


// for autocomplete
