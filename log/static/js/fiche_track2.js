$('document').ready(function(){ 
var tracksss= document.getElementById('TRACK').innerText;
var pictures=document.getElementById('wcloud_picture1').src;

       
     
     
      $('#submit').click(function(){
        
        if($('.rating').val()>0){

       $('#rating3').hide();
        
        console.log('hide');
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
  



});


// function for getting back the length of the song
/////////////////////////////////////
var time = document.getElementById("myAudio");
  
  function getCurTime() { 
       alert((time.currentTime/length.duration)*100);   
         
      // $('#lol2').text(time.currentTime); 
       //$('#listening_time').text(time.currentTime); 
       
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
   // var progress = document.querySelector('.progress-bar');
    // progress.style.width = percent + '%';

    // progress.textContent = percent + '%';  
    //$('#lol2').text(fraction); 
    //$('.listening_time').each(function(){
    //$(this).val(time);
    //}); 
    $('.listening_time').val(time);
    $('.percentage').val(fraction); 
    $('.listening_time2').val(time);
    $('.percentage2').val(fraction); 
    $('.time_before_rated').val(time);

    //$('.percentage').each(function(){
    //  $(this).val(fraction);
    //});
};

///////////////// text lyrics

  

// rating
/////////////////////////

 $(function () { 
       $('.rating').rating();           
       
        $('.rating').on('change', function () {
           $('#heart-rate').text($(this).val());
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
