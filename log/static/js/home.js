$('document').ready(function(){ 

	var dates = $('*[id^="type"]');
	
	


	$('#liste_songs').hide();
	$('#Icons').hide();
	$('.gallery').hide();

	$('#gallery_6').show();
	$('.genre_display').text('All')

	$('#Icons').click(function(){
		
		$('#List').show();
		$('#liste_songs').hide();
		$('#Icons').hide();
		
		dates.show();
		$('#gallery_6').show();
		$('.genre_display').text('All');
		
	});

	$('#List').click(function(){
		$('#liste_songs').show();
		$('#List').hide();
		$('#Icons').show();
		$('.gallery').hide();

		dates.hide();
		$('.genre_display').text('');


		
	});

	 $.each(dates, function( index, value ) {

	 	$('#type_'+index).click(function(){
	 		$('.genre_display').text($(this).text());
	 		/*console.log('gallery_'+index);*/
	 		$('.gallery').hide();
	 		$('#gallery_'+index).show();
	 		console.log('gallery_'+index);


	 		
	 	});
   
      
       
        
     });


});