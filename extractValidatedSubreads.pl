#!/usr/bin/perl

$identity_threshold = 55.0;
$extreme_threshold  = 200;
while (<>) {
    chomp();
    $_ =~ /(.*?) (.*?) (.*?) (.*?) (.*?) (.*?) (.*?) (.*?) (.*?)/;
    $subread_length = $3;
    $identity = $4;
    $overlap_length = $5;
    $plus_start = $6;
    $plus_end = $7;
    $minus_start = $8;
    $minus_end = $9;

    if ($overlap_length == 0 || $identity < $identity_threshold) {
	next;
    }
    if ($plus_start > $extreme_threshold && $plus_end < $subread_length - $extreme_threshold) { 
	next;
    }
    if ($minus_start > $extreme_threshold && $minus_end < $subread_length - $extreme_threshold) {
	next;
    }

    print $_;
    if ($plus_start <= $extreme_threshold && $plus_end >= $subread_length - $extreme_threshold) {
	print " complete\n";
    } else {
	print " partial\n";
    }
}
