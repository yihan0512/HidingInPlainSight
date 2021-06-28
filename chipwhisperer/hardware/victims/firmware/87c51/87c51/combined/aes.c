// aes.c
// A very small AES-128 implementation
// Some things to note:
// - Almost everything needs to be done in place
// - Don't have enough space for the key schedule; need to generate it in place
// Credit to https://github.com/kokke/tiny-AES128-C for some details

#include <stdint.h>

#include "crypto.h"

// AES-128 constants
#define Nb 4
#define Nk 4
#define Nr 10
#define KEYLEN 16

const static uint8_t s_box[256] = 
{
	0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 
	0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
	0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 
	0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
	0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 
	0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
	0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 
	0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
	0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 
	0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
	0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 
	0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
	0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 
	0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
	0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 
	0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
	0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 
	0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
	0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 
	0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
	0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 
	0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
	0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 
	0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
	0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 
	0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
	0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 
	0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
	0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 
	0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
	0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 
	0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
};

const static uint8_t rcon[11] = 
{
	0x00,
	0x01,
	0x02,
	0x04,
	0x08,
	0x10,
	0x20, 
	0x40, 
	0x80, 
	0x1b, 
	0x36, 
};

// Helper functions
uint8_t xtime(uint8_t x)
{
	return ((x<<1) ^ (((x>>7) & 1) * 0x1b));
}

// Cipher functions
void add_round_key(uint8_t* state, uint8_t* w)
{
	uint8_t i;
	for(i = 0; i < KEYLEN; i++)
		state[i] ^= w[i];
}

void sub_bytes(uint8_t* state)
{
	uint8_t i;
	for(i = 0; i < KEYLEN; i++)
		state[i] = s_box[state[i]];
}

void shift_rows(uint8_t* state)
{
	uint8_t temp;
	temp = state[1];
	state[1] = state[5];
	state[5] = state[9];
	state[9] = state[13];
	state[13] = temp;
	
	temp = state[2];
	state[2] = state[10];
	state[10] = temp;
	
	temp = state[6];
	state[6] = state[14];
	state[14] = temp;
	
	temp = state[3];
	state[3]  = state[15];
	state[15] = state[11];
	state[11] = state[7];
	state[7]  = temp;
}

void mix_columns(uint8_t* state)
{
	uint8_t col;
	for(col = 0; col < 4; col++)
	{
		uint8_t Tmp, Tm, t;
		Tmp = state[4*col+0] ^ state[4*col+1] ^ state[4*col+2] ^ state[4*col+3];
		t  = state[4*col];
		Tm = state[4*col+0] ^ state[4*col+1]; Tm = xtime(Tm); state[4*col+0] ^= (Tm ^ Tmp);
		Tm = state[4*col+1] ^ state[4*col+2]; Tm = xtime(Tm); state[4*col+1] ^= (Tm ^ Tmp);
		Tm = state[4*col+2] ^ state[4*col+3]; Tm = xtime(Tm); state[4*col+2] ^= (Tm ^ Tmp);
		Tm = state[4*col+3] ^ t;              Tm = xtime(Tm); state[4*col+3] ^= (Tm ^ Tmp);
	}
}

void update_key(uint8_t* w, uint8_t round)
{
	uint8_t temp[4];
	uint8_t i;
	
	for(i = 0; i < 4; i++)
	{
		if(i == 0)
		{
			temp[0] = s_box[w[13]] ^ rcon[round];
			temp[1] = s_box[w[14]];
			temp[2] = s_box[w[15]];
			temp[3] = s_box[w[12]];
		}
		else
		{
			temp[0] = w[4*(i-1) + 0];
			temp[1] = w[4*(i-1) + 1];
			temp[2] = w[4*(i-1) + 2];
			temp[3] = w[4*(i-1) + 3];
		}
		
		w[4*i+0] ^= temp[0];
		w[4*i+1] ^= temp[1];
		w[4*i+2] ^= temp[2];
		w[4*i+3] ^= temp[3];
	}
}
	
void aes_encrypt(uint8_t* state, uint8_t* key)
{
	unsigned char i;
	uint8_t w[KEYLEN];
	for(i = 0; i < KEYLEN; i++)
		w[i] = key[i];

	add_round_key(state, w);
	for(i = 1; i < Nr; i++)
	{
		sub_bytes(state);
		shift_rows(state);
		mix_columns(state);
		update_key(w, i);	
		add_round_key(state, w);
	}
	
	sub_bytes(state);
	shift_rows(state);
	update_key(w, i);
	add_round_key(state, w);
}

void aes_auth(uint8_t* v, uint8_t* k, uint8_t* e)
{
	uint8_t res = 0x10;
	uint8_t i;
	aes_encrypt(v, k);
	for(i = 0; i < 16; i++)
	{
		if(v[i] != e[i])
			res = 0;
		v[i] = 0;
	}
	v[0] = res;
}