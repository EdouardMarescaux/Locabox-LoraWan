<?php
$string1 = '//44hKsIt2Q=';
$binary = base64_decode($string1);
$hex = bin2hex($binary);
echo $hex;
?>