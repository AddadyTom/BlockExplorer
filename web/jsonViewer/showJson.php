<?php
$blockNumber = $_REQUEST['blockNumber'];
if (is_numeric($blockNumber)) {
	$str = file_get_contents("../../transactions/{$blockNumber}.json");
} else {
	die("Sorry json file doesn't exist");
}
#$json = json_decode($str, true);
echo '<html>
<head>
	<title>jJsonViewer</title>

	<link rel="stylesheet" href="css/jjsonviewer.css">
</head>
<body>
	<div id="jjson" class="jjson"></div>

	<script type="text/javascript" src="js/lib/jquery.js"></script>
	<script type="text/javascript" src="js/jjsonviewer.js"></script>
	<script type="text/javascript">
		$(document).ready(function() {
			var jjson = '.$str.';
			$("#jjson").jJsonViewer(jjson);
		});
	</script>
</body>
</html>';
?>
