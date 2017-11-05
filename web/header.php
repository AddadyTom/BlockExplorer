<?php
$header = "
<html>
	<head>
		<title>
			Block Explorer
				</title>
				<link rel=\"stylesheet\" href=\"css/style.css\">
				<!-- Global site tag (gtag.js) - Google Analytics -->


				<script async src=\"https://www.googletagmanager.com/gtag/js?id=UA-109203176-1\"></script>
				<script>
					  window.dataLayer = window.dataLayer || [];
					  function gtag(){dataLayer.push(arguments);}
					  gtag('js', new Date());
					  gtag('config', 'UA-109203176-1');
				</script>

	</head>
	<body>
		<script type='text/javascript'>
			//Popup window code
			function newPopup(url) {
		
				window.open(url,\"winname\",\"directories=no,titlebar=no,toolbar=no,location=no,status=no,menubar=no,scrollbars=no,resizable=no,width=700,height=550\");	

			}
		</script>
		<ul>
		  <li><a href=\"index.php\">Home</a></li>
		  <li><a href=\"index.php?type=account_create\">Account create</a></li>
		  <li><a href=\"index.php?type=transfer\">Transfer</a></li>
		  <li><a href=\"about.php\">About</a></li>
		</ul>
		<center>
		<table class=\"table-fill\"><tr>
		
		";
//		popupWindow = window.open(	
//												url,\'popUpWindow\',\'height=300,width=400,left=10,top=10,resizable=no,scrollbars=yes,toolbar=no,menubar=no,location=no,directories=no,status=yes\')						
//		
?>
