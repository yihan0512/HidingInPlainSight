/* This code was published at http://cs.ucsb.edu/~koc/cs178/projects/JT/avr_aes.html .
 * 
 * It is a straight-forward AES implementation. It was selected basically because it's one of the
 * first three Google hits for 'AVR AES'. It's thus very likely someone looking for a simple
 * implementation would find this, so I've selected this as a reasonable choice to attack
 *
 * The code as written was vulnerable to timing attacks (as mentioned in the comments). It's been
 * fixed to add the NOP to avoid this.
 */
 

/*
 * AES
 */
#include "aes.h"

/* Sbox Lookup Table */
const byte sbox[256] = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
    0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
    0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
    0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
    0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
    0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
    0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
    0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
    0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
    0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
    0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
    0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
    0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
    0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
    0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
    0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
    0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
};

byte rcon [] = {
0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab
};

byte state[16];
byte key[16];

byte * aes(byte *in, byte *skey)
{
	int i;

	for(i=0; i < 16; i++)
	{
		state[i] = in[i];
		key[i] = skey[i];
	}
	addRoundKey();

	for(i = 0; i < 9; i++)
	{
 		subBytes();
		shiftRows();
		mixColumns();
		computeKey(rcon[i]);
		addRoundKey();
	}

	subBytes();
	shiftRows();
	computeKey(rcon[i]);
	addRoundKey();

	return state;
}

void addRoundKey(void)
{
	int i;

	for(i=0; i < 16; i++)
	{
		state[i] ^= key[i];
	}
}

/* subBytes
 * Table Lookup
 */
void subBytes(void)
{
	int i;

	for(i = 0; i < 16; i++)
	{
		state[i] = sbox[ state[i] ];
	}
}

/* shiftRows                Before         After
 * Row 1: No change        0 4  8 12      0  4  8 12    
 * Row 2: Left Shift by 1  1 5  9 13  =>  5  9 13  1    
 * Row 3: Left Shift by 2  2 6 10 14     10 14  2  6   
 * Row 4: Left Shift by 3  3 7 11 15     15 3   7 11  
 */
void shiftRows(void)
{
	byte temp;

	//Row 2
	temp = state[1]; state[1] = state[5]; state[5] = state[9];
    state[9] = state[13]; state[13] = temp;
	//Row 3
	temp = state[10]; state[10] = state[2]; state[2] = temp;
	temp = state[14]; state[14] = state[6]; state[6] = temp;
	//Row 4
	temp = state[3]; state[3] = state[15]; state[15] = state[11]; 
    state[11] = state[7]; state[7] = temp;
}

/* MixColumns Shortcut 
 * **WARNING** For DPA to work must be constant timing. The following was tested on WinAVR
 * compiler with -Os optimization. Do NOT change optimization level or this will fail. Check
 * listing output if unsure.
 */
byte xtime(byte x)
{
	byte rv = (x<<1);
	if (x & 0x80) {
		rv ^= 0x1b;
	} else {
		asm volatile("nop\n\t"
             "nop\n\t"
             "nop\n\t"::);
	}
	return rv;
}

/* Mix Columns */
void mixColumns(void)
{
	byte i, a, b, c, d, e;
	
	/* Process a column at a time */
	for(i = 0; i < 16; i+=4)
	{
		a = state[i]; b = state[i+1]; c = state[i+2]; d = state[i+3];
		e = a ^ b ^ c ^ d;
		state[i]   ^= e ^ xtime(a^b);
		state[i+1] ^= e ^ xtime(b^c);
		state[i+2] ^= e ^ xtime(c^d);
		state[i+3] ^= e ^ xtime(d^a);
	}
}
/* Compute a round of the key
 * 0 4  8 12
 * 1 5  9 13
 * 2 6 10 14
 * 3 7 11 15
 */
void computeKey(byte rcon)
{
	byte buf0, buf1, buf2, buf3;
	buf0 = sbox[ key[13] ];
	buf1 = sbox[ key[14] ];
	buf2 = sbox[ key[15] ];
	buf3 = sbox[ key[12] ];

	key[0] ^= buf0 ^ rcon;
    key[1] ^= buf1;
    key[2] ^= buf2;
    key[3] ^= buf3;

	key[4] ^= key[0];
	key[5] ^= key[1];
	key[6] ^= key[2];
	key[7] ^= key[3];

	key[8]  ^= key[4];
	key[9]  ^= key[5];
	key[10] ^= key[6];
	key[11] ^= key[7];

	key[12] ^= key[8];
	key[13] ^= key[9];
	key[14] ^= key[10];
	key[15] ^= key[11];
}
