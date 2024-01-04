#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

#include <string.h>
#include "xdriveCom.h"
#include "usbCom.h"

int main(void)
{ 
    usbComInit();
    while (1)
    {
        float pos=0;
        printf("\ndeg=");
        scanf("%f",&pos);
        motorPosControl(0x01, pos/360.0*51200, 0);
        sleep(1);

        usbComRead((u_int8_t*)&xdriveCtl_Recv[1],10);
        u_int8_t* pbuf = (u_int8_t*)&xdriveCtl_Recv[1];
        printf("\n");
        for (int i = 0; i < 10; i++)
        {
            printf(" %x", pbuf[i]);
        }
        
        float rcvDeg = xdriveCtl_Recv[1].pos/51200*360.0;
        float rcvSpd = xdriveCtl_Recv[1].speed/400;
        printf("\n receive:\ndeg = %f\nspeed=%fr/s",rcvDeg,rcvSpd);

    }
    return 1;
}
