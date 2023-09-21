#!/usr/bin/perl

use strict;

my $b1 = int(rand(125.9))+1;
print "_IP01_ = $b1.0.0.0\n";

my $b3 = int(rand(98.9))+10;

my $b2 = int(rand(15.9))+16;

my $b1 = int(rand(31.9))+192;

my $b2 = $b1;
my $b1 = int(rand(63.9))+128;
print "_IP02_ = $b1.$b2.128.0/17\n";

my $b1 = int(rand(125.9))+1;

my $b1 = int(rand(31.9))+192;
my $s4 = int(rand(3.9));
my $b4 = $s4 * 64;
print "_IP03_ = $b1.0.$b2.132/26\n";

my $b1 = int(rand(63.9))+128;
my $b2 = int(rand(254.9));

my $b1 = int(rand(125.9))+1;

my $b3 = int(rand(63.9))+128;

my $b1 = int(rand(31.9))+192;

my $b1 = int(rand(31.9))+192;
print "_IP04_ = $b1.0.0.128/25\n";

my $b1 = int(rand(63.9))+128;
print "_IP05_ = $b1.0.0.0/18\n";

my $b1 = int(rand(125.9))+1;
print "_IP06_ = $b1.64.0.0/10\n";

my $b1 = int(rand(31.9))+192;

my $b1 = int(rand(63.9))+128;

my $b1 = int(rand(31.9))+192;
print "_IP07A_ = $b1.0.0.32/27\n";
print "_IP07B_ = $b1.0.0.195/28\n";

my $b1 = int(rand(125.9))+1;
my $b2 = int(rand(254.9));
my $b4 = int(rand(254.9));
my $b1 = int(rand(31.9))+192;
my $b3 = int(rand(254.9));
my $b4 = int(rand(254.9));

my $b1 = int(rand(125.9))+1;

my $b1 = int(rand(125.9))+1;
my $b2 = int(rand(254.9));
print "_IP08_ = $b1.$b2.0.0/24\n";

my $b1 = int(rand(125.9))+1;
print "_IP09_ = $b1.0.224.0/14\n";

my $b1 = int(rand(125.9))+1;

my $b1 = int(rand(63.9))+128;
print "_IP10_ = $b1.0.180.0/23\n";


my $b1 = int(rand(31.9))+192;
my $b2 = int(rand(254.9));
my $b3 = int(rand(254.9));
print "_IP11_ = $b1.$b2.$b3.0/24\n";

