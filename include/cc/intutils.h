extern unsigned short short_from_bytes(unsigned char lsb, unsigned char msb);
extern unsigned int int_from_shorts(unsigned short lsw, unsigned short msw);
extern unsigned long long_from_ints(unsigned int lsd, unsigned int msd);
unsigned short short_from_bytes_msb_left(unsigned char lsb, unsigned char msb);
unsigned short short_from_bytes_msb_right(unsigned char lsb, unsigned char msb);
unsigned int int_from_bytes_msb_left(unsigned char lsb, unsigned char byte1, unsigned char byte2, unsigned char msb);
unsigned int int_from_bytes_msb_right(unsigned char lsb, unsigned char byte1, unsigned char byte2, unsigned char msb);
unsigned long long_from_bytes_msb_left(unsigned char lsb, unsigned char byte1, unsigned char byte2, unsigned char byte3, unsigned char byte4, unsigned char byte5, unsigned char byte6, unsigned char msb);
unsigned long long_from_bytes_msb_right(unsigned char lsb, unsigned char byte1, unsigned char byte2, unsigned char byte3, unsigned char byte4, unsigned char byte5, unsigned char byte6, unsigned char msb);
unsigned long ascii_to_long(panah_asciinum_t ascii);
panah_nonyield_t long_to_ascii(unsigned long number, panah_asciiznum_t asciinum);