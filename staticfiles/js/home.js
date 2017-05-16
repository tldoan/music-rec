$('document').ready(function(){ 

	var dates = $('*[id^="type"]');
	
	


	$('#liste_songs').hide();
	$('#Icons').hide();
	$('.gallery').hide();


	var random_type=Math.floor(Math.random() * 5) + 1  ;
	



	$('#gallery_'+random_type).show();
	$('.genre_display').text($('#type_'+random_type).text());
	


	$('#Icons').click(function(){
		
		$('#List').show();
		$('#liste_songs').hide();
		$('#Icons').hide();
		
		dates.show();

		var random_type2 =Math.floor(Math.random() * 5) + 1  ;
		
		$('#gallery_'+random_type2).show();

		$('.genre_display').text($('#type_'+random_type2).text());
		

		
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
	 		

	 		
	 	});
   
      
       
        
     });


});