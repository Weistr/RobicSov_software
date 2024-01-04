#include "xdriveCom.h"
#include "crc16modbus.h"
#include "usbCom.h"


xdriveComTypddef xdriveCtl_Send[4];
xdriveComTypddef xdriveCtl_Recv[4];

void motorPosControl(u_int8_t id, int32_t pos, int32_t speed)
{
    xdriveCtl_Send[id].id = id;
    xdriveCtl_Send[id].mode = 0x20;
    xdriveCtl_Send[id].pos = pos;
    xdriveCtl_Send[id].speed = speed;
    xdriveCtl_Send[id].crc = crc16Cal((u_int8_t*)&xdriveCtl_Send[id],8);
    usbComSend((u_int8_t*)&xdriveCtl_Send[id],10);
}
void motorStop(u_int8_t id)
{
    xdriveCtl_Send[id].id = id;
    xdriveCtl_Send[id].mode = 0x10;
    xdriveCtl_Send[id].crc = crc16Cal((u_int8_t*)&xdriveCtl_Send[id],2);
    usbComSend((u_int8_t*)&xdriveCtl_Send[id],4);
}