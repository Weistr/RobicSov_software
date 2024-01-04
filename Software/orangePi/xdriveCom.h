#ifndef _XDRIVECOM_H
#define _XDRIVECOM_H
#include <sys/types.h>

#pragma pack(1)
typedef struct  
{
    u_int8_t id;
    u_int8_t mode;
    int32_t pos;
    int16_t speed;
    int16_t crc;
}xdriveComTypddef;
#pragma pack()


extern xdriveComTypddef xdriveCtl_Send[4];
extern xdriveComTypddef xdriveCtl_Recv[4];
void motorPosControl(u_int8_t id, int32_t pos, int32_t speed);
void motorStop(u_int8_t id);

#endif
