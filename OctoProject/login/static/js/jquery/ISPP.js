$(document).ready(function() {
    $('#product').DataTable();
} );				


function geturl(c){
	var x = document.getElementById("playcontext").value+c;
	document.getElementById("playlink").value=c;
	url='http://demo.octoshape.com/arplayer3/?link='+x
	document.getElementById("urlstream").src=url
	}

	
function putThis(control) { 
	    document.getElementById("streamviewname").value=control.innerText
	    document.getElementById("Holgerinp").value=control.innerText
	}
	

function editstream(x)
{		    if ( confirm('You are about to edit the stream'+x+')== true'){} 
		    else 		    
		    {document.getElementById("searchresult").innerHTML ="Action Canceled. Try Again";  }}



function getauth(){
	var c=document.getElementById("playlink").value;
	var authpsw=document.getElementById("authpsw").value;	
	url='http://demo.octoshape.com/arplayer3/?link='+document.getElementById("playcontext").value+c+'&psw='+authpsw
	document.getElementById("urlstream").src=url

	}