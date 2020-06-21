.name "All operations"
.comment ""
live:
 live%:live
	ld 25,r01	
 	ld%:live,r2 
st r1, 25
  	st r1,r8 
 
 add r1,r2 , r3	
	sub r3  ,r1, r5
	and r1, r2, r3


	and r1, 25, r5
	and r1, %125,r5
	and 25, r1, r1

	and 122, 125,r2
	and 001, %128090,r3
	and %005, r8, r3
	and %-35, -123, r3
	and %0, 8, r99

	or r1, r2, r3
	or r1, 25, r5
	or r1, %125,r5
	or 25, r1, r1

	or 122, 125,r2
	or 001, %128095,r3
	or %005, r8, r3
	or %-35, -123, r3
	or %0, 8, r99	  
	xor r1, r2, r3
	xor r1, 25, r5
	xor r1, %125,r5
	xor 25, r1, r1

	xor 122, 125,r2
	xor 001, %128095,r3
	xor %005, r8, r3
	xor %-35, -123, r3
	xor %0, 8, r99
    zjmp    %:live
		ldi r1,%008,r3
	ldi r12,r23, r3
	ldi 75,%008, r3
	ldi %80, r1, r5
	ldi 000, %00, r0
	ldi %0, r10,r09

	sti r1, r02, r03
	sti r00, r90, %009
	sti r23, %5 , r8
	sti r57, %999, %25
	sti r08, 12345, r5
	sti r89,:live, %12
	fork %1234567
	lld%025,   r12
	lld 25, r12

	lldi r1,%008,r3
	lldi r12,r12, r3
	lldi 75,%008, r3
	lldi %80, r1, r5
	lldi 000, %00, r0
	lldi %0,  %:live,r09
	lfork %12
	aff r01
