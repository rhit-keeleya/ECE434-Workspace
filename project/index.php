<?php

	// MINIXED is a minimal but nice-looking PHP directory indexer.
	// More at https://github.com/lorenzos/Minixed
	/*
	 * MIT License
	 * Copyright (c) 2020 Lorenzo Stanco
	 *
	 * Permission is hereby granted, free of charge, to any person obtaining a copy
	 * of this software and associated documentation files (the "Software"), to deal
	 * in the Software without restriction, including without limitation the rights
	 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	 * copies of the Software, and to permit persons to whom the Software is
	 * furnished to do so, subject to the following conditions:
	 *
	 * The above copyright notice and this permission notice shall be included in all
	 * copies or substantial portions of the Software.
	 *
	 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	 * SOFTWARE.
	 */

	// =============================
	// Configuration                
	// =============================
	
	$browseDirectories = true; // Navigate into sub-folders
	$title = 'Index of {{path}}';
	$subtitle = '{{files}} objects in this folder, {{size}} total'; // Empty to disable
	$breadcrumbs = true; // Make links in {{path}}
	$showParent = true; // Display a (parent directory) link
	$showDirectories = true;
	$showDirectoriesFirst = true; // Lists directories first when sorting by name
	$showHiddenFiles = false; // Display files starting with "." too
	$alignment = 'left'; // You can use 'left' or 'center'
	$showIcons = true;
	$dateFormat = 'd/m/y H:i'; // Used in date() function
	$sizeDecimals = 1;
	$robots = 'noindex, nofollow'; // Avoid robots by default
	$showFooter = true; // Display the "Powered by" footer
	$openIndex = $browseDirectories && true; // Open index files present in the current directory if $browseDirectories is enabled
	$browseDefault = null; // Start on a different "default" directory if $browseDirectories is enabled
	$ignore = array('index.php', 'execute.sh', 'php.log'); // Names of files and folders to not list (case-sensitive)
	
	// =============================
	// =============================
	
	// Who am I?
	$_self = basename($_SERVER['PHP_SELF']);
	$_path = str_replace('\\', '/', dirname($_SERVER['PHP_SELF']));
	$_total = 0;
	$_total_size = 0;
	$name = getTitleHTML($title);
	
	// Directory browsing
	$_browse = null;
	if ($browseDirectories) {
		if (!empty($browseDefault) && !isset($_GET['b'])) $_GET['b'] = $browseDefault;
		$_GET['b'] = trim(str_replace('\\', '/', (string)@$_GET['b']), '/ ');
		$_GET['b'] = str_replace(array('/..', '../'), '', (string)@$_GET['b']); // Avoid going up into filesystem
		if (!empty($_GET['b']) && $_GET['b'] != '..' && is_dir($_GET['b'])) {
			$browseIgnored = false;
			foreach (explode('/', $_GET['b']) as $browseName) {
				if (!empty($ignore) && is_array($ignore) && in_array($browseName, $ignore)) {
					$browseIgnored = true;
					break;
				}
			}
			if (!$browseIgnored) $_browse = $_GET['b']; // Avoid browsing ignored folder names
		}
	}
	
	// Index open
	if (!empty($_browse) && $openIndex) {
		$_index = null;
		if (file_exists($_browse . "/index.htm")) $_index = "/index.htm";
		if (file_exists($_browse . "/index.html")) $_index = "/index.html";
		if (file_exists($_browse . "/index.php")) $_index = "/index.php";
		if (!empty($_index)) {
			header('Location: ' . $_browse . $_index);
			exit();
		}
	}

	// Encoded images generator
	if (!empty($_GET['i'])) {
		header('Content-type: image/png');
		switch ($_GET['i']) {
			case       'asc': exit(base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAcAAAAHCAYAAADEUlfTAAAAFUlEQVQImWNgoBT8x4JxKsBpAhUAAPUACPhuMItPAAAAAElFTkSuQmCC'));
			case      'desc': exit(base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAcAAAAHCAYAAADEUlfTAAAAF0lEQVQImWNgoBb4j0/iPzYF/7FgCgAADegI+OMeBfsAAAAASUVORK5CYII='));
			case 'directory': exit(base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAASklEQVQYlYWPwQ3AMAgDb3Tv5AHdR5OqTaBB8gM4bAGApACPRr/XuujA+vqVcAI3swDYjqRSH7B9oHI8grbTgWN+g3+xq0k6TegCNtdPnJDsj8sAAAAASUVORK5CYII='));
			case      'file': exit(base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAPklEQVQYlcXQsQ0AIAhE0b//GgzDWGdjDCJoKck13CsIALi7gJxyVmFmyrsXLHEHD7zBmBbezvoJm4cL0OwYouM4O3J+UDYAAAAASUVORK5CYII='));
		}
	}
	
	// I'm not sure this function is really needed...
	function ls($path, $show_folders = false, $show_hidden = false) {
		global $_self, $_total, $_total_size, $ignore;
		$ls = array();
		$ls_d = array();
		if (($dh = @opendir($path)) === false) return $ls;
		if (substr($path, -1) != '/') $path .= '/';
		while (($file = readdir($dh)) !== false) {
			if ($file == $_self) continue;
			if ($file == '.' || $file == '..') continue;
			if (!$show_hidden) if (substr($file, 0, 1) == '.') continue;
			if (!empty($ignore) && is_array($ignore) && in_array($file, $ignore)) continue;
			$isdir = is_dir($path . $file);
			if (!$show_folders && $isdir) continue;
			$item = array('name' => $file, 'isdir' => $isdir, 'size' => $isdir ? 0 : filesize($path . $file), 'time' => filemtime($path . $file));
			if ($isdir) $ls_d[] = $item; else $ls[] = $item;
			$_total++;
			$_total_size += $item['size'];
		}
		return array_merge($ls_d, $ls);
	}
	
	// Get the list of files
	$items = ls('.' . (empty($_browse) ? '' : '/' . $_browse), $showDirectories, $showHiddenFiles);
	
	// Sort it
	function sortByName($a, $b) { global $showDirectoriesFirst; return ($a['isdir'] == $b['isdir'] || !$showDirectoriesFirst ? strtolower($a['name']) > strtolower($b['name']) : $a['isdir'] < $b['isdir']) ? 1 : -1; }
	function sortBySize($a, $b) { return ($a['isdir'] == $b['isdir'] ? $a['size'] > $b['size'] : $a['isdir'] < $b['isdir']) ? 1 : -1; }
	function sortByTime($a, $b) { return ($a['time'] > $b['time']) ? 1 : -1; }
	switch (@$_GET['s']) {
		case 'size': $_sort = 'size'; usort($items, 'sortBySize'); break;
		case 'time': $_sort = 'time'; usort($items, 'sortByTime'); break;
		default    : $_sort = 'name'; usort($items, 'sortByName'); break;
	}
	
	// Reverse?
	$_sort_reverse = (@$_GET['r'] == '1');
	if ($_sort_reverse) $items = array_reverse($items);
	
	// Add parent
	if ($showParent && $_path != '/' && empty($_browse)) array_unshift($items, array(
		'name' => '..',
		'isparent' => true,
		'isdir' => true,
		'size' => 0,
		'time' => 0
	));

	// Add parent in case of browsing a sub-folder
	if (!empty($_browse)) array_unshift($items, array(
		'name' => '..',
		'isparent' => false,
		'isdir' => true,
		'size' => 0,
		'time' => 0
	));
	
	// 37.6 MB is better than 39487001
	function humanizeFilesize($val, $round = 0) {
		$unit = array('','K','M','G','T','P','E','Z','Y');
		do { $val /= 1024; array_shift($unit); } while ($val >= 1000);
		return sprintf('%.'.intval($round).'f', $val) . ' ' . array_shift($unit) . 'B';
	}
	
	// Titles parser
	function getTitleHTML($title, $breadcrumbs = false) {
		global $_path, $_browse, $_total, $_total_size, $sizeDecimals;
		$title = htmlentities(str_replace(array('{{files}}', '{{size}}'), array($_total, humanizeFilesize($_total_size, $sizeDecimals)), $title));
		$path = htmlentities($_path);
		if ($breadcrumbs) $path = sprintf('<a href="%s">%s</a>', htmlentities(buildLink(array('b' => ''))), $path);
		if (!empty($_browse)) {
			if ($_path != '/') $path .= '/';
			$browseArray = explode('/', trim($_browse, '/'));
			foreach ($browseArray as $i => $part) {
				if ($breadcrumbs) {
					$path .= sprintf('<a href="%s">%s</a>', htmlentities(buildLink(array('b' => implode('/', array_slice($browseArray, 0, $i + 1))))), htmlentities($part));
				} else {
					$path .= htmlentities($part);
				}
				if (count($browseArray) > ($i + 1)) $path .= '/';
			}
		}
		return str_replace('{{path}}', $path, $title);
	}
	
	// Link builder
	function buildLink($changes) {
		global $_self;
		$params = $_GET;
		foreach ($changes as $k => $v) if (is_null($v)) unset($params[$k]); else $params[$k] = $v;
		foreach ($params as $k => $v) $params[$k] = urlencode($k) . '=' . urlencode($v);
		// want to remove actions, as they are handled in another function
		unset($params['action']);
		return empty($params) ? $_self : $_self . '?' . implode('&', $params);
	}

	// Determines action based on folder path
	function actionName($cur_path) {
		if(strpos($cur_path, "temporary") !== false){
			return "Archive";
		} else if(strpos($cur_path, "permanent") !== false){
			return "Delete";
		} else {
			return "N/A";
		}
	}

	function isEvent($cur_path) {
		if(strpos($cur_path, "event") !== false){
			return true;
		}
		return false;
	}

	function clickLink($buttonName, $file) {
		return buildLink(null) . "&" . "action=" . $buttonName . "+" . $_GET['b'] . "/" . $file;
	}

	// Executes script based on action
	if(strpos($_GET['action'], " ") !== false){
		$parameter = explode(" ", $_GET['action']);
		// what we want to /do/ - either archive or delete
		$do = $parameter[0] . " ";
		// /directory/ we want to /do/ things to
		$directory = $parameter[1];
		exec("echo Event: " . $do . $directory . " detected... >> php.log 2>&1");
		exec("./execute.sh " . $do . $directory . " >> php.log 2>&1");
		// redirect user up a level
		$redirect = buildLink(array('b' => exec("dirname " . $directory)));
		header("Location: " . $redirect);
	}
?>
<!DOCTYPE HTML>
<html lang="en-US">
<head>
	
	<meta charset="UTF-8">
	<meta name="robots" content="<?php echo htmlentities($robots) ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	
	<title><?php echo getTitleHTML($title) ?></title>
	
	<style type="text/css">
		
		* {
			margin: 0;
			padding: 0;
			border: none;
			background-color: black;
		}
		
		body {
			text-align: center;
			font-family: sans-serif;
			font-size: 13px;
			color: #999999;
		}
		
		#wrapper {
			max-width: 600px;
			*width: 600px;
			margin: 0 auto;
			text-align: left;
		}
		
		body#left {
			text-align: left;
		}
		
		body#left #wrapper {
			margin: 0 20px;
		}
		
		h1 {
			font-size: 21px;
			padding: 0 10px;
			margin: 20px 0 0;
			font-weight: bold;
		}
		
		h2 {
			font-size: 14px;
			padding: 0 10px;
			margin: 10px 0 0;
			color: #999999;
			font-weight: normal;
		}
		
		a {
			color: #003399;
			text-decoration: none;
		}
		
		a:hover {
			color: #0066cc;
			text-decoration: underline;
		}
		
		ul#header {	
			margin-top: 20px;
		}
		
		ul li {
			display: block;
			list-style-type: none;
			overflow: hidden;
			padding: 10px;
			background-color: #121212;
		}
		
		ul li:hover {
			background-color: #101010;
		}
		
		ul li .date {
			text-align: center;
			width: 120px;
			background-color: #121212;
		}
		
		ul li .size {
			text-align: center;
			width: 90px;
			background-color: #121212;
		}

		ul li .action {
			width: 90px;
			text-align: center;
		}

		li .date, li .size, li .action { 
			float: right; 
			font-size: 12px; 
			display: block;
			background-color: #121212;
		}

		ul#header li {
			font-size: 11px;
			font-weight: bold;
			border-bottom: 1px solid #cccccc;
		}
		
		ul#header li:hover {
			background-color: transparent;
		}
		
		ul#header li a:hover {
			color: #666666;
		}
		
		ul#header li .asc span, ul#header li .desc span {
			padding-right: 15px;
			background-position: right center;
			background-repeat: no-repeat;
			background-color: #121212;
		}
		
		ul#header li .asc span {
			background-image: url('<?php echo $_self ?>?i=asc');
		}
		
		ul#header li .desc span {
			background-image: url('<?php echo $_self ?>?i=desc');
		}
		
		ul li.item {
			border-top: 1px solid #f3f3f3;
		}
		
		ul li.item:first-child {
			border-top: none;
		}
		
		ul li.item .name {
			font-weight: bold;
			background-color: #121212;
		}
		
		ul li.item .directory, ul li.item .file {
			padding-left: 20px;
			background-position: left center;
			background-repeat: no-repeat;
		}
		
		ul li.item .directory {
			background-image: url('<?php echo $_self ?>?i=directory');
		}
		
		ul li.item .file {
			background-image: url('<?php echo $_self ?>?i=file');
		}

		button.navigation {
			border-style: solid;
			border-width: medium;
			border-color: white;
			background-color: #90EE90;
			transition-duration: 0.4s;
			cursor: pointer;
			color: black;
			width: 288px;
		}
		
		button.action {
			border-style: solid;
			border-width: medium;
			border-color: white;
			background-color: #90EE90;
			display: inline-block;
			transition-duration: 0.4s;
			cursor: pointer;
			color: black;
		}
		
		#footer {
			color: #cccccc;
			font-size: 11px;
			margin-top: 40px;
			margin-bottom: 20px;
			padding: 0 10px;
			text-align: left;
		}
		
		#footer a {
			color: #cccccc;
			font-weight: bold;
		}
		
		#footer a:hover {
			color: #999999;
		}
		
	</style>
	
</head>
<body <?php if ($alignment == 'left') echo 'id="left"' ?>>

	<div id="wrapper">
		
		<h1><?php echo getTitleHTML($title, $breadcrumbs) ?></h1>
		<h2><?php echo getTitleHTML($subtitle, $breadcrumbs) ?></h2>
		
		<ul id="header">
			<li>
				<a href="<?php echo buildLink(array('b' => 'temporary')) ?>"><button class="navigation">Temporary Files</button></a>
				<a href="<?php echo buildLink(array('b' => 'permanent')) ?>"><button class="navigation">Permanent Files</button></a>
			</li>
			<li>
				<span class = "action">Action</span>
				<a href="<?php echo buildLink(array('s' => 'size', 'r' => (!$_sort_reverse && $_sort == 'size') ? '1' : null)) ?>" class="size <?php if ($_sort == 'size') echo $_sort_reverse ? 'desc' : 'asc' ?>"><span class = "size">Size</span></a>
				<a href="<?php echo buildLink(array('s' => 'time', 'r' => (!$_sort_reverse && $_sort == 'time') ? '1' : null)) ?>" class="date <?php if ($_sort == 'time') echo $_sort_reverse ? 'desc' : 'asc' ?>"><span class = "date">Last modified</span></a>
				<a href="<?php echo buildLink(array('s' =>  null , 'r' => (!$_sort_reverse && $_sort == 'name') ? '0' : null)) ?>" class="name <?php if ($_sort == 'name') echo $_sort_reverse ? 'desc' : 'asc' ?>"><span class = "name">Name</span></a>
			</li>
			
		</ul>
		<ul>
			
			<?php foreach ($items as $item): ?>
				
				<li class="item">

					<?php if (!$item['isdir']) {	?>
						<a href="<?php echo clickLink(actionName(getTitleHTML($title, $breadcrumbs)), $item['name']) ?>"><button class="action"><?php echo actionName(getTitleHTML($title, $breadcrumbs)) . " Event" ?></button></a>	
					<?php } else { ?>
							<span class = "action ">-</span>
					<?php } ?>
				
					<span class="size"><?php echo $item['isdir'] ? '-' : humanizeFilesize($item['size'], $sizeDecimals) ?></span>
					
					<span class="date"><?php echo (@$item['isparent'] || empty($item['time'])) ? '-' : date($dateFormat, $item['time']) ?></span>
					
					<?php
						if ($item['isdir'] && $browseDirectories && !@$item['isparent']) {
							if ($item['name'] == '..') {
								$itemURL = buildLink(array('b' => substr($_browse, 0, strrpos($_browse, '/'))));
							} else {
								$itemURL = buildLink(array('b' => (empty($_browse) ? '' : (string)$_browse . '/') . $item['name']));
							}
						} else {
							$itemURL = (empty($_browse) ? '' : str_replace(['%2F', '%2f'], '/', rawurlencode((string)$_browse)) . '/') . rawurlencode($item['name']);
						}
					?>
					
					<a href="<?php echo htmlentities($itemURL) ?>" class="name <?php if ($showIcons) echo $item['isdir'] ? 'directory' : 'file' ?>"><?php echo htmlentities($item['name']) . ($item['isdir'] ? ' /' : '') ?></a>
					
				</li>
				
			<?php endforeach; ?>
			
		</ul>
		
		<?php if ($showFooter): ?>
			
			<p id="footer">
				Powered by <a href="https://github.com/lorenzos/Minixed" target="_blank">Minixed</a>, a PHP directory indexer
			</p>
			
		<?php endif; ?>
		
	</div>
	
</body>
</html>
