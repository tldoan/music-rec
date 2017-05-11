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

	$('#feedback').click(function(){
		
		/*window.open('mailto:doantl89@gmail.com');*/
		var email = 'thang.doan@mail.mcgill.ca';
        var subject = 'music recommendations';
        var emailBody = 'your feedback or comments';
        var attach = 'path';
        document.location = "mailto:"+email+"?subject="+subject+"&body="+emailBody+
            "?attach="+attach;


	});

	$('#Instructions').click(function(){
		alert(' \n 1) Choose a song \n 2) Listen as long as you like \n 3) Please give a rating and a word \n 4) - Accept recommendations you like \n \xa0   - Come back to homepage otherwise');
			
			
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