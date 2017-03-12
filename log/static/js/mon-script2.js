$('document').ready(function(){ 

    $('.panel-body').hide();
    $('#hide').hide();

    $('#hide').click(function(){
        $('.panel-body').hide();
        $('#hide').hide();
        $('#show').show();
        });

    $('#show').click(function(){
        $('.panel-body').show();
        $('#show').hide();
        $('#hide').show();
    
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
    var progress = document.querySelector('.progress-bar');
    progress.style.width = percent + '%';

    progress.textContent = percent + '%';  
    $('#lol2').text(fraction); 
    //$('.listening_time').each(function(){
    //$(this).val(time);
    //}); 
    $('.listening_time').val(time);
    $('.percentage').val(fraction); 
    $('.listening_time2').val(time);
    $('.percentage2').val(fraction); 
    //$('.percentage').each(function(){
    //  $(this).val(fraction);
    //});
};

///////////////// text lyrics
$(function () { 
var myVar = document.getElementById("lyrics_var").value;
//console.log(myVar);
$.ajax({
    type: "GET",

    url:"/static/lyrics/"+myVar+".txt",
    
    dataType: "text",
    async : false,
   success: function(text){lyrics(text);},
   error: function(){
    alert('can t open file or doesn t exist');
   }
   });
 //alert('2');
 console.log('2');
 function lyrics(text){
  var rows=text.split('\n'); 
  //console.log(rows);
  $('#lyrics').html(rows).text();
}
});
  

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
console.log('1');
$.ajax({
    type: "GET",

    url:"/static/list/token_list.csv",
    
    dataType: "text",
    async : false,
   success: function(text){parseTxt(text);},
   error: function(){
    alert('can t open file or doesn t exist');
   }
   });
 //alert('2');
 console.log('2');
 function parseTxt(text){
  //alert('success');

  var rows=text.split('\n'); 
  console.log(rows);
  $.each(rows, function( index, value ) {
    mot[index]=value;
  });
  //console.log(mot);
  
  };
  console.log(mot);
// tokenfield
//////////////////////////
console.log('3');
$('#tokenfield').tokenfield({

  autocomplete: {
    source:mot,
    //source: ['awesomeness'],
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
  console.log(mot);
    //var available_tokens = ['red','blue','green','yellow','violet','brown','purple','black','white','awesomeness'];
    var exists = false;
    $.each(mot, function( index, value ) {
            //console.log(value+","+event.attrs.value);

             if (value.replace('\r', '')==String(event.attrs.value)) {
              //console.log('equals');
              // console.log(value);
               exists = true;
            }
            // bizare si on retire value ca ne marche plus !!
            //console.log(event.attrs.value);
                   
    });
    if(exists === false)
        event.preventDefault();
});

       

});

