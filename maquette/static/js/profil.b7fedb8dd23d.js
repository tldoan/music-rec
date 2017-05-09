$('document').ready(function(){ 
$('#cc').hide();

$('#cancel').hide();
	$('#change_settings').click(function(){

        $('#change_settings').hide();
        $('#cc').show();
        $('#cancel').show();
        
        });

	$('#cancel').click(function(){
		$('#change_settings').show();
		$('#cancel').hide();
		$('#cc').hide();


	});
		//console.log(document.getElementById("sex").innerHTML);
		
		
		
	
	 if( $('.age').text()=='' || $('.area').text()=='' || $('.region').text()=='' || $('.sex').text()=='' ) 
	 {
	 	$('#homee').hide();
	 	$('#homee2').hide();
	 	$('.uncomplete_form').text('Complete the form before going to the next step');

	 }
	 else
	 {
	 	$('#homee').show();
	 	$('#homee2').show();
	 	$('.uncomplete_form').text('');
	 }

	 












});