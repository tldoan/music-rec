$('document').ready(function(){ 
	  var tracksss= document.getElementById('TRACK').innerText;
	 /* var pictures=document.getElementById('wcloud_picture1').src;*/
	$('.fa-hand-o-down').hide();


    
    // $('.fa-play').attr("id","ahha");
    $('.glyphicon-play-circle').attr("id","ahha");  
    $('.glyphicon-trash').attr("id","ahha");
    console.log($('#update_or_not').val());

    

       /*var QQ = $('*[id^="queue_"]');
       QQ.hide();*/

       $('#conteneur').hide();


     $('#feedback').click(function(){
    

    var email = 'thang.doan@mail.mcgill.ca';
        var subject = 'music recommendations';
        var emailBody = 'your feedback or comments';
        var attach = 'path';
        document.location = "mailto:"+email+"?subject="+subject+"&body="+emailBody+
            "?attach="+attach;


  });
     
      $('#submit').click(function(){
      	
      	if($('.rating').val()>0){

     	 $('#rating3').hide();
        
       	
       	$.ajax({
	    type: "POST",
	    url:"/save_rating",  
	    async : false,
	   data: { rating: $('.rating').val(),  
	 wordcloud: $('#tokenfield').val(), track_pseudo:tracksss},  
	   dataType: 'json',
	   success:function(jsons){

	   	var data = JSON.stringify(jsons);
        var data2=JSON.parse(data);  
        alert('Thanks for your comment !');  


	   },
	   error: function(){
	    alert('error');
	   },
 });
   }else{
   	alert('please give a rating !');
   }
  



});


if($('#update_or_not').val()=='True'){
  console.log('sisi');
                $.ajax({
                    type: "GET",
                    url:"/recommend_songs",  
                    async : true,
                    timeout: 20000,
                   // data: { track_pseudo: tracksss },  
                    dataType: 'json',
                   success:function(jsons){
                        
                        $('#conteneur').show();
                        var data = JSON.stringify(jsons);
                       

                        var data2=JSON.parse(data);
                        /*console.log(data2);*/
                      	/*QQ.show();*/
                        $('.fa-hand-o-down').show();
                      
                        $.each(data2, function(key, value){
                     
                        if (key.startsWith('#NOTE_') == true){
                            
                           $(key).text(value);
                          
                        }else if (key.startsWith('image') == true){
                         
                          document.getElementById(key).src=value;

                        }else if (key.startsWith('#genre_') == true){

                         
                        	$(key).text(value);

                    	}else if (key.startsWith('.next_song_') == true){
                           
                           $(key).val(value);

                        }else if(key.startsWith('#Eelement_') == true){
                           
                          $(key).text(value);
                        }       
                      }); 


                      $('.rating2').each(function(index,value){
                        
                      $(this).rating('rate',$('#NOTE_'+index).text())
                       });  


                        $('#pub2').text('');  
                        $('#pub2').removeClass('label label-danger').addClass('label label-warning');
                        $('#pub2').text('our recommendations : add one or two songs');
                        // QQ.show();
                     },
                   error: function(){
                    alert('error ');

                //////////////////////////////////////
                    $.ajax({

                    async : false,
                   
                   success:function(jsons){
                   	
                   	window.location.replace("https://music-rec.herokuapp.com/home");
                   },
                    error: function(){
                    alert('error again...');
                	},
                	});
                //////////////////////////////////////
                   },

                   });
}else{
  console.log('nooo');
   $('#conteneur').show();
                        $('#pub2').text('');  
                        $('#pub2').removeClass('label label-danger').addClass('label label-warning');
                        $('#pub2').text('our recommendations : add one or two songs');
}







});


// function for getting back the length of the song
/////////////////////////////////////
var time = document.getElementById("myAudio");

  
  function getCurTime() { 
       alert((time.currentTime));   
         
     
       
  }

  var length = document.getElementById("myAudio");

  var l=length.duration;
  function myFunction() { 
    alert(length.duration);
} 

function update(player) {

    var duration = player.duration;    // Durée totale

    var time     = player.currentTime; // Temps écoulé

    var fraction = time / duration;
    var percent  = Math.ceil(fraction * 100);

    $('.listening_time').val(time);
    $('.percentage').val(fraction); 
    $('.listening_time2').val(time);

    $('.percentage2').val(fraction); 
    $('.time_before_rated').val(time);

};




 $(function () { 
       $('.rating').rating();           
       
        $('.rating').on('change', function () {
           $('#heart-rate').text($(this).val());
        });        
  });




$(function () { 
         
  $('.rating2').each(function(index,value){
     

      
      
      $(this).rating('rate',$('#NOTE_'+index).text())
       });  
  });

document.getElementById('load2').disabled=true;
document.getElementById('unload').disabled=true;
$(function() { 

    

  $('#unload').click(function(){
     $.each($('.element'), function( index, value ) {
       $('#element_'+index).show();
       
        document.getElementById('unload').disabled=true;
     });
    $('#titre_1').text('empty');
    $('#titre_2').text('empty');
    $('.titre_1').val($('#titre_1').text());
    $('.titre_2').val($('#titre_2').text());


    $('#pub2').text('');
  
    $('#pub2').removeClass('label label-success').addClass('label label-warning');
    $('#pub2').text('our recommendations : add one or two songs to the playlist');

    // $('.fa-play').attr("id","ahah");
    $('.glyphicon-play-circle').attr("id","ahah");
    $('.glyphicon-trash').attr("id","ahha");



    document.getElementById('unload').disabled=true;
    document.getElementById('load2').disabled=true;

  });
         
  $('.swtich_page').each(function(index,value){
    
      
     $('#'+'queue_'+index).click(function(){         
         if ($('#titre_1').text()=='empty') {


                  $('#pub2').text('');
                  $('#pub2').removeClass('label label-warning').addClass('label label-success');
                  $('#pub2').text('You can now play the song or add one more');
                 
                  // $('.fa-play').attr("id","play_songs");
                  $('.glyphicon-play-circle').attr("id","play_songs");
                  $('.glyphicon-trash').attr("id","play_songs");


                  $('#titre_1').text($('.next_song_'+index).val());
                  $('.titre_1').val($('.next_song_'+index).val());
                  $('#element_'+index).hide();
                  document.getElementById('load2').disabled=false;
                  document.getElementById('unload').disabled=false;
             
            }else if ($('#titre_2').text()=='empty') {
              $('#titre_2').text($('.next_song_'+index).val());
              $('.titre_2').val($('.next_song_'+index).val());
              $('#element_'+index).hide();

              $('#pub2').text('ready to play !');


            } else if ($('#titre_1').text()!=='empty' && $('#titre_2').text()!=='empty'){
                alert('queue full ! Clear songs');
               
      
              

             
            }

        
  
      
       });  
  });
  });







 // token list
 ///////////////////
var mot=[];

$(function () { 
//console.log('1');
$.ajax({
    type: "GET",

    url:"/static/list/token_list.csv",
    
    dataType: "text",
    async : false,
   success: function(text){parseTxt(text);},
   error: function(){
    alert('can t open file or doesn t exist');
   },
   });
 //alert('2');
// console.log('2');
 function parseTxt(text){
  //alert('success');

  var rows=text.split('\n'); 
  //console.log(rows);

  $.each(rows, function( index, value ) {
  	
    mot[index]=value.replace(' ','');
   
  });
  
  
  };
 // console.log(mot);
// tokenfield
//////////////////////////
//console.log('3');
$('#tokenfield').tokenfield({

  autocomplete: {
    source:mot,
    delay: 100
  },
  showAutocompleteOnFocus: true


});

$('#tokenfield').on('tokenfield:createtoken', function (event) {
    var existingTokens = $(this).tokenfield('getTokens');
    $.each(existingTokens, function(index, token) {
        if (token.value === event.attrs.value) 
                    event.preventDefault();
    });
});

$('#tokenfield').on('tokenfield:createtoken', function (event) {
  //console.log(mot);
   
    var exists = false;
    $.each(mot, function( index, value ) {
            //console.log(value+","+event.attrs.value);

             // if (value.replace('\r', '')==String(event.attrs.value)) {
              if (value.replace(' ','')==String(event.attrs.value)) {
     
               exists = true;
          
               
            
            }
          
                   
    });
    if(exists === false)
        event.preventDefault();
    	// console.log(exists);
    	// console.log(mot[16]);
});

       

});
