/* cast6-sbox.c */
/*
    This file is part of the AVR-Crypto-Lib.
    Copyright (C) 2008  Daniel Otte (daniel.otte@rub.de)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
/* 
 * File:	cast6-sbox.c
 * Author:	Daniel Otte
 * Date: 	26.07.2006
 * License: GPL
 * Description: sboxes for CAST6 (aka CAST-256) cipher algorithm as described in RFC 2612.
 * 
 */
 
#include <avr/pgmspace.h>
#include <stdint.h>

#ifndef BIG_ENDIAN

const uint32_t s1[] PROGMEM = {
0x30fb40d4UL, 0x9fa0ff0bUL, 0x6beccd2fUL, 0x3f258c7aUL, 0x1e213f2fUL, 0x9c004dd3UL, 0x6003e540UL, 0xcf9fc949UL,
0xbfd4af27UL, 0x88bbbdb5UL, 0xe2034090UL, 0x98d09675UL, 0x6e63a0e0UL, 0x15c361d2UL, 0xc2e7661dUL, 0x22d4ff8eUL,
0x28683b6fUL, 0xc07fd059UL, 0xff2379c8UL, 0x775f50e2UL, 0x43c340d3UL, 0xdf2f8656UL, 0x887ca41aUL, 0xa2d2bd2dUL,
0xa1c9e0d6UL, 0x346c4819UL, 0x61b76d87UL, 0x22540f2fUL, 0x2abe32e1UL, 0xaa54166bUL, 0x22568e3aUL, 0xa2d341d0UL,
0x66db40c8UL, 0xa784392fUL, 0x004dff2fUL, 0x2db9d2deUL, 0x97943facUL, 0x4a97c1d8UL, 0x527644b7UL, 0xb5f437a7UL,
0xb82cbaefUL, 0xd751d159UL, 0x6ff7f0edUL, 0x5a097a1fUL, 0x827b68d0UL, 0x90ecf52eUL, 0x22b0c054UL, 0xbc8e5935UL,
0x4b6d2f7fUL, 0x50bb64a2UL, 0xd2664910UL, 0xbee5812dUL, 0xb7332290UL, 0xe93b159fUL, 0xb48ee411UL, 0x4bff345dUL,
0xfd45c240UL, 0xad31973fUL, 0xc4f6d02eUL, 0x55fc8165UL, 0xd5b1caadUL, 0xa1ac2daeUL, 0xa2d4b76dUL, 0xc19b0c50UL,
0x882240f2UL, 0x0c6e4f38UL, 0xa4e4bfd7UL, 0x4f5ba272UL, 0x564c1d2fUL, 0xc59c5319UL, 0xb949e354UL, 0xb04669feUL,
0xb1b6ab8aUL, 0xc71358ddUL, 0x6385c545UL, 0x110f935dUL, 0x57538ad5UL, 0x6a390493UL, 0xe63d37e0UL, 0x2a54f6b3UL,
0x3a787d5fUL, 0x6276a0b5UL, 0x19a6fcdfUL, 0x7a42206aUL, 0x29f9d4d5UL, 0xf61b1891UL, 0xbb72275eUL, 0xaa508167UL,
0x38901091UL, 0xc6b505ebUL, 0x84c7cb8cUL, 0x2ad75a0fUL, 0x874a1427UL, 0xa2d1936bUL, 0x2ad286afUL, 0xaa56d291UL,
0xd7894360UL, 0x425c750dUL, 0x93b39e26UL, 0x187184c9UL, 0x6c00b32dUL, 0x73e2bb14UL, 0xa0bebc3cUL, 0x54623779UL,
0x64459eabUL, 0x3f328b82UL, 0x7718cf82UL, 0x59a2cea6UL, 0x04ee002eUL, 0x89fe78e6UL, 0x3fab0950UL, 0x325ff6c2UL,
0x81383f05UL, 0x6963c5c8UL, 0x76cb5ad6UL, 0xd49974c9UL, 0xca180dcfUL, 0x380782d5UL, 0xc7fa5cf6UL, 0x8ac31511UL,
0x35e79e13UL, 0x47da91d0UL, 0xf40f9086UL, 0xa7e2419eUL, 0x31366241UL, 0x051ef495UL, 0xaa573b04UL, 0x4a805d8dUL,
0x548300d0UL, 0x00322a3cUL, 0xbf64cddfUL, 0xba57a68eUL, 0x75c6372bUL, 0x50afd341UL, 0xa7c13275UL, 0x915a0bf5UL,
0x6b54bfabUL, 0x2b0b1426UL, 0xab4cc9d7UL, 0x449ccd82UL, 0xf7fbf265UL, 0xab85c5f3UL, 0x1b55db94UL, 0xaad4e324UL,
0xcfa4bd3fUL, 0x2deaa3e2UL, 0x9e204d02UL, 0xc8bd25acUL, 0xeadf55b3UL, 0xd5bd9e98UL, 0xe31231b2UL, 0x2ad5ad6cUL,
0x954329deUL, 0xadbe4528UL, 0xd8710f69UL, 0xaa51c90fUL, 0xaa786bf6UL, 0x22513f1eUL, 0xaa51a79bUL, 0x2ad344ccUL,
0x7b5a41f0UL, 0xd37cfbadUL, 0x1b069505UL, 0x41ece491UL, 0xb4c332e6UL, 0x032268d4UL, 0xc9600accUL, 0xce387e6dUL,
0xbf6bb16cUL, 0x6a70fb78UL, 0x0d03d9c9UL, 0xd4df39deUL, 0xe01063daUL, 0x4736f464UL, 0x5ad328d8UL, 0xb347cc96UL,
0x75bb0fc3UL, 0x98511bfbUL, 0x4ffbcc35UL, 0xb58bcf6aUL, 0xe11f0abcUL, 0xbfc5fe4aUL, 0xa70aec10UL, 0xac39570aUL,
0x3f04442fUL, 0x6188b153UL, 0xe0397a2eUL, 0x5727cb79UL, 0x9ceb418fUL, 0x1cacd68dUL, 0x2ad37c96UL, 0x0175cb9dUL,
0xc69dff09UL, 0xc75b65f0UL, 0xd9db40d8UL, 0xec0e7779UL, 0x4744ead4UL, 0xb11c3274UL, 0xdd24cb9eUL, 0x7e1c54bdUL,
0xf01144f9UL, 0xd2240eb1UL, 0x9675b3fdUL, 0xa3ac3755UL, 0xd47c27afUL, 0x51c85f4dUL, 0x56907596UL, 0xa5bb15e6UL,
0x580304f0UL, 0xca042cf1UL, 0x011a37eaUL, 0x8dbfaadbUL, 0x35ba3e4aUL, 0x3526ffa0UL, 0xc37b4d09UL, 0xbc306ed9UL,
0x98a52666UL, 0x5648f725UL, 0xff5e569dUL, 0x0ced63d0UL, 0x7c63b2cfUL, 0x700b45e1UL, 0xd5ea50f1UL, 0x85a92872UL,
0xaf1fbda7UL, 0xd4234870UL, 0xa7870bf3UL, 0x2d3b4d79UL, 0x42e04198UL, 0x0cd0ede7UL, 0x26470db8UL, 0xf881814cUL,
0x474d6ad7UL, 0x7c0c5e5cUL, 0xd1231959UL, 0x381b7298UL, 0xf5d2f4dbUL, 0xab838653UL, 0x6e2f1e23UL, 0x83719c9eUL,
0xbd91e046UL, 0x9a56456eUL, 0xdc39200cUL, 0x20c8c571UL, 0x962bda1cUL, 0xe1e696ffUL, 0xb141ab08UL, 0x7cca89b9UL,
0x1a69e783UL, 0x02cc4843UL, 0xa2f7c579UL, 0x429ef47dUL, 0x427b169cUL, 0x5ac9f049UL, 0xdd8f0f00UL, 0x5c8165bfUL};

const uint32_t s2[] PROGMEM = {
0x1f201094UL, 0xef0ba75bUL, 0x69e3cf7eUL, 0x393f4380UL, 0xfe61cf7aUL, 0xeec5207aUL, 0x55889c94UL, 0x72fc0651UL,
0xada7ef79UL, 0x4e1d7235UL, 0xd55a63ceUL, 0xde0436baUL, 0x99c430efUL, 0x5f0c0794UL, 0x18dcdb7dUL, 0xa1d6eff3UL,
0xa0b52f7bUL, 0x59e83605UL, 0xee15b094UL, 0xe9ffd909UL, 0xdc440086UL, 0xef944459UL, 0xba83ccb3UL, 0xe0c3cdfbUL,
0xd1da4181UL, 0x3b092ab1UL, 0xf997f1c1UL, 0xa5e6cf7bUL, 0x01420ddbUL, 0xe4e7ef5bUL, 0x25a1ff41UL, 0xe180f806UL,
0x1fc41080UL, 0x179bee7aUL, 0xd37ac6a9UL, 0xfe5830a4UL, 0x98de8b7fUL, 0x77e83f4eUL, 0x79929269UL, 0x24fa9f7bUL,
0xe113c85bUL, 0xacc40083UL, 0xd7503525UL, 0xf7ea615fUL, 0x62143154UL, 0x0d554b63UL, 0x5d681121UL, 0xc866c359UL,
0x3d63cf73UL, 0xcee234c0UL, 0xd4d87e87UL, 0x5c672b21UL, 0x071f6181UL, 0x39f7627fUL, 0x361e3084UL, 0xe4eb573bUL,
0x602f64a4UL, 0xd63acd9cUL, 0x1bbc4635UL, 0x9e81032dUL, 0x2701f50cUL, 0x99847ab4UL, 0xa0e3df79UL, 0xba6cf38cUL,
0x10843094UL, 0x2537a95eUL, 0xf46f6ffeUL, 0xa1ff3b1fUL, 0x208cfb6aUL, 0x8f458c74UL, 0xd9e0a227UL, 0x4ec73a34UL,
0xfc884f69UL, 0x3e4de8dfUL, 0xef0e0088UL, 0x3559648dUL, 0x8a45388cUL, 0x1d804366UL, 0x721d9bfdUL, 0xa58684bbUL,
0xe8256333UL, 0x844e8212UL, 0x128d8098UL, 0xfed33fb4UL, 0xce280ae1UL, 0x27e19ba5UL, 0xd5a6c252UL, 0xe49754bdUL,
0xc5d655ddUL, 0xeb667064UL, 0x77840b4dUL, 0xa1b6a801UL, 0x84db26a9UL, 0xe0b56714UL, 0x21f043b7UL, 0xe5d05860UL,
0x54f03084UL, 0x066ff472UL, 0xa31aa153UL, 0xdadc4755UL, 0xb5625dbfUL, 0x68561be6UL, 0x83ca6b94UL, 0x2d6ed23bUL,
0xeccf01dbUL, 0xa6d3d0baUL, 0xb6803d5cUL, 0xaf77a709UL, 0x33b4a34cUL, 0x397bc8d6UL, 0x5ee22b95UL, 0x5f0e5304UL,
0x81ed6f61UL, 0x20e74364UL, 0xb45e1378UL, 0xde18639bUL, 0x881ca122UL, 0xb96726d1UL, 0x8049a7e8UL, 0x22b7da7bUL,
0x5e552d25UL, 0x5272d237UL, 0x79d2951cUL, 0xc60d894cUL, 0x488cb402UL, 0x1ba4fe5bUL, 0xa4b09f6bUL, 0x1ca815cfUL,
0xa20c3005UL, 0x8871df63UL, 0xb9de2fcbUL, 0x0cc6c9e9UL, 0x0beeff53UL, 0xe3214517UL, 0xb4542835UL, 0x9f63293cUL,
0xee41e729UL, 0x6e1d2d7cUL, 0x50045286UL, 0x1e6685f3UL, 0xf33401c6UL, 0x30a22c95UL, 0x31a70850UL, 0x60930f13UL,
0x73f98417UL, 0xa1269859UL, 0xec645c44UL, 0x52c877a9UL, 0xcdff33a6UL, 0xa02b1741UL, 0x7cbad9a2UL, 0x2180036fUL,
0x50d99c08UL, 0xcb3f4861UL, 0xc26bd765UL, 0x64a3f6abUL, 0x80342676UL, 0x25a75e7bUL, 0xe4e6d1fcUL, 0x20c710e6UL,
0xcdf0b680UL, 0x17844d3bUL, 0x31eef84dUL, 0x7e0824e4UL, 0x2ccb49ebUL, 0x846a3baeUL, 0x8ff77888UL, 0xee5d60f6UL,
0x7af75673UL, 0x2fdd5cdbUL, 0xa11631c1UL, 0x30f66f43UL, 0xb3faec54UL, 0x157fd7faUL, 0xef8579ccUL, 0xd152de58UL,
0xdb2ffd5eUL, 0x8f32ce19UL, 0x306af97aUL, 0x02f03ef8UL, 0x99319ad5UL, 0xc242fa0fUL, 0xa7e3ebb0UL, 0xc68e4906UL,
0xb8da230cUL, 0x80823028UL, 0xdcdef3c8UL, 0xd35fb171UL, 0x088a1bc8UL, 0xbec0c560UL, 0x61a3c9e8UL, 0xbca8f54dUL,
0xc72feffaUL, 0x22822e99UL, 0x82c570b4UL, 0xd8d94e89UL, 0x8b1c34bcUL, 0x301e16e6UL, 0x273be979UL, 0xb0ffeaa6UL,
0x61d9b8c6UL, 0x00b24869UL, 0xb7ffce3fUL, 0x08dc283bUL, 0x43daf65aUL, 0xf7e19798UL, 0x7619b72fUL, 0x8f1c9ba4UL,
0xdc8637a0UL, 0x16a7d3b1UL, 0x9fc393b7UL, 0xa7136eebUL, 0xc6bcc63eUL, 0x1a513742UL, 0xef6828bcUL, 0x520365d6UL,
0x2d6a77abUL, 0x3527ed4bUL, 0x821fd216UL, 0x095c6e2eUL, 0xdb92f2fbUL, 0x5eea29cbUL, 0x145892f5UL, 0x91584f7fUL,
0x5483697bUL, 0x2667a8ccUL, 0x85196048UL, 0x8c4baceaUL, 0x833860d4UL, 0x0d23e0f9UL, 0x6c387e8aUL, 0x0ae6d249UL,
0xb284600cUL, 0xd835731dUL, 0xdcb1c647UL, 0xac4c56eaUL, 0x3ebd81b3UL, 0x230eabb0UL, 0x6438bc87UL, 0xf0b5b1faUL,
0x8f5ea2b3UL, 0xfc184642UL, 0x0a036b7aUL, 0x4fb089bdUL, 0x649da589UL, 0xa345415eUL, 0x5c038323UL, 0x3e5d3bb9UL,
0x43d79572UL, 0x7e6dd07cUL, 0x06dfdf1eUL, 0x6c6cc4efUL, 0x7160a539UL, 0x73bfbe70UL, 0x83877605UL, 0x4523ecf1UL};

const uint32_t s3[] PROGMEM = {
0x8defc240UL, 0x25fa5d9fUL, 0xeb903dbfUL, 0xe810c907UL, 0x47607fffUL, 0x369fe44bUL, 0x8c1fc644UL, 0xaececa90UL,
0xbeb1f9bfUL, 0xeefbcaeaUL, 0xe8cf1950UL, 0x51df07aeUL, 0x920e8806UL, 0xf0ad0548UL, 0xe13c8d83UL, 0x927010d5UL,
0x11107d9fUL, 0x07647db9UL, 0xb2e3e4d4UL, 0x3d4f285eUL, 0xb9afa820UL, 0xfade82e0UL, 0xa067268bUL, 0x8272792eUL,
0x553fb2c0UL, 0x489ae22bUL, 0xd4ef9794UL, 0x125e3fbcUL, 0x21fffceeUL, 0x825b1bfdUL, 0x9255c5edUL, 0x1257a240UL,
0x4e1a8302UL, 0xbae07fffUL, 0x528246e7UL, 0x8e57140eUL, 0x3373f7bfUL, 0x8c9f8188UL, 0xa6fc4ee8UL, 0xc982b5a5UL,
0xa8c01db7UL, 0x579fc264UL, 0x67094f31UL, 0xf2bd3f5fUL, 0x40fff7c1UL, 0x1fb78dfcUL, 0x8e6bd2c1UL, 0x437be59bUL,
0x99b03dbfUL, 0xb5dbc64bUL, 0x638dc0e6UL, 0x55819d99UL, 0xa197c81cUL, 0x4a012d6eUL, 0xc5884a28UL, 0xccc36f71UL,
0xb843c213UL, 0x6c0743f1UL, 0x8309893cUL, 0x0feddd5fUL, 0x2f7fe850UL, 0xd7c07f7eUL, 0x02507fbfUL, 0x5afb9a04UL,
0xa747d2d0UL, 0x1651192eUL, 0xaf70bf3eUL, 0x58c31380UL, 0x5f98302eUL, 0x727cc3c4UL, 0x0a0fb402UL, 0x0f7fef82UL,
0x8c96fdadUL, 0x5d2c2aaeUL, 0x8ee99a49UL, 0x50da88b8UL, 0x8427f4a0UL, 0x1eac5790UL, 0x796fb449UL, 0x8252dc15UL,
0xefbd7d9bUL, 0xa672597dUL, 0xada840d8UL, 0x45f54504UL, 0xfa5d7403UL, 0xe83ec305UL, 0x4f91751aUL, 0x925669c2UL,
0x23efe941UL, 0xa903f12eUL, 0x60270df2UL, 0x0276e4b6UL, 0x94fd6574UL, 0x927985b2UL, 0x8276dbcbUL, 0x02778176UL,
0xf8af918dUL, 0x4e48f79eUL, 0x8f616ddfUL, 0xe29d840eUL, 0x842f7d83UL, 0x340ce5c8UL, 0x96bbb682UL, 0x93b4b148UL,
0xef303cabUL, 0x984faf28UL, 0x779faf9bUL, 0x92dc560dUL, 0x224d1e20UL, 0x8437aa88UL, 0x7d29dc96UL, 0x2756d3dcUL,
0x8b907ceeUL, 0xb51fd240UL, 0xe7c07ce3UL, 0xe566b4a1UL, 0xc3e9615eUL, 0x3cf8209dUL, 0x6094d1e3UL, 0xcd9ca341UL,
0x5c76460eUL, 0x00ea983bUL, 0xd4d67881UL, 0xfd47572cUL, 0xf76cedd9UL, 0xbda8229cUL, 0x127dadaaUL, 0x438a074eUL,
0x1f97c090UL, 0x081bdb8aUL, 0x93a07ebeUL, 0xb938ca15UL, 0x97b03cffUL, 0x3dc2c0f8UL, 0x8d1ab2ecUL, 0x64380e51UL,
0x68cc7bfbUL, 0xd90f2788UL, 0x12490181UL, 0x5de5ffd4UL, 0xdd7ef86aUL, 0x76a2e214UL, 0xb9a40368UL, 0x925d958fUL,
0x4b39fffaUL, 0xba39aee9UL, 0xa4ffd30bUL, 0xfaf7933bUL, 0x6d498623UL, 0x193cbcfaUL, 0x27627545UL, 0x825cf47aUL,
0x61bd8ba0UL, 0xd11e42d1UL, 0xcead04f4UL, 0x127ea392UL, 0x10428db7UL, 0x8272a972UL, 0x9270c4a8UL, 0x127de50bUL,
0x285ba1c8UL, 0x3c62f44fUL, 0x35c0eaa5UL, 0xe805d231UL, 0x428929fbUL, 0xb4fcdf82UL, 0x4fb66a53UL, 0x0e7dc15bUL,
0x1f081fabUL, 0x108618aeUL, 0xfcfd086dUL, 0xf9ff2889UL, 0x694bcc11UL, 0x236a5caeUL, 0x12deca4dUL, 0x2c3f8cc5UL,
0xd2d02dfeUL, 0xf8ef5896UL, 0xe4cf52daUL, 0x95155b67UL, 0x494a488cUL, 0xb9b6a80cUL, 0x5c8f82bcUL, 0x89d36b45UL,
0x3a609437UL, 0xec00c9a9UL, 0x44715253UL, 0x0a874b49UL, 0xd773bc40UL, 0x7c34671cUL, 0x02717ef6UL, 0x4feb5536UL,
0xa2d02fffUL, 0xd2bf60c4UL, 0xd43f03c0UL, 0x50b4ef6dUL, 0x07478cd1UL, 0x006e1888UL, 0xa2e53f55UL, 0xb9e6d4bcUL,
0xa2048016UL, 0x97573833UL, 0xd7207d67UL, 0xde0f8f3dUL, 0x72f87b33UL, 0xabcc4f33UL, 0x7688c55dUL, 0x7b00a6b0UL,
0x947b0001UL, 0x570075d2UL, 0xf9bb88f8UL, 0x8942019eUL, 0x4264a5ffUL, 0x856302e0UL, 0x72dbd92bUL, 0xee971b69UL,
0x6ea22fdeUL, 0x5f08ae2bUL, 0xaf7a616dUL, 0xe5c98767UL, 0xcf1febd2UL, 0x61efc8c2UL, 0xf1ac2571UL, 0xcc8239c2UL,
0x67214cb8UL, 0xb1e583d1UL, 0xb7dc3e62UL, 0x7f10bdceUL, 0xf90a5c38UL, 0x0ff0443dUL, 0x606e6dc6UL, 0x60543a49UL,
0x5727c148UL, 0x2be98a1dUL, 0x8ab41738UL, 0x20e1be24UL, 0xaf96da0fUL, 0x68458425UL, 0x99833be5UL, 0x600d457dUL,
0x282f9350UL, 0x8334b362UL, 0xd91d1120UL, 0x2b6d8da0UL, 0x642b1e31UL, 0x9c305a00UL, 0x52bce688UL, 0x1b03588aUL,
0xf7baefd5UL, 0x4142ed9cUL, 0xa4315c11UL, 0x83323ec5UL, 0xdfef4636UL, 0xa133c501UL, 0xe9d3531cUL, 0xee353783UL};

const uint32_t s4[] PROGMEM = {
0x9db30420UL, 0x1fb6e9deUL, 0xa7be7befUL, 0xd273a298UL, 0x4a4f7bdbUL, 0x64ad8c57UL, 0x85510443UL, 0xfa020ed1UL,
0x7e287affUL, 0xe60fb663UL, 0x095f35a1UL, 0x79ebf120UL, 0xfd059d43UL, 0x6497b7b1UL, 0xf3641f63UL, 0x241e4adfUL,
0x28147f5fUL, 0x4fa2b8cdUL, 0xc9430040UL, 0x0cc32220UL, 0xfdd30b30UL, 0xc0a5374fUL, 0x1d2d00d9UL, 0x24147b15UL,
0xee4d111aUL, 0x0fca5167UL, 0x71ff904cUL, 0x2d195ffeUL, 0x1a05645fUL, 0x0c13fefeUL, 0x081b08caUL, 0x05170121UL,
0x80530100UL, 0xe83e5efeUL, 0xac9af4f8UL, 0x7fe72701UL, 0xd2b8ee5fUL, 0x06df4261UL, 0xbb9e9b8aUL, 0x7293ea25UL,
0xce84ffdfUL, 0xf5718801UL, 0x3dd64b04UL, 0xa26f263bUL, 0x7ed48400UL, 0x547eebe6UL, 0x446d4ca0UL, 0x6cf3d6f5UL,
0x2649abdfUL, 0xaea0c7f5UL, 0x36338cc1UL, 0x503f7e93UL, 0xd3772061UL, 0x11b638e1UL, 0x72500e03UL, 0xf80eb2bbUL,
0xabe0502eUL, 0xec8d77deUL, 0x57971e81UL, 0xe14f6746UL, 0xc9335400UL, 0x6920318fUL, 0x081dbb99UL, 0xffc304a5UL,
0x4d351805UL, 0x7f3d5ce3UL, 0xa6c866c6UL, 0x5d5bcca9UL, 0xdaec6feaUL, 0x9f926f91UL, 0x9f46222fUL, 0x3991467dUL,
0xa5bf6d8eUL, 0x1143c44fUL, 0x43958302UL, 0xd0214eebUL, 0x022083b8UL, 0x3fb6180cUL, 0x18f8931eUL, 0x281658e6UL,
0x26486e3eUL, 0x8bd78a70UL, 0x7477e4c1UL, 0xb506e07cUL, 0xf32d0a25UL, 0x79098b02UL, 0xe4eabb81UL, 0x28123b23UL,
0x69dead38UL, 0x1574ca16UL, 0xdf871b62UL, 0x211c40b7UL, 0xa51a9ef9UL, 0x0014377bUL, 0x041e8ac8UL, 0x09114003UL,
0xbd59e4d2UL, 0xe3d156d5UL, 0x4fe876d5UL, 0x2f91a340UL, 0x557be8deUL, 0x00eae4a7UL, 0x0ce5c2ecUL, 0x4db4bba6UL,
0xe756bdffUL, 0xdd3369acUL, 0xec17b035UL, 0x06572327UL, 0x99afc8b0UL, 0x56c8c391UL, 0x6b65811cUL, 0x5e146119UL,
0x6e85cb75UL, 0xbe07c002UL, 0xc2325577UL, 0x893ff4ecUL, 0x5bbfc92dUL, 0xd0ec3b25UL, 0xb7801ab7UL, 0x8d6d3b24UL,
0x20c763efUL, 0xc366a5fcUL, 0x9c382880UL, 0x0ace3205UL, 0xaac9548aUL, 0xeca1d7c7UL, 0x041afa32UL, 0x1d16625aUL,
0x6701902cUL, 0x9b757a54UL, 0x31d477f7UL, 0x9126b031UL, 0x36cc6fdbUL, 0xc70b8b46UL, 0xd9e66a48UL, 0x56e55a79UL,
0x026a4cebUL, 0x52437effUL, 0x2f8f76b4UL, 0x0df980a5UL, 0x8674cde3UL, 0xedda04ebUL, 0x17a9be04UL, 0x2c18f4dfUL,
0xb7747f9dUL, 0xab2af7b4UL, 0xefc34d20UL, 0x2e096b7cUL, 0x1741a254UL, 0xe5b6a035UL, 0x213d42f6UL, 0x2c1c7c26UL,
0x61c2f50fUL, 0x6552daf9UL, 0xd2c231f8UL, 0x25130f69UL, 0xd8167fa2UL, 0x0418f2c8UL, 0x001a96a6UL, 0x0d1526abUL,
0x63315c21UL, 0x5e0a72ecUL, 0x49bafefdUL, 0x187908d9UL, 0x8d0dbd86UL, 0x311170a7UL, 0x3e9b640cUL, 0xcc3e10d7UL,
0xd5cad3b6UL, 0x0caec388UL, 0xf73001e1UL, 0x6c728affUL, 0x71eae2a1UL, 0x1f9af36eUL, 0xcfcbd12fUL, 0xc1de8417UL,
0xac07be6bUL, 0xcb44a1d8UL, 0x8b9b0f56UL, 0x013988c3UL, 0xb1c52fcaUL, 0xb4be31cdUL, 0xd8782806UL, 0x12a3a4e2UL,
0x6f7de532UL, 0x58fd7eb6UL, 0xd01ee900UL, 0x24adffc2UL, 0xf4990fc5UL, 0x9711aac5UL, 0x001d7b95UL, 0x82e5e7d2UL,
0x109873f6UL, 0x00613096UL, 0xc32d9521UL, 0xada121ffUL, 0x29908415UL, 0x7fbb977fUL, 0xaf9eb3dbUL, 0x29c9ed2aUL,
0x5ce2a465UL, 0xa730f32cUL, 0xd0aa3fe8UL, 0x8a5cc091UL, 0xd49e2ce7UL, 0x0ce454a9UL, 0xd60acd86UL, 0x015f1919UL,
0x77079103UL, 0xdea03af6UL, 0x78a8565eUL, 0xdee356dfUL, 0x21f05cbeUL, 0x8b75e387UL, 0xb3c50651UL, 0xb8a5c3efUL,
0xd8eeb6d2UL, 0xe523be77UL, 0xc2154529UL, 0x2f69efdfUL, 0xafe67afbUL, 0xf470c4b2UL, 0xf3e0eb5bUL, 0xd6cc9876UL,
0x39e4460cUL, 0x1fda8538UL, 0x1987832fUL, 0xca007367UL, 0xa99144f8UL, 0x296b299eUL, 0x492fc295UL, 0x9266beabUL,
0xb5676e69UL, 0x9bd3dddaUL, 0xdf7e052fUL, 0xdb25701cUL, 0x1b5e51eeUL, 0xf65324e6UL, 0x6afce36cUL, 0x0316cc04UL,
0x8644213eUL, 0xb7dc59d0UL, 0x7965291fUL, 0xccd6fd43UL, 0x41823979UL, 0x932bcdf6UL, 0xb657c34dUL, 0x4edfd282UL,
0x7ae5290cUL, 0x3cb9536bUL, 0x851e20feUL, 0x9833557eUL, 0x13ecf0b0UL, 0xd3ffb372UL, 0x3f85c5c1UL, 0x0aef7ed2UL};

#else

const uint32_t s1[] PROGMEM = {
0xd440fb30UL, 0x0bffa09fUL, 0x2fcdec6bUL, 0x7a8c253fUL, 0x2f3f211eUL, 0xd34d009cUL, 0x40e50360UL, 0x49c99fcfUL,
0x27afd4bfUL, 0xb5bdbb88UL, 0x904003e2UL, 0x7596d098UL, 0xe0a0636eUL, 0xd261c315UL, 0x1d66e7c2UL, 0x8effd422UL,
0x6f3b6828UL, 0x59d07fc0UL, 0xc87923ffUL, 0xe2505f77UL, 0xd340c343UL, 0x56862fdfUL, 0x1aa47c88UL, 0x2dbdd2a2UL,
0xd6e0c9a1UL, 0x19486c34UL, 0x876db761UL, 0x2f0f5422UL, 0xe132be2aUL, 0x6b1654aaUL, 0x3a8e5622UL, 0xd041d3a2UL,
0xc840db66UL, 0x2f3984a7UL, 0x2fff4d00UL, 0xded2b92dUL, 0xac3f9497UL, 0xd8c1974aUL, 0xb7447652UL, 0xa737f4b5UL,
0xefba2cb8UL, 0x59d151d7UL, 0xedf0f76fUL, 0x1f7a095aUL, 0xd0687b82UL, 0x2ef5ec90UL, 0x54c0b022UL, 0x35598ebcUL,
0x7f2f6d4bUL, 0xa264bb50UL, 0x104966d2UL, 0x2d81e5beUL, 0x902233b7UL, 0x9f153be9UL, 0x11e48eb4UL, 0x5d34ff4bUL,
0x40c245fdUL, 0x3f9731adUL, 0x2ed0f6c4UL, 0x6581fc55UL, 0xadcab1d5UL, 0xae2daca1UL, 0x6db7d4a2UL, 0x500c9bc1UL,
0xf2402288UL, 0x384f6e0cUL, 0xd7bfe4a4UL, 0x72a25b4fUL, 0x2f1d4c56UL, 0x19539cc5UL, 0x54e349b9UL, 0xfe6946b0UL,
0x8aabb6b1UL, 0xdd5813c7UL, 0x45c58563UL, 0x5d930f11UL, 0xd58a5357UL, 0x9304396aUL, 0xe0373de6UL, 0xb3f6542aUL,
0x5f7d783aUL, 0xb5a07662UL, 0xdffca619UL, 0x6a20427aUL, 0xd5d4f929UL, 0x91181bf6UL, 0x5e2772bbUL, 0x678150aaUL,
0x91109038UL, 0xeb05b5c6UL, 0x8ccbc784UL, 0x0f5ad72aUL, 0x27144a87UL, 0x6b93d1a2UL, 0xaf86d22aUL, 0x91d256aaUL,
0x604389d7UL, 0x0d755c42UL, 0x269eb393UL, 0xc9847118UL, 0x2db3006cUL, 0x14bbe273UL, 0x3cbcbea0UL, 0x79376254UL,
0xab9e4564UL, 0x828b323fUL, 0x82cf1877UL, 0xa6cea259UL, 0x2e00ee04UL, 0xe678fe89UL, 0x5009ab3fUL, 0xc2f65f32UL,
0x053f3881UL, 0xc8c56369UL, 0xd65acb76UL, 0xc97499d4UL, 0xcf0d18caUL, 0xd5820738UL, 0xf65cfac7UL, 0x1115c38aUL,
0x139ee735UL, 0xd091da47UL, 0x86900ff4UL, 0x9e41e2a7UL, 0x41623631UL, 0x95f41e05UL, 0x043b57aaUL, 0x8d5d804aUL,
0xd0008354UL, 0x3c2a3200UL, 0xdfcd64bfUL, 0x8ea657baUL, 0x2b37c675UL, 0x41d3af50UL, 0x7532c1a7UL, 0xf50b5a91UL,
0xabbf546bUL, 0x26140b2bUL, 0xd7c94cabUL, 0x82cd9c44UL, 0x65f2fbf7UL, 0xf3c585abUL, 0x94db551bUL, 0x24e3d4aaUL,
0x3fbda4cfUL, 0xe2a3ea2dUL, 0x024d209eUL, 0xac25bdc8UL, 0xb355dfeaUL, 0x989ebdd5UL, 0xb23112e3UL, 0x6cadd52aUL,
0xde294395UL, 0x2845beadUL, 0x690f71d8UL, 0x0fc951aaUL, 0xf66b78aaUL, 0x1e3f5122UL, 0x9ba751aaUL, 0xcc44d32aUL,
0xf0415a7bUL, 0xadfb7cd3UL, 0x0595061bUL, 0x91e4ec41UL, 0xe632c3b4UL, 0xd4682203UL, 0xcc0a60c9UL, 0x6d7e38ceUL,
0x6cb16bbfUL, 0x78fb706aUL, 0xc9d9030dUL, 0xde39dfd4UL, 0xda6310e0UL, 0x64f43647UL, 0xd828d35aUL, 0x96cc47b3UL,
0xc30fbb75UL, 0xfb1b5198UL, 0x35ccfb4fUL, 0x6acf8bb5UL, 0xbc0a1fe1UL, 0x4afec5bfUL, 0x10ec0aa7UL, 0x0a5739acUL,
0x2f44043fUL, 0x53b18861UL, 0x2e7a39e0UL, 0x79cb2757UL, 0x8f41eb9cUL, 0x8dd6ac1cUL, 0x967cd32aUL, 0x9dcb7501UL,
0x09ff9dc6UL, 0xf0655bc7UL, 0xd840dbd9UL, 0x79770eecUL, 0xd4ea4447UL, 0x74321cb1UL, 0x9ecb24ddUL, 0xbd541c7eUL,
0xf94411f0UL, 0xb10e24d2UL, 0xfdb37596UL, 0x5537aca3UL, 0xaf277cd4UL, 0x4d5fc851UL, 0x96759056UL, 0xe615bba5UL,
0xf0040358UL, 0xf12c04caUL, 0xea371a01UL, 0xdbaabf8dUL, 0x4a3eba35UL, 0xa0ff2635UL, 0x094d7bc3UL, 0xd96e30bcUL,
0x6626a598UL, 0x25f74856UL, 0x9d565effUL, 0xd063ed0cUL, 0xcfb2637cUL, 0xe1450b70UL, 0xf150ead5UL, 0x7228a985UL,
0xa7bd1fafUL, 0x704823d4UL, 0xf30b87a7UL, 0x794d3b2dUL, 0x9841e042UL, 0xe7edd00cUL, 0xb80d4726UL, 0x4c8181f8UL,
0xd76a4d47UL, 0x5c5e0c7cUL, 0x591923d1UL, 0x98721b38UL, 0xdbf4d2f5UL, 0x538683abUL, 0x231e2f6eUL, 0x9e9c7183UL,
0x46e091bdUL, 0x6e45569aUL, 0x0c2039dcUL, 0x71c5c820UL, 0x1cda2b96UL, 0xff96e6e1UL, 0x08ab41b1UL, 0xb989ca7cUL,
0x83e7691aUL, 0x4348cc02UL, 0x79c5f7a2UL, 0x7df49e42UL, 0x9c167b42UL, 0x49f0c95aUL, 0x000f8fddUL, 0xbf65815cUL};

const uint32_t s2[] PROGMEM = {
0x9410201fUL, 0x5ba70befUL, 0x7ecfe369UL, 0x80433f39UL, 0x7acf61feUL, 0x7a20c5eeUL, 0x949c8855UL, 0x5106fc72UL,
0x79efa7adUL, 0x35721d4eUL, 0xce635ad5UL, 0xba3604deUL, 0xef30c499UL, 0x94070c5fUL, 0x7ddbdc18UL, 0xf3efd6a1UL,
0x7b2fb5a0UL, 0x0536e859UL, 0x94b015eeUL, 0x09d9ffe9UL, 0x860044dcUL, 0x594494efUL, 0xb3cc83baUL, 0xfbcdc3e0UL,
0x8141dad1UL, 0xb12a093bUL, 0xc1f197f9UL, 0x7bcfe6a5UL, 0xdb0d4201UL, 0x5befe7e4UL, 0x41ffa125UL, 0x06f880e1UL,
0x8010c41fUL, 0x7aee9b17UL, 0xa9c67ad3UL, 0xa43058feUL, 0x7f8bde98UL, 0x4e3fe877UL, 0x69929279UL, 0x7b9ffa24UL,
0x5bc813e1UL, 0x8300c4acUL, 0x253550d7UL, 0x5f61eaf7UL, 0x54311462UL, 0x634b550dUL, 0x2111685dUL, 0x59c366c8UL,
0x73cf633dUL, 0xc034e2ceUL, 0x877ed8d4UL, 0x212b675cUL, 0x81611f07UL, 0x7f62f739UL, 0x84301e36UL, 0x3b57ebe4UL,
0xa4642f60UL, 0x9ccd3ad6UL, 0x3546bc1bUL, 0x2d03819eUL, 0x0cf50127UL, 0xb47a8499UL, 0x79dfe3a0UL, 0x8cf36cbaUL,
0x94308410UL, 0x5ea93725UL, 0xfe6f6ff4UL, 0x1f3bffa1UL, 0x6afb8c20UL, 0x748c458fUL, 0x27a2e0d9UL, 0x343ac74eUL,
0x694f88fcUL, 0xdfe84d3eUL, 0x88000eefUL, 0x8d645935UL, 0x8c38458aUL, 0x6643801dUL, 0xfd9b1d72UL, 0xbb8486a5UL,
0x336325e8UL, 0x12824e84UL, 0x98808d12UL, 0xb43fd3feUL, 0xe10a28ceUL, 0xa59be127UL, 0x52c2a6d5UL, 0xbd5497e4UL,
0xdd55d6c5UL, 0x647066ebUL, 0x4d0b8477UL, 0x01a8b6a1UL, 0xa926db84UL, 0x1467b5e0UL, 0xb743f021UL, 0x6058d0e5UL,
0x8430f054UL, 0x72f46f06UL, 0x53a11aa3UL, 0x5547dcdaUL, 0xbf5d62b5UL, 0xe61b5668UL, 0x946bca83UL, 0x3bd26e2dUL,
0xdb01cfecUL, 0xbad0d3a6UL, 0x5c3d80b6UL, 0x09a777afUL, 0x4ca3b433UL, 0xd6c87b39UL, 0x952be25eUL, 0x04530e5fUL,
0x616fed81UL, 0x6443e720UL, 0x78135eb4UL, 0x9b6318deUL, 0x22a11c88UL, 0xd12667b9UL, 0xe8a74980UL, 0x7bdab722UL,
0x252d555eUL, 0x37d27252UL, 0x1c95d279UL, 0x4c890dc6UL, 0x02b48c48UL, 0x5bfea41bUL, 0x6b9fb0a4UL, 0xcf15a81cUL,
0x05300ca2UL, 0x63df7188UL, 0xcb2fdeb9UL, 0xe9c9c60cUL, 0x53ffee0bUL, 0x174521e3UL, 0x352854b4UL, 0x3c29639fUL,
0x29e741eeUL, 0x7c2d1d6eUL, 0x86520450UL, 0xf385661eUL, 0xc60134f3UL, 0x952ca230UL, 0x5008a731UL, 0x130f9360UL,
0x1784f973UL, 0x599826a1UL, 0x445c64ecUL, 0xa977c852UL, 0xa633ffcdUL, 0x41172ba0UL, 0xa2d9ba7cUL, 0x6f038021UL,
0x089cd950UL, 0x61483fcbUL, 0x65d76bc2UL, 0xabf6a364UL, 0x76263480UL, 0x7b5ea725UL, 0xfcd1e6e4UL, 0xe610c720UL,
0x80b6f0cdUL, 0x3b4d8417UL, 0x4df8ee31UL, 0xe424087eUL, 0xeb49cb2cUL, 0xae3b6a84UL, 0x8878f78fUL, 0xf6605deeUL,
0x7356f77aUL, 0xdb5cdd2fUL, 0xc13116a1UL, 0x436ff630UL, 0x54ecfab3UL, 0xfad77f15UL, 0xcc7985efUL, 0x58de52d1UL,
0x5efd2fdbUL, 0x19ce328fUL, 0x7af96a30UL, 0xf83ef002UL, 0xd59a3199UL, 0x0ffa42c2UL, 0xb0ebe3a7UL, 0x06498ec6UL,
0x0c23dab8UL, 0x28308280UL, 0xc8f3dedcUL, 0x71b15fd3UL, 0xc81b8a08UL, 0x60c5c0beUL, 0xe8c9a361UL, 0x4df5a8bcUL,
0xfaef2fc7UL, 0x992e8222UL, 0xb470c582UL, 0x894ed9d8UL, 0xbc341c8bUL, 0xe6161e30UL, 0x79e93b27UL, 0xa6eaffb0UL,
0xc6b8d961UL, 0x6948b200UL, 0x3fceffb7UL, 0x3b28dc08UL, 0x5af6da43UL, 0x9897e1f7UL, 0x2fb71976UL, 0xa49b1c8fUL,
0xa03786dcUL, 0xb1d3a716UL, 0xb793c39fUL, 0xeb6e13a7UL, 0x3ec6bcc6UL, 0x4237511aUL, 0xbc2868efUL, 0xd6650352UL,
0xab776a2dUL, 0x4bed2735UL, 0x16d21f82UL, 0x2e6e5c09UL, 0xfbf292dbUL, 0xcb29ea5eUL, 0xf5925814UL, 0x7f4f5891UL,
0x7b698354UL, 0xcca86726UL, 0x48601985UL, 0xeaac4b8cUL, 0xd4603883UL, 0xf9e0230dUL, 0x8a7e386cUL, 0x49d2e60aUL,
0x0c6084b2UL, 0x1d7335d8UL, 0x47c6b1dcUL, 0xea564cacUL, 0xb381bd3eUL, 0xb0ab0e23UL, 0x87bc3864UL, 0xfab1b5f0UL,
0xb3a25e8fUL, 0x424618fcUL, 0x7a6b030aUL, 0xbd89b04fUL, 0x89a59d64UL, 0x5e4145a3UL, 0x2383035cUL, 0xb93b5d3eUL,
0x7295d743UL, 0x7cd06d7eUL, 0x1edfdf06UL, 0xefc46c6cUL, 0x39a56071UL, 0x70bebf73UL, 0x05768783UL, 0xf1ec2345UL};

const uint32_t s3[] PROGMEM = {
0x40c2ef8dUL, 0x9f5dfa25UL, 0xbf3d90ebUL, 0x07c910e8UL, 0xff7f6047UL, 0x4be49f36UL, 0x44c61f8cUL, 0x90caceaeUL,
0xbff9b1beUL, 0xeacafbeeUL, 0x5019cfe8UL, 0xae07df51UL, 0x06880e92UL, 0x4805adf0UL, 0x838d3ce1UL, 0xd5107092UL,
0x9f7d1011UL, 0xb97d6407UL, 0xd4e4e3b2UL, 0x5e284f3dUL, 0x20a8afb9UL, 0xe082defaUL, 0x8b2667a0UL, 0x2e797282UL,
0xc0b23f55UL, 0x2be29a48UL, 0x9497efd4UL, 0xbc3f5e12UL, 0xeefcff21UL, 0xfd1b5b82UL, 0xedc55592UL, 0x40a25712UL,
0x02831a4eUL, 0xff7fe0baUL, 0xe7468252UL, 0x0e14578eUL, 0xbff77333UL, 0x88819f8cUL, 0xe84efca6UL, 0xa5b582c9UL,
0xb71dc0a8UL, 0x64c29f57UL, 0x314f0967UL, 0x5f3fbdf2UL, 0xc1f7ff40UL, 0xfc8db71fUL, 0xc1d26b8eUL, 0x9be57b43UL,
0xbf3db099UL, 0x4bc6dbb5UL, 0xe6c08d63UL, 0x999d8155UL, 0x1cc897a1UL, 0x6e2d014aUL, 0x284a88c5UL, 0x716fc3ccUL,
0x13c243b8UL, 0xf143076cUL, 0x3c890983UL, 0x5fdded0fUL, 0x50e87f2fUL, 0x7e7fc0d7UL, 0xbf7f5002UL, 0x049afb5aUL,
0xd0d247a7UL, 0x2e195116UL, 0x3ebf70afUL, 0x8013c358UL, 0x2e30985fUL, 0xc4c37c72UL, 0x02b40f0aUL, 0x82ef7f0fUL,
0xadfd968cUL, 0xae2a2c5dUL, 0x499ae98eUL, 0xb888da50UL, 0xa0f42784UL, 0x9057ac1eUL, 0x49b46f79UL, 0x15dc5282UL,
0x9b7dbdefUL, 0x7d5972a6UL, 0xd840a8adUL, 0x0445f545UL, 0x03745dfaUL, 0x05c33ee8UL, 0x1a75914fUL, 0xc2695692UL,
0x41e9ef23UL, 0x2ef103a9UL, 0xf20d2760UL, 0xb6e47602UL, 0x7465fd94UL, 0xb2857992UL, 0xcbdb7682UL, 0x76817702UL,
0x8d91aff8UL, 0x9ef7484eUL, 0xdf6d618fUL, 0x0e849de2UL, 0x837d2f84UL, 0xc8e50c34UL, 0x82b6bb96UL, 0x48b1b493UL,
0xab3c30efUL, 0x28af4f98UL, 0x9baf9f77UL, 0x0d56dc92UL, 0x201e4d22UL, 0x88aa3784UL, 0x96dc297dUL, 0xdcd35627UL,
0xee7c908bUL, 0x40d21fb5UL, 0xe37cc0e7UL, 0xa1b466e5UL, 0x5e61e9c3UL, 0x9d20f83cUL, 0xe3d19460UL, 0x41a39ccdUL,
0x0e46765cUL, 0x3b98ea00UL, 0x8178d6d4UL, 0x2c5747fdUL, 0xd9ed6cf7UL, 0x9c22a8bdUL, 0xaaad7d12UL, 0x4e078a43UL,
0x90c0971fUL, 0x8adb1b08UL, 0xbe7ea093UL, 0x15ca38b9UL, 0xff3cb097UL, 0xf8c0c23dUL, 0xecb21a8dUL, 0x510e3864UL,
0xfb7bcc68UL, 0x88270fd9UL, 0x81014912UL, 0xd4ffe55dUL, 0x6af87eddUL, 0x14e2a276UL, 0x6803a4b9UL, 0x8f955d92UL,
0xfaff394bUL, 0xe9ae39baUL, 0x0bd3ffa4UL, 0x3b93f7faUL, 0x2386496dUL, 0xfabc3c19UL, 0x45756227UL, 0x7af45c82UL,
0xa08bbd61UL, 0xd1421ed1UL, 0xf404adceUL, 0x92a37e12UL, 0xb78d4210UL, 0x72a97282UL, 0xa8c47092UL, 0x0be57d12UL,
0xc8a15b28UL, 0x4ff4623cUL, 0xa5eac035UL, 0x31d205e8UL, 0xfb298942UL, 0x82dffcb4UL, 0x536ab64fUL, 0x5bc17d0eUL,
0xab1f081fUL, 0xae188610UL, 0x6d08fdfcUL, 0x8928fff9UL, 0x11cc4b69UL, 0xae5c6a23UL, 0x4dcade12UL, 0xc58c3f2cUL,
0xfe2dd0d2UL, 0x9658eff8UL, 0xda52cfe4UL, 0x675b1595UL, 0x8c484a49UL, 0x0ca8b6b9UL, 0xbc828f5cUL, 0x456bd389UL,
0x3794603aUL, 0xa9c900ecUL, 0x53527144UL, 0x494b870aUL, 0x40bc73d7UL, 0x1c67347cUL, 0xf67e7102UL, 0x3655eb4fUL,
0xff2fd0a2UL, 0xc460bfd2UL, 0xc0033fd4UL, 0x6defb450UL, 0xd18c4707UL, 0x88186e00UL, 0x553fe5a2UL, 0xbcd4e6b9UL,
0x168004a2UL, 0x33385797UL, 0x677d20d7UL, 0x3d8f0fdeUL, 0x337bf872UL, 0x334fccabUL, 0x5dc58876UL, 0xb0a6007bUL,
0x01007b94UL, 0xd2750057UL, 0xf888bbf9UL, 0x9e014289UL, 0xffa56442UL, 0xe0026385UL, 0x2bd9db72UL, 0x691b97eeUL,
0xde2fa26eUL, 0x2bae085fUL, 0x6d617aafUL, 0x6787c9e5UL, 0xd2eb1fcfUL, 0xc2c8ef61UL, 0x7125acf1UL, 0xc23982ccUL,
0xb84c2167UL, 0xd183e5b1UL, 0x623edcb7UL, 0xcebd107fUL, 0x385c0af9UL, 0x3d44f00fUL, 0xc66d6e60UL, 0x493a5460UL,
0x48c12757UL, 0x1d8ae92bUL, 0x3817b48aUL, 0x24bee120UL, 0x0fda96afUL, 0x25844568UL, 0xe53b8399UL, 0x7d450d60UL,
0x50932f28UL, 0x62b33483UL, 0x20111dd9UL, 0xa08d6d2bUL, 0x311e2b64UL, 0x005a309cUL, 0x88e6bc52UL, 0x8a58031bUL,
0xd5efbaf7UL, 0x9ced4241UL, 0x115c31a4UL, 0xc53e3283UL, 0x3646efdfUL, 0x01c533a1UL, 0x1c53d3e9UL, 0x833735eeUL};

const uint32_t s4[] PROGMEM = {
0x2004b39dUL, 0xdee9b61fUL, 0xef7bbea7UL, 0x98a273d2UL, 0xdb7b4f4aUL, 0x578cad64UL, 0x43045185UL, 0xd10e02faUL,
0xff7a287eUL, 0x63b60fe6UL, 0xa1355f09UL, 0x20f1eb79UL, 0x439d05fdUL, 0xb1b79764UL, 0x631f64f3UL, 0xdf4a1e24UL,
0x5f7f1428UL, 0xcdb8a24fUL, 0x400043c9UL, 0x2022c30cUL, 0x300bd3fdUL, 0x4f37a5c0UL, 0xd9002d1dUL, 0x157b1424UL,
0x1a114deeUL, 0x6751ca0fUL, 0x4c90ff71UL, 0xfe5f192dUL, 0x5f64051aUL, 0xfefe130cUL, 0xca081b08UL, 0x21011705UL,
0x00015380UL, 0xfe5e3ee8UL, 0xf8f49aacUL, 0x0127e77fUL, 0x5feeb8d2UL, 0x6142df06UL, 0x8a9b9ebbUL, 0x25ea9372UL,
0xdfff84ceUL, 0x018871f5UL, 0x044bd63dUL, 0x3b266fa2UL, 0x0084d47eUL, 0xe6eb7e54UL, 0xa04c6d44UL, 0xf5d6f36cUL,
0xdfab4926UL, 0xf5c7a0aeUL, 0xc18c3336UL, 0x937e3f50UL, 0x612077d3UL, 0xe138b611UL, 0x030e5072UL, 0xbbb20ef8UL,
0x2e50e0abUL, 0xde778decUL, 0x811e9757UL, 0x46674fe1UL, 0x005433c9UL, 0x8f312069UL, 0x99bb1d08UL, 0xa504c3ffUL,
0x0518354dUL, 0xe35c3d7fUL, 0xc666c8a6UL, 0xa9cc5b5dUL, 0xea6fecdaUL, 0x916f929fUL, 0x2f22469fUL, 0x7d469139UL,
0x8e6dbfa5UL, 0x4fc44311UL, 0x02839543UL, 0xeb4e21d0UL, 0xb8832002UL, 0x0c18b63fUL, 0x1e93f818UL, 0xe6581628UL,
0x3e6e4826UL, 0x708ad78bUL, 0xc1e47774UL, 0x7ce006b5UL, 0x250a2df3UL, 0x028b0979UL, 0x81bbeae4UL, 0x233b1228UL,
0x38adde69UL, 0x16ca7415UL, 0x621b87dfUL, 0xb7401c21UL, 0xf99e1aa5UL, 0x7b371400UL, 0xc88a1e04UL, 0x03401109UL,
0xd2e459bdUL, 0xd556d1e3UL, 0xd576e84fUL, 0x40a3912fUL, 0xdee87b55UL, 0xa7e4ea00UL, 0xecc2e50cUL, 0xa6bbb44dUL,
0xffbd56e7UL, 0xac6933ddUL, 0x35b017ecUL, 0x27235706UL, 0xb0c8af99UL, 0x91c3c856UL, 0x1c81656bUL, 0x1961145eUL,
0x75cb856eUL, 0x02c007beUL, 0x775532c2UL, 0xecf43f89UL, 0x2dc9bf5bUL, 0x253becd0UL, 0xb71a80b7UL, 0x243b6d8dUL,
0xef63c720UL, 0xfca566c3UL, 0x8028389cUL, 0x0532ce0aUL, 0x8a54c9aaUL, 0xc7d7a1ecUL, 0x32fa1a04UL, 0x5a62161dUL,
0x2c900167UL, 0x547a759bUL, 0xf777d431UL, 0x31b02691UL, 0xdb6fcc36UL, 0x468b0bc7UL, 0x486ae6d9UL, 0x795ae556UL,
0xeb4c6a02UL, 0xff7e4352UL, 0xb4768f2fUL, 0xa580f90dUL, 0xe3cd7486UL, 0xeb04daedUL, 0x04bea917UL, 0xdff4182cUL,
0x9d7f74b7UL, 0xb4f72aabUL, 0x204dc3efUL, 0x7c6b092eUL, 0x54a24117UL, 0x35a0b6e5UL, 0xf6423d21UL, 0x267c1c2cUL,
0x0ff5c261UL, 0xf9da5265UL, 0xf831c2d2UL, 0x690f1325UL, 0xa27f16d8UL, 0xc8f21804UL, 0xa6961a00UL, 0xab26150dUL,
0x215c3163UL, 0xec720a5eUL, 0xfdfeba49UL, 0xd9087918UL, 0x86bd0d8dUL, 0xa7701131UL, 0x0c649b3eUL, 0xd7103eccUL,
0xb6d3cad5UL, 0x88c3ae0cUL, 0xe10130f7UL, 0xff8a726cUL, 0xa1e2ea71UL, 0x6ef39a1fUL, 0x2fd1cbcfUL, 0x1784dec1UL,
0x6bbe07acUL, 0xd8a144cbUL, 0x560f9b8bUL, 0xc3883901UL, 0xca2fc5b1UL, 0xcd31beb4UL, 0x062878d8UL, 0xe2a4a312UL,
0x32e57d6fUL, 0xb67efd58UL, 0x00e91ed0UL, 0xc2ffad24UL, 0xc50f99f4UL, 0xc5aa1197UL, 0x957b1d00UL, 0xd2e7e582UL,
0xf6739810UL, 0x96306100UL, 0x21952dc3UL, 0xff21a1adUL, 0x15849029UL, 0x7f97bb7fUL, 0xdbb39eafUL, 0x2aedc929UL,
0x65a4e25cUL, 0x2cf330a7UL, 0xe83faad0UL, 0x91c05c8aUL, 0xe72c9ed4UL, 0xa954e40cUL, 0x86cd0ad6UL, 0x19195f01UL,
0x03910777UL, 0xf63aa0deUL, 0x5e56a878UL, 0xdf56e3deUL, 0xbe5cf021UL, 0x87e3758bUL, 0x5106c5b3UL, 0xefc3a5b8UL,
0xd2b6eed8UL, 0x77be23e5UL, 0x294515c2UL, 0xdfef692fUL, 0xfb7ae6afUL, 0xb2c470f4UL, 0x5bebe0f3UL, 0x7698ccd6UL,
0x0c46e439UL, 0x3885da1fUL, 0x2f838719UL, 0x677300caUL, 0xf84491a9UL, 0x9e296b29UL, 0x95c22f49UL, 0xabbe6692UL,
0x696e67b5UL, 0xdaddd39bUL, 0x2f057edfUL, 0x1c7025dbUL, 0xee515e1bUL, 0xe62453f6UL, 0x6ce3fc6aUL, 0x04cc1603UL,
0x3e214486UL, 0xd059dcb7UL, 0x1f296579UL, 0x43fdd6ccUL, 0x79398241UL, 0xf6cd2b93UL, 0x4dc357b6UL, 0x82d2df4eUL,
0x0c29e57aUL, 0x6b53b93cUL, 0xfe201e85UL, 0x7e553398UL, 0xb0f0ec13UL, 0x72b3ffd3UL, 0xc1c5853fUL, 0xd27eef0aUL};

#endif

