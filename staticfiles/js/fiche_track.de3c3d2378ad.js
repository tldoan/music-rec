$('document').ready(function(){ 
	  var tracksss= document.getElementById('TRACK').innerText;
	  var pictures=document.getElementById('wcloud_picture1').src;
	 
	  

       var QQ = $('*[id^="queue_"]');
       QQ.hide();




     $('#feedback').click(function(){
    
    /*window.open('mailto:doantl89@gmail.com');*/
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

	      if (data2['update_wcloud']){
	      	alert('Thanks for your coments !');
	       	document.getElementById('wcloud_picture1').src="https://s3.ca-central-1.amazonaws.com/music-rec/wait.gif"
	       
	       	setTimeout(function() {
	       			
  				 document.getElementById('wcloud_picture1').src=pictures;
		}, 1000);
	       
	       
	      	
	            

	    }else{
	    	alert('pas d update');
	    }
	   },
	   error: function(){
	    alert('error during the callback');
	   },
 });
   }else{
   	alert('please give a rating !');
   }
  



});




$.ajax({
    type: "GET",
    url:"/recommend_songs",  
    async : false,
   // data: { track_pseudo: tracksss },  
    dataType: 'json',
   success:function(jsons){
      
        var data = JSON.stringify(jsons);
       

        var data2=JSON.parse(data);
        /*console.log(data2);*/
      	QQ.show();
      
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
        $('#pub').text('You may also like:');
        QQ.show();
     },
   error: function(){
    alert('error during the callback, redirect you to homepage');

//////////////////////////////////////
    $.ajax({
    type: "GET",
    url:"/home",  
    async : false,
   
   success:function(jsons){
   	alert('back to homepage');
   },
    error: function(){
    alert('error during the callback2');
	},
	});
//////////////////////////////////////


   },

   });


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


/* var song_rate = document.getElementById("song_rate").value;*/

$(function () { 
         
  $('.rating2').each(function(index,value){
     
  //  console.log($('#'+index).text());
      
      
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



    document.getElementById('unload').disabled=true;
    document.getElementById('load2').disabled=true;

  });
         
  $('.swtich_page').each(function(index,value){
    
      
     $('#'+'queue_'+index).click(function(){         
         if ($('#titre_1').text()=='empty') {

                  //console.log('titre_1');  
                 
                  $('#titre_1').text($('.next_song_'+index).val());
                  $('.titre_1').val($('.next_song_'+index).val());
                  $('#element_'+index).hide();
                  document.getElementById('load2').disabled=false;
                  document.getElementById('unload').disabled=false;
             
            }else if ($('#titre_2').text()=='empty') {
              $('#titre_2').text($('.next_song_'+index).val());
              $('.titre_2').val($('.next_song_'+index).val());
              $('#element_'+index).hide();


            } else if ($('#titre_1').text()!=='empty' && $('#titre_2').text()!=='empty'){
                alert('queue full ! delete songs');
               
      
              

             
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
