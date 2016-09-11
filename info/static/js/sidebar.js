$(window).resize(function() {
	var path = $(this);
	var contW = path.width();
	if(contW >= 761){
		document.getElementsByClassName("sidebar-toggle")[0].style.left="0px";
    document.getElementById("page-content").style.left="250px";
    //document.getElementById("page-content").style.marginRight="0px";
  }else{
		document.getElementsByClassName("sidebar-toggle")[0].style.left="-250px";
    document.getElementById("page-content").style.left="0px";
    //document.getElementById("page-content").style.marginRight="0px";
	}
});
$(document).ready(function() {
	$('.dropdown').on('show.bs.dropdown', function(e){
	    $(this).find('.dropdown-menu').first().stop(true, true).slideDown(300);
	});
	$('.dropdown').on('hide.bs.dropdown', function(e){
		$(this).find('.dropdown-menu').first().stop(true, true).slideUp(300);
	});
	$("#menu-toggle").click(function(e) {
		e.preventDefault();
		var elem = document.getElementById("sidebar-wrapper");
		left = window.getComputedStyle(elem,null).getPropertyValue("left");
		if(left == "0px"){
			document.getElementsByClassName("sidebar-toggle")[0].style.left="-250px";
      document.getElementById("page-content").style.left="0px";
      //document.getElementById("page-content").style.marginRight="0px";
		}
		else if(left == "-250px"){
			document.getElementsByClassName("sidebar-toggle")[0].style.left="0px";
      document.getElementById("page-content").style.left="250px";
      //document.getElementById("page-content").style.width=(screen.width - 250).toString() + "px";
      //document.getElementById("page-content").style.marginRight="-250px";
		}
	});
});
