#ifndef _CRC16MODBUS_H
#define _CRC16MODBUS_H
#include <sys/types.h>
u_int16_t crc16Cal(u_int8_t *in, u_int16_t length);

#endif