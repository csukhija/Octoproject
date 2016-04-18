$(function(){	
var cpcode =[
    { value: 'Digiturk1', data: 'AKAM89213979' },
    { value: 'abs-cbn', data: 'AKAMxxxx'},
    { value: 'abudhabi', data: 'AKAMxxxx' },
    { value: 'airties', data: 'AKAMxxxx' },
    { value: 'akamai', data: 'Debtor'},
    { value: 'Pros7', data: 'Debtor'},
    { value: 'brainsonic', data: 'Debtor' },
    { value: 'datco', data: 'Tur29'},
    { value: 'Turner', data: 'Tur29'},
    { value: 'cisco', data: 'AKAMxxxx' },
    { value: 'Turner', data: 'Tur2922' },
    { value: 'encompass', data: 'AKAM1xxxx' },
    { value: 'forevertek', data: 'AKAMxxxx' },
    { value: 'hanyastar', data: 'AKAMxxx3x' },
    { value: 'movingimage24', data: 'AKAMx12xxx' },
    { value: 'presumiendomexico', data: 'AKAMxx12xx' },
    { value: 'viacom', data: 'AKAMxx2xx' },
    { value: 'Digiturk', data: 'AKAMx3xxx' },  
    { value: 'vivoplay', data: 'AKAMx3xxx' },
  ];
  
  // setup autocomplete function pulling from cpcode[] array
  $('#autocomplete').autocomplete({
    lookup: cpcode,
    onSelect: function (suggestion) {
      var thehtml = '<strong>Customer Name:</strong> ' 
    	  			+ suggestion.value + ' <br> <strong>CP Code:</strong> ' 
    	  			+ suggestion.data;
      $('#outputcontent').html(thehtml);
      $('#streamnamesearch').val(suggestion.stream);
      
    }
  });
  
 

});