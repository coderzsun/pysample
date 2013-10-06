jQuery(document).ready(function() {
	/*
	 * The jQuery $(document).ready function can be placed on multiple script files.
	 * 
	 * It's smart enough to figure it out, and they'll all be executed 
	 * WHEN the page has loaded.
	 * 
	 */
	
	// this will bind the change event of our countries drop down
	jQuery("#countries").change(function() {
		//alert($(this).val());

		// jquery ajax args must be a JSON string.  So, you can build a string like this:
		// (see the next ajax call for a different approach)
		var args = '{"country":"' + jQuery(this).val() + '"}';

		//this call will get back a JSON list, and use client side script to populate it
		jQuery.ajax({
			type : "POST",
			async : false,
			url : "/getregionsasjson",
			data : args,
			contentType : "application/json; charset=utf-8",
			dataType : "json",
			success : function(regions) {
				jQuery("#regions").empty();
				jQuery.each(regions, function(index, region) {
					jQuery("#regions").append("<option value='" + region + "'>" + region + "</option>");
				});
			},
			error : function(response) {
				alert(response.responseText);
			}
		});
	});
});
