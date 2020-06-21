     .name     "Negative arg Values "
	 .comment ""

	 	st r1,-08 
	 					 12345:
 	and r1, %-1,r5
	and -025, -1230, r1

	or %-03500,-123, r3
	or %-0, -8, r99	  
	xor -001, %-127805,r3
	xor %-005, r8, r3
	xor :12345, -8, r99
	ldi -000, %-00, r0
	ldi %0,r01,r08
