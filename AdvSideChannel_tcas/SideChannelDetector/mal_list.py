data_injection = [
'''@ chunk1
	ldr r10, =Cur_Vertical_Sep 
	mov r9, #768
	str r9, [r10]\n''',
'''@ chunk2
	ldr r10, =High_Confidence
	mov r9, #1
	str r9, [r10]\n''',
'''@chunk3
	ldr r10, =Two_of_Three_Reports_Valid
	mov r9, #0
	str r9, [r10]\n''',
'''@chunk4
	ldr r10, =Own_Tracked_Alt
	mov r9, #64
	str r9, [r10]\n''',
'''@chunk5
	ldr r10, =Own_Tracked_Alt_Rate
	mov r9, #0
	str r9, [r10]\n''',
'''@chunk6
	ldr r10, =Other_Tracked_Alt
	mov r9, #0
	str r9, [r10]\n''',
'''@chunk7
	ldr r10, =Alt_Layer_Value
	mov r9, #0
	str r9, [r10]\n''',
'''@chunk8
	ldr r10, =Up_Separation
	mov r9, #448
	str r9, [r10]\n''',
'''@chunk9
	ldr r10, =Down_Separation
	mov r9, #1024
	str r9, [r10]\n''',
'''@chunk10
	ldr r10, =Other_RAC
	mov r9, #0
	str r9, [r10]\n''',
'''@chunk11
	ldr r10, =Other_Capability
	mov r9, #2
	str r9, [r10]\n''',
'''@chunk12
	ldr r10, =Climb_Inhibit
	mov r9, #0
	str r9, [r10]\n'''
]

candidate_locations = list(range(638, 649)) + list(range(281, 402)) + list(range(63, 144)) + list(range(173, 255))
exclude = list(range(110, 112)) + list(range(137, 139)) + list(range(246, 248)) + list(range(315, 317)) + list(range(358, 360)) + list(range(397, 401)) 
locations = [l for l in candidate_locations if l not in exclude]
data_injection_locations = len(data_injection) * [locations]

control_parameter = [
'''@chunk1
	ldr r10, =OLEV
	mov r9, #100
	str r9, [r10]\n''',
'''@chunk2
	ldr r10, =MAXALTDIFF
	mov r9, #100
	str r9, [r10]\n''',
'''@chunk3
	ldr r10, =MINSEP
	mov r9, #100
	str r9, [r10]\n''',
'''@chunk4
	ldr r10, =NOZCROSS
	mov r9, #100
	str r9, [r10]\n'''
]

control_parameter_locations = len(control_parameter) * [locations]

overwrite_output = [
'''@chunk1
	ldr r10, =alt_sep_result
	mov r9, #100
	str r9, [r10]\n'''
]

overwrite_output_locations = len(overwrite_output) * [locations]

data_logging = [
'''@chunk1
	ldr r9, =0x20002f34
	ldr r10, [r9]
	ldr r11, =0x20000f00
	str r10, [r11]\n''',
'''@chunk2
	ldr r9, =0x20002f36
	ldr r10, [r9]
	ldr r11, =0x20000f02
	str r10, [r11]\n''',
]

data_logging_locations = len(data_logging) * [locations]

information_disclosure = [
'''@chunk1
	sub sp, #0x20
	add r9, sp, #8
	str r12, [r9, #0xc]
	str r1, [r9, #8]
	movs r10, #0x1388
	str r10, [r9]
	movs r10, #0x01
	strh r10, [r9, #6]
	movs r10, #0
	str r10, [r9, #0x14]''',
'''@chunk2
	ldr r10, [r9, #0xc]
	movs r11, #1
	strb r11, [r10, #0x68]
	ldr r10, [r9, #0xc]
	movs r11, #0
	str r11, [r10, #0x6c]
	ldr r10, [r9, #0xc]
	movs r11, #0x21
	strb r11, [r10, #0x69]''',
'''@chunk3
	ldr r10, [pc, #0x10]
	ldr r10, [r10]
	adds r11, r10, #1
	ldr r1, [pc, #0xc]
	str r11, [r1]
	mov r12, r10''',
'''@chunk4
	str r12, [r9, #0x14]
	ldr r10, [r9, #0xc]
	ldrh r11, [r9, #6]
	strh r11, [r10, #0x50]
	ldr r10, [r9, #0xc]
	ldrh r11, [r9, #6]
	strhr11, [r10, #0x52]''',
'''@chunk5
	ldr r10, [r9, #0xc]
	ldrh r10, [r10, #0x52]
	uxth r10, r10
	subs r10, #1
	uxth r11, r10''',
'''@chunk6
	ldr r10, [r9, #8]
	str r10, [r9, #0x10]
	ldr r10, [r9, #0x10]
	ldrh r11, [r10]
	ldr r10, [r9, #0xc]
	ldr r10, [r10]
	ubfx r11, r11, #0, #9
	uxth r11, r11
	strh r11, [r10, #0x28]
	ldr r10, [r9, #8]
	adds r10, #2
	str r10, [r9, #8]''',
'''@chunk7
	ldr r10, [r9, #8]
	adds r11, r10, #1
	str r11, [r9, #8]
	ldrb r11, [r10]
	ldr r10, [r9, #0xc]
	ldr r10, [r10]
	uxth r11, r11
	strh r11, [r10, #0x28]''',
'''@chunk8
	ldr r10, [r9, #0xc]
	movs r11, #0x20
	strb r11, [r10, #0x69]
	ldr r10, [r9, #0xc]
	movs r11, #0
	strb r11, [r10, #0x68]
	movs r10, #0''',
'''@chunk9
	movs r10, #3''',
]

information_disclosure_locations = len(information_disclosure) * [locations]