$('document').ready(function(){    
var track= document.getElementById('TRACK').innerText;
console.log(track); 
$.ajax({
    type: "GET",
    url:"/LL",  
  //  data: { track_pseudo: track },  
    dataType: 'json',
   success:function(jsons){
        console.log('reussi');
        var data = JSON.stringify(jsons);
        console.log(data[0]);


        var data2=JSON.parse(data);
        console.log(data2);
        //console.log(data2['0']);
        $.each(data2, function(key, value){
       // console.log(key, value);
        if (key.startsWith('#song_rate') == true){
          $(key).val(value);       
         
        }else if (key.startsWith('image') == true){
         
          document.getElementById(key).src =value;
        }else{
           
        $(key).text(value);
      }


      });                     
     },
   error: function(){
    alert('error during the callback');
   }
   });

});
 
