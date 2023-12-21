;
; a3part-C.asm
;
; Part C of assignment #3
;
;
; Student name: Karen Xu
; Student ID: 
; Date of completed work: 3/26/2023
;
; **********************************
; Code provided for Assignment #3
;
; Author: Mike Zastre (2022-Nov-05)
;
; This skeleton of an assembly-language program is provided to help you 
; begin with the programming tasks for A#3. As with A#2 and A#1, there are
; "DO NOT TOUCH" sections. You are *not* to modify the lines within these
; sections. The only exceptions are for specific changes announced on
; Brightspace or in written permission from the course instruction.
; *** Unapproved changes could result in incorrect code execution
; during assignment evaluation, along with an assignment grade of zero. ***
;


; =============================================
; ==== BEGINNING OF "DO NOT TOUCH" SECTION ====
; =============================================
;
; In this "DO NOT TOUCH" section are:
; 
; (1) assembler direction setting up the interrupt-vector table
;
; (2) "includes" for the LCD display
;
; (3) some definitions of constants that may be used later in
;     the program
;
; (4) code for initial setup of the Analog-to-Digital Converter
;     (in the same manner in which it was set up for Lab #4)
;
; (5) Code for setting up three timers (timers 1, 3, and 4).
;
; After all this initial code, your own solutions's code may start
;

.cseg
.org 0
	jmp reset

; Actual .org details for this an other interrupt vectors can be
; obtained from main ATmega2560 data sheet
;
.org 0x22
	jmp timer1

; This included for completeness. Because timer3 is used to
; drive updates of the LCD display, and because LCD routines
; *cannot* be called from within an interrupt handler, we
; will need to use a polling loop for timer3.
;
.org 0x40
	jmp timer3

.org 0x54
	jmp timer4

.include "m2560def.inc"
.include "lcd.asm"

.cseg
#define CLOCK 16.0e6
#define DELAY1 0.01
#define DELAY3 0.1
#define DELAY4 0.5

#define BUTTON_RIGHT_MASK 0b00000001	
#define BUTTON_UP_MASK    0b00000010
#define BUTTON_DOWN_MASK  0b00000100
#define BUTTON_LEFT_MASK  0b00001000

#define BUTTON_RIGHT_ADC  0x032
#define BUTTON_UP_ADC     0x0b0   ; was 0x0c3
#define BUTTON_DOWN_ADC   0x160   ; was 0x17c
#define BUTTON_LEFT_ADC   0x22b
#define BUTTON_SELECT_ADC 0x316

.equ PRESCALE_DIV=1024   ; w.r.t. clock, CS[2:0] = 0b101

; TIMER1 is a 16-bit timer. If the Output Compare value is
; larger than what can be stored in 16 bits, then either
; the PRESCALE needs to be larger, or the DELAY has to be
; shorter, or both.
.equ TOP1=int(0.5+(CLOCK/PRESCALE_DIV*DELAY1))
.if TOP1>65535
.error "TOP1 is out of range"
.endif

; TIMER3 is a 16-bit timer. If the Output Compare value is
; larger than what can be stored in 16 bits, then either
; the PRESCALE needs to be larger, or the DELAY has to be
; shorter, or both.
.equ TOP3=int(0.5+(CLOCK/PRESCALE_DIV*DELAY3))
.if TOP3>65535
.error "TOP3 is out of range"
.endif

; TIMER4 is a 16-bit timer. If the Output Compare value is
; larger than what can be stored in 16 bits, then either
; the PRESCALE needs to be larger, or the DELAY has to be
; shorter, or both.
.equ TOP4=int(0.5+(CLOCK/PRESCALE_DIV*DELAY4))
.if TOP4>65535
.error "TOP4 is out of range"
.endif

reset:
; ***************************************************
; **** BEGINNING OF FIRST "STUDENT CODE" SECTION ****
; ***************************************************

; Anything that needs initialization before interrupts
; start must be placed here.

.def DATAH=r25  ;DATAH:DATAL  store 10 bits data from ADC
.def DATAL=r24
.def BOUNDARY_H=r1  ;hold high byte value of the threshold for button
.def BOUNDARY_L=r0  ;hold low byte value of the threshold for button, r1:r0

; Definitions for using the Analog to Digital Conversion
.equ ADCSRA_BTN=0x7A
.equ ADCSRB_BTN=0x7B
.equ ADMUX_BTN=0x7C
.equ ADCL_BTN=0x78
.equ ADCH_BTN=0x79

	rcall lcd_init ; call lcd_init to Initialize the LCD (line 689 in lcd.asm)

; ***************************************************
; ******* END OF FIRST "STUDENT CODE" SECTION *******
; ***************************************************

; =============================================
; ====  START OF "DO NOT TOUCH" SECTION    ====
; =============================================

	; initialize the ADC converter (which is needed
	; to read buttons on shield). Note that we'll
	; use the interrupt handler for timer 1 to
	; read the buttons (i.e., every 10 ms)
	;
	ldi temp, (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0)
	sts ADCSRA, temp
	ldi temp, (1 << REFS0)
	sts ADMUX, r16

	; Timer 1 is for sampling the buttons at 10 ms intervals.
	; We will use an interrupt handler for this timer.
	ldi r17, high(TOP1)
	ldi r16, low(TOP1)
	sts OCR1AH, r17
	sts OCR1AL, r16
	clr r16
	sts TCCR1A, r16
	ldi r16, (1 << WGM12) | (1 << CS12) | (1 << CS10)
	sts TCCR1B, r16
	ldi r16, (1 << OCIE1A)
	sts TIMSK1, r16

	; Timer 3 is for updating the LCD display. We are
	; *not* able to call LCD routines from within an 
	; interrupt handler, so this timer must be used
	; in a polling loop.
	ldi r17, high(TOP3)
	ldi r16, low(TOP3)
	sts OCR3AH, r17
	sts OCR3AL, r16
	clr r16
	sts TCCR3A, r16
	ldi r16, (1 << WGM32) | (1 << CS32) | (1 << CS30)
	sts TCCR3B, r16
	; Notice that the code for enabling the Timer 3
	; interrupt is missing at this point.

	; Timer 4 is for updating the contents to be displayed
	; on the top line of the LCD.
	ldi r17, high(TOP4)
	ldi r16, low(TOP4)
	sts OCR4AH, r17
	sts OCR4AL, r16
	clr r16
	sts TCCR4A, r16
	ldi r16, (1 << WGM42) | (1 << CS42) | (1 << CS40)
	sts TCCR4B, r16
	ldi r16, (1 << OCIE4A)
	sts TIMSK4, r16

	sei

; =============================================
; ====    END OF "DO NOT TOUCH" SECTION    ====
; =============================================

; ****************************************************
; **** BEGINNING OF SECOND "STUDENT CODE" SECTION ****
; ****************************************************

start:
	; push stack
	push r24
	push r25

	ldi r24, 0
	ldi r25, 0
	sts BUTTON_IS_PRESSED, r24 ; initialize BUTTON_IS_PRESSED to 0
	sts CURRENT_CHARSET_INDEX, r25 ; initialize CURRENT_CHARSET_INDEX to 0

	; pop stack
	pop r25
	pop r24

	rjmp timer3
stop:
	rjmp stop

timer1:
	cli
	; push stack
	push r16
	push DATAL
	push DATAH
	push BOUNDARY_L
	push BOUNDARY_H
	push r24
	push r23

check_button:
	; start a2d
	lds	r16, ADCSRA_BTN	

	; bit 6 =1 ADSC (ADC Start Conversion bit), remain 1 if conversion not done
	; ADSC changed to 0 if conversion is done
	ori r16, 0x40 ; 0x40 = 0b01000000
	sts	ADCSRA_BTN, r16

	; wait for it to complete, check for bit 6, the ADSC bit
wait:	
	
	lds r16, ADCSRA_BTN
	andi r16, 0x40
	brne wait

	; read the value, use XH:XL to store the 10-bit result
	lds DATAL, ADCL_BTN
	lds DATAH, ADCH_BTN

	; check if right button was pressed
right:
	ldi r16, low(50)
	mov BOUNDARY_L, r16
	ldi r16, high(50) 
	mov BOUNDARY_H, r16 ; set boundary for ADC value
	cp DATAL, BOUNDARY_L
	cpc DATAH, BOUNDARY_H ; check if ADC value within bounds
	brsh up ; if the ADC value is higher than the boundary, check other buttons

	; right button was pressed
	ldi r23,'R'
	ldi r24, 1
	sts LAST_BUTTON_PRESSED, r23 ; load 'R' in LAST_BUTTON_PRESSED
	sts BUTTON_IS_PRESSED, r24 ; set BUTTON_IS_PRESSED
	rjmp skip
up:
	ldi r16, low(176);
	mov BOUNDARY_L, r16
	ldi r16, high(176)
	mov BOUNDARY_H, r16 ; set boundary for ADC value
	cp DATAL, BOUNDARY_L
	cpc DATAH, BOUNDARY_H ; check if ADC value within bounds
	brsh down ; if the ADC value is higher than the boundary, check other buttons

	; up button was pressed
	ldi r23,'U'
	ldi r24, 1
	sts LAST_BUTTON_PRESSED, r23 ; load 'U' in LAST_BUTTON_PRESSED
	sts BUTTON_IS_PRESSED, r24 ; set BUTTON_IS_PRESSED
	rjmp skip
down:
	ldi r16, low(352);
	mov BOUNDARY_L, r16
	ldi r16, high(352)
	mov BOUNDARY_H, r16 ; set boundary for ADC value
	cp DATAL, BOUNDARY_L
	cpc DATAH, BOUNDARY_H ; check if ADC value within bounds
	brsh left ; if the ADC value is higher than the boundary, check other buttons

	; down button was pressed
	ldi r23,'D'
	ldi r24, 1
	sts LAST_BUTTON_PRESSED, r23 ; load 'D' in LAST_BUTTON_PRESSED
	sts BUTTON_IS_PRESSED, r24 ; set BUTTON_IS_PRESSED
	rjmp skip
left:
	ldi r16, low(555);
	mov BOUNDARY_L, r16
	ldi r16, high(555)
	mov BOUNDARY_H, r16 ; set boundary for ADC value
	cp DATAL, BOUNDARY_L
	cpc DATAH, BOUNDARY_H ; check if ADC value within bounds
	brsh none ; if the ADC value is higher than the boundary, no button is pressed

	; left button was pressed
	ldi r23,'L' 
	ldi r24, 1 
	sts LAST_BUTTON_PRESSED, r23 ; load 'L' in LAST_BUTTON_PRESSED
	sts BUTTON_IS_PRESSED, r24 ; set BUTTON_IS_PRESSED
	rjmp skip
none:
	ldi r16, low(900);
	mov BOUNDARY_L, r16
	ldi r16, high(900)
	mov BOUNDARY_H, r16
	cp DATAL, BOUNDARY_L
	cpc DATAH, BOUNDARY_H
	rjmp skip

skip:
	;pop stack
	pop r23
	pop r24
	pop BOUNDARY_H
	pop BOUNDARY_L
	pop DATAH
	pop DATAL
	pop r16

	sei
	reti

timer3:
;
; Note: There is no "timer3" interrupt handler as you must use
; timer3 in a polling style (i.e. it is used to drive the refreshing
; of the LCD display, but LCD functions cannot be called/used from
; within an interrupt handler).

	in r18, TIFR3
	sbrs r18, OCF3A
	rjmp timer3

	ldi r18, 1<<OCF3A
	out TIFR3, temp

; check if button was pressed
	lds r19, BUTTON_IS_PRESSED
	cpi r19, 1
	breq is_pressed ; if pressed, branch to is_pressed

	; button is not pressed
	ldi r20, 1
	ldi r21, 15
	push r20 ;row
	push r21 ;column
	rcall lcd_gotoxy ; set location for character
	pop r21
	pop r20

	ldi r20, '-'
	push r20
	rcall lcd_putchar ; display '-' at set location
	pop r20

	rjmp timer3

; button is pressed
is_pressed:
ldi r20, 1
	ldi r21, 15
	push r20 ;row
	push r21 ;column
	rcall lcd_gotoxy ; set location for character
	pop r21
	pop r20

	ldi r20,'*'
	push r20
	rcall lcd_putchar ; display '*' at set location
	pop r20

	; set white space in row 1, columns 0, 1, 2, 3
	ldi r20, 1
	ldi r21, 3
	push r20 ;row
	push r21 ;column
	rcall lcd_gotoxy
	pop r21
	pop r20

	ldi r20, ' '
	push r20
	rcall lcd_putchar
	pop r20

	ldi r20, 1
	ldi r21, 2
	push r20 ;row
	push r21 ;column
	rcall lcd_gotoxy
	pop r21
	pop r20

	ldi r20, ' '
	push r20
	rcall lcd_putchar
	pop r20

	ldi r20, 1
	ldi r21, 1
	push r20 ;row
	push r21 ;column
	rcall lcd_gotoxy
	pop r21
	pop r20

	ldi r20, ' '
	push r20
	rcall lcd_putchar
	pop r20

	ldi r20, 1
	ldi r21, 0
	push r20 ;row
	push r21 ;column
	rcall lcd_gotoxy
	pop r21
	pop r20

	ldi r20, ' '
	push r20
	rcall lcd_putchar
	pop r20

; checking if right button was pressed
check_right:
	lds r19, LAST_BUTTON_PRESSED
	cpi r19, 'R'
	breq display_r ; branch to display_r if right button pressed

; checking if up button was pressed
check_up:
	lds r19, LAST_BUTTON_PRESSED
	cpi r19, 'U'
	breq display_u ; branch to display_u if up button pressed

; checking if down button was pressed
check_down:
	lds r19, LAST_BUTTON_PRESSED
	cpi r19, 'D'
	breq display_d ; branch to display_d if down button pressed

; checking if left button was pressed
check_left:
	lds r19, LAST_BUTTON_PRESSED
	cpi r19, 'L'
	breq display_l ; branch to display_l if left button pressed

	; no button was pressed, arrive here
	rjmp timer3

; runs if right button pressed
display_r:
	ldi r20, 1
	ldi r21, 3
	push r20 ;row
	push r21 ;column
	rcall lcd_gotoxy ; set location for 'R' to be displayed
	pop r21
	pop r20

	ldi r20,'R'
	push r20
	rcall lcd_putchar ; display 'R'
	pop r20

	ldi r24, 0
	sts BUTTON_IS_PRESSED, r24 ; reset BUTTON_IS_PRESSED to 0

	rjmp timer3

; runs if up button pressed
display_u:
	; display U
	ldi r20, 1
	ldi r21, 2
	push r20 ;row
	push r21 ;column
	rcall lcd_gotoxy ; set location for 'U' to be displayed
	pop r21
	pop r20

	ldi r20,'U'
	push r20
	rcall lcd_putchar ; display 'U'
	pop r20

	; display TOP_LINE_CONTENT
	ldi r20, 0
	ldi r21, 0
	push r20 ;row
	push r21 ;column
	rcall lcd_gotoxy ; set location for TOP_LINE_CONTENT
	pop r21
	pop r20

	lds r20, TOP_LINE_CONTENT 
	push r20
	rcall lcd_putchar ; display TOP_LINE_CONTENT
	pop r20

	ldi r24, 0
	sts BUTTON_IS_PRESSED, r24 ; reset BUTTON_IS_PRESSED to 0

	rjmp timer3

; runs if left button pressed
display_l:
	ldi r20, 1
	ldi r21, 0
	push r20 ;row
	push r21 ;column
	rcall lcd_gotoxy ; set location for 'L' to be displayed
	pop r21
	pop r20

	ldi r20,'L'
	push r20
	rcall lcd_putchar ; display 'L'
	pop r20

	ldi r24, 0
	sts BUTTON_IS_PRESSED, r24 ; reset BUTTON_IS_PRESSED to 0

	rjmp timer3

; runs if down button pressed
display_d:
	; display 'D'
	ldi r20, 1
	ldi r21, 1
	push r20 ;row
	push r21 ;column
	rcall lcd_gotoxy ; set location for 'D' to be displayed
	pop r21
	pop r20

	ldi r20,'D'
	push r20
	rcall lcd_putchar ; display 'D'
	pop r20

	; display TOP_LINE_CONTENT
	ldi r20, 0
	ldi r21, 0
	push r20 ;row
	push r21 ;column
	rcall lcd_gotoxy ; set location for TOP_LINE_CONTENT
	pop r21
	pop r20

	lds r20, TOP_LINE_CONTENT 
	push r20
	rcall lcd_putchar ; display TOP_LINE_CONTENT
	pop r20

	ldi r24, 0
	sts BUTTON_IS_PRESSED, r24 ; reset BUTTON_IS_PRESSED to 0

	rjmp timer3
	

timer4:
	cli
	; push stack
	push r19
	push r20
	push r21
	push r22
	push r23
	push ZL
	push ZH

	; set pointer to AVAIABLE_CHARSET
	ldi ZL, LOW(AVAILABLE_CHARSET * 2)
	ldi ZH, HIGH(AVAILABLE_CHARSET * 2)

	; check which button was last pressed
	lds r19, LAST_BUTTON_PRESSED

	cpi r19, 'U'
	breq pressed_up ; if up was pressed, branch to pressed_up

	cpi r19, 'D'
	breq pressed_down ; if down was pressed, branch to pressed_down

	; neither up or down were pressed
	rjmp end
	
; runs if up was pressed
pressed_up:
	lds r22, CURRENT_CHARSET_INDEX
	inc r22 ; increment CURRENT_CHARSET_INDEX

	; check if out of bounds
	add ZL, r22
	lpm r23, Z
	cpi r23, '_' 
	breq end ; if terminal character reached, exit

	; arrived here, not out of bounds
	sts CURRENT_CHARSET_INDEX, r22 ; update CURRENT_CHARSET_INDEX

	lpm r23, Z+CURRENT_CHARSET_INDEX
	sts TOP_LINE_CONTENT, r23 ; load pointer to new char in TOP_LINE_CONTENT

	rjmp end

; runs if down was pressed
pressed_down:
	lds r22, CURRENT_CHARSET_INDEX
	dec r22 ; decrement CURRENT_CHARSET_INDEX

	; check if out of bounds
	add ZL, r22
	lpm r23, Z
	cpi r23, '0'
	breq end ; if terminal character reached, exit

	; arrived here, not out of bounds
	sts CURRENT_CHARSET_INDEX, r22 ; update CURRENT_CHARSET_INDEX

	lpm r23, Z+CURRENT_CHARSET_INDEX
	sts TOP_LINE_CONTENT, r23 ; load pointer to new char in TOP_LINE_CONTENT

	rjmp end

end:
	; pop stack
	pop ZH
	pop ZL
	pop r23
	pop r22
	pop r21
	pop r20
	pop r19

	sei
	reti



; ****************************************************
; ******* END OF SECOND "STUDENT CODE" SECTION *******
; ****************************************************


; =============================================
; ==== BEGINNING OF "DO NOT TOUCH" SECTION ====
; =============================================

; r17:r16 -- word 1
; r19:r18 -- word 2
; word 1 < word 2? return -1 in r25
; word 1 > word 2? return 1 in r25
; word 1 == word 2? return 0 in r25
;
compare_words:
	; if high bytes are different, look at lower bytes
	cp r17, r19
	breq compare_words_lower_byte

	; since high bytes are different, use these to
	; determine result
	;
	; if C is set from previous cp, it means r17 < r19
	; 
	; preload r25 with 1 with the assume r17 > r19
	ldi r25, 1
	brcs compare_words_is_less_than
	rjmp compare_words_exit

compare_words_is_less_than:
	ldi r25, -1
	rjmp compare_words_exit

compare_words_lower_byte:
	clr r25
	cp r16, r18
	breq compare_words_exit

	ldi r25, 1
	brcs compare_words_is_less_than  ; re-use what we already wrote...

compare_words_exit:
	ret

.cseg
AVAILABLE_CHARSET: .db "0123456789abcdef_", 0


.dseg

BUTTON_IS_PRESSED: .byte 1			; updated by timer1 interrupt, used by LCD update loop
LAST_BUTTON_PRESSED: .byte 1        ; updated by timer1 interrupt, used by LCD update loop

TOP_LINE_CONTENT: .byte 16			; updated by timer4 interrupt, used by LCD update loop
CURRENT_CHARSET_INDEX: .byte 16		; updated by timer4 interrupt, used by LCD update loop
CURRENT_CHAR_INDEX: .byte 1			; ; updated by timer4 interrupt, used by LCD update loop


; =============================================
; ======= END OF "DO NOT TOUCH" SECTION =======
; =============================================


; ***************************************************
; **** BEGINNING OF THIRD "STUDENT CODE" SECTION ****
; ***************************************************

.dseg

; If you should need additional memory for storage of state,
; then place it within the section. However, the items here
; must not be simply a way to replace or ignore the memory
; locations provided up above.


; ***************************************************
; ******* END OF THIRD "STUDENT CODE" SECTION *******
; ***************************************************
