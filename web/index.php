<?php
include "bottom.php";
include "header.php";
include "details.php";



if (!mysql_connect($db_host, $db_user, $db_pwd))
		    die("Can't connect to database");

if (!mysql_select_db($database))
		die("Can't select database");
$isSearch = False;
//adjusting the requested table fileds parameters according to parameters that had been sent. 
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	if (isset($_POST['search1']) || isset($_POST['search'])) {
			$isSearch = True;
			if (isset($_POST['current'])){
				$current = $_POST['current'];	
				if (isset($_POST['next'])) {
						$current = $current + $howManyToShow;		          
				} else {
					$current = $current - $howManyToShow;		          	
				}	
				$table = $_POST['type'];
			} else {
				$table = $_POST['type'];
				#$table = "all_transaction";
				$current = 0;
			}
	} else {
		$current = $_POST['current'];	
		//something posted
		if (isset($_POST['next'])) {
			$current = $current + $howManyToShow;		          	
		} else {
		$current = $current - $howManyToShow;		          	
		}
		$table = $_POST['type'];
	}
} else if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['type'])) {
	if (isset($_GET['search'])) {
		$isSearch = True;
	}
	$table = $_GET['type'];
	$current = 0;
}else {
	$current = 0;
	$whereTo = $howManyToShow;
	$table = "all_transaction";
}
//sending query
if ($isSearch){
	#$query = mysqli_real_escape_string($_REQUEST['search']);
	$query = $_REQUEST['search'];
	$searchFor = $_REQUEST['whatToSearchFor'];
#	echo "mysql_query(\"SELECT * FROM {$table}
#			WHERE ({$searchFor} LIKE '%\"$query\"%') LIMIT {$current} , {$howManyToShow}\") or die(mysql_error());";
	$result = mysql_query("SELECT * FROM {$table}
			WHERE ({$searchFor} LIKE '%".$query."%')  ORDER BY BlockNumber DESC LIMIT {$current} , {$howManyToShow}") or die(mysql_error());
}else {
	$result = mysql_query("SELECT * FROM {$table} ORDER BY time DESC LIMIT {$current} , {$howManyToShow}");
}
echo $header;

if (!$result) {
		// die("Query to show fields from table failed");
		echo "<h1>no more results to shoe please press beck</h1>";
}

$fields_num = mysql_num_fields($result);
echo "<h3> page : ".toNiceString($table)."</h3>";
if (mysql_num_rows($result) == 0) {
		echo "<h1>No Result to show</h1>";
} else {
	$temp = $result;	
	if (!$isSearch) {
			echo "<form  action=\"index.php\" method=\"POST\">
					<select class=\"form-select\" name='whatToSearchFor' width=\"10px\">
					<option value=\"\" disabled selected>Search for</option>";
			for($i=0; $i<$fields_num; $i++){
	   	 $field = mysql_fetch_field($result);
   	     echo "<option value={$field->name}>{$field->name}</option>";
	}

			echo" </select> &nbsp 
					<input type=\"text\" name=\"search\" placeholder=\"search in {$table}\" >
			<input type=\"hidden\" name=\"type\" value='$table'> &nbsp 
			<input type=\"submit\" class=\"button button1\" value=\"search\" name=\"search1\" />

		</form>";
	}

	echo "<thead>
			<tr>";
	// printing table headers
	for($i=0; $i<$fields_num; $i++){
	   	 $field1 = mysql_fetch_field($temp,$i);
   	     echo "<th>".toNiceString($field1->name)."</th>";
	}
	if($table == "all_transaction") {
		echo "<th>View</th>";
		echo "<th>Icon</th>";
		echo "<th>Json</th>";

	}
	echo "
			</tr>
			</thead>
			<tbody class=\"table-hover\">";

// printing table rows
while($row = mysql_fetch_row($result))
{
    echo "<tr>";

        // $row is array... foreach( .. ) puts every element
	// of $row to $cell variable
	$firstIterate = True; 
	$whichOpertion = $row[0];
//	$blockNumber = $row[1];
	foreach($row as $cell) {
			 echo "<td>".toNiceString($cell)."</td>";
	 }
	if($table == "all_transaction") {
		if (isImportantOperation($whichOpertion)) {
			//		"<td><a href='".$row[$key]."'".$row[$key]."</a></td>"
					echo "<td><a href='?search={$row[1]}&type={$whichOpertion}&whatToSearchFor=blockNumber'>show</a></td>";
		} else {
				echo "<td>Not Available</td>";
		}


		if (file_exists('icon/'.$whichOpertion.'.gif')) {
				echo "<td><img src=\"icon/{$whichOpertion}.gif\" style=\"width:20px;height:20px;\"></td>";
		} else {
				echo "<td><img src=\"icon/transparent.gif\" style=\"width:20px;height:20px;\"></td>";
		}
		echo "<td><p><a href=\"JavaScript:newPopup('/jsonViewer/showJson.php?blockNumber={$row[1]}');\"> json </a></p></td>";
	}


	 echo "</tr>\n";
}
}
echo "</tbody></table>";
//if its not a search
if (!$isSearch) {
		//if its not the first table (next has been clicked)
		if ($current > 0) {
				//if there is a need to show next
			if (mysql_num_rows($result) == $howManyToShow){
				echo '</br></table><form class="submitClass" action="index.php" method="POST">
					<input type="submit" value="prev" name="prev"/>
				    <input type="submit" value="next" name="next" />
					<input type="hidden" name="type" value='.$table.'>
					<input type="hidden" name="current" value='.$current.'>
					</br>
					</form>	';
			} else {
				echo '</br></table><form class="submitClass" action="index.php" method="POST">
					<input type="submit" value="prev" name="prev"/>
				    <input type="submit" value="next" name="next" />
					<input type="hidden" name="type" value='.$table.'>
					<input type="hidden" name="current" value='.$current.'>
					</br>
					</form>	';
			}
		} else {
			if (mysql_num_rows($result) == $howManyToShow){
				echo '</br></table><form class="submitClass" action="index.php" method="POST">
			    <input type="submit" value="next" name="next" />
				<input type="hidden" name="type" value='.$table.'>
				<input type="hidden" name="current" value='.$current.'>
				</form>	';
			} else {
				echo '</br></table><form class="submitClass" action="index.php" method="POST">
					<input type="hidden" name="type" value='.$table.'>
					<input type="hidden" name="current" value='.$current.'>
			</br>	<a href="javascript:history.back()">Go Back</a>
					</form>	';
			}
	}
} else {
	if ($current > 0) {
			if (mysql_num_rows($result) == $howManyToShow){
				echo '</br></table><form class="submitClass" action="index.php" method="POST">
					<input type="submit" value="prev" name="prev"/>
				    <input type="submit" value="next" name="next" />
					<input type="hidden" name="whatToSearchFor" value='.$searchFor.'>
					<input type="hidden" name="search" value='.$query.'>
					<input type="hidden" name="type" value='.$table.'>
					<input type="hidden" name="current" value='.$current.'>
					</form>	';
			}
			else {
				echo '</br></table><form class="submitClass" action="index.php" method="POST">
					<input type="submit" value="prev" name="prev"/>
					<input type="hidden" name="search" value='.$query.'>
					<input type="hidden" name="whatToSearchFor" value='.$searchFor.'>
					<input type="hidden" name="type" value='.$table.'>
					<input type="hidden" name="current" value='.$current.'>
					</form>	';
			}
	} else {
			if (mysql_num_rows($result) == $howManyToShow){
				echo '</br></table><form class="submitClass" action="index.php" method="POST">
				    <input type="submit" value="next" name="next" />
					<input type="hidden" name="search" value='.$query.'>
					<input type="hidden" name="whatToSearchFor" value='.$searchFor.'>
					<input type="hidden" name="type" value='.$table.'>
					<input type="hidden" name="current" value='.$current.'>
					</form>	';
			} else {
				echo '</br></table><form class="submitClass" action="index.php" method="POST">
					<input type="hidden" name="search" value='.$query.'>
					<input type="hidden" name="type" value='.$table.'>
					<input type="hidden" name="whatToSearchFor" value='.$searchFor.'>
					<input type="hidden" name="current" value='.$current.'>
			</br>	<a href="javascript:history.back()">Go Back</a>
					</form>	';
			}
	}
}

mysql_free_result($result);
echo $bottom;
function isImportantOperation($x) {
	if ($x == "account_create" || $x == "transfer"){  
			return true;
	}
	return false;
}
function toNiceString($str) {
	$str = ucfirst($str);
	$str = str_replace("_", " ",$str);
	return $str;
	

}
?>
							
