.comment  	" "
.name "Repeating labels"
	label:
		ld   %0,r2
		zjmp  %:label
			
label:	live %42
		fork %:label_1
label_1:	live %42
		ldi  %4,%:label,r15 		
		ld   %-190,r14			
		ld   %0,r2
		zjmp %:label
		
label_1:	live %42	
		ldi  %12,%:label_1,r15		
		ld   %-182,r14			
		ld   %0,r2
		zjmp %:label
 