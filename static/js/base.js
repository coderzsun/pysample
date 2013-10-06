/*
 * This script will be loaded on every page, since it's referenced by the base.html template.
 */
jQuery(document).ready(function() {
	// bind a handler to the logo, so clicking will return home
	jQuery("#app_header_logo").click(function() {
		location.href = "/";
	})
	// bind a handler to the settings icon
	jQuery("#settings_btn").click(function() {
		//		alert("wire up this link in base.js")
/*		if(jQuery('#checkbox1').is(':checked')) {
			alert("checkbox1 选中")
		}
*/
		
/*		
		var countChecked = function() {
			var n = jQuery( "input:checked" ).length;
			jQuery( "div" ).text( n + (n === 1 ? " is" : " are") + " checked!" );
		};
		countChecked();
		jQuery( "input[type=checkbox]" ).on( "click", countChecked );
*/
		var checkValues = jQuery('input[name=checkbox]:checked').map(function() {
			return jQuery(this).attr('value')
		}).get();
		var args = '{"checkbox":"' + checkValues + '"}';
		//this call will get back a JSON list, and use client side script to populate it
		jQuery.ajax({
			type : "POST",
			async : false,
			url : "/getcheckbox",
			data : args,
			contentType : "application/json; charset=utf-8",
			dataType : "json",
			success : function(cities) {
				jQuery("#coolstuff").empty();
				jQuery.each(cities, function(index, city) {
					jQuery("#coolstuff").append("<span class='red'>" + city +" <b> checked!</b></span> <br>")
				});

				jQuery('#container').highcharts({
					chart: {
						type: 'column'
					},
					title: {
						text: 'Fruit Consumption'
					},
					xAxis: {
						categories: ['Apples', 'Bananas', 'Oranges']
					},
					yAxis: {
						title: {
							text: 'Fruit eaten'
						}
					},
					series: [{
						name: 'Jane',
					data: [1, 0, 4]
					}, {
						name: 'John',
					data: [5, 7, 3]
					}]
				});

			},
			error : function(response) {
				alert(response.responseText);
			}
		});

	})
});
