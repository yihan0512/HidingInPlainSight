// aes_crypto.h

#ifndef AES_CRYPTO_H
#define AES_CRYPTO_H

#include <stdint.h>

// Encrypt (or decrypt) the state matrix with AES-128
// Encryption is done in-place and result is stored in state[]
void aes_encrypt(uint8_t* state, uint8_t* key);

#endif // AES_CRYPTO_H