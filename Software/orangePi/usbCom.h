#ifndef _USBCOM_H
#define _USBCOM_H
#include <sys/types.h>


int usbComInit(void);
void usbComSend(u_int8_t* buf, int len);
void usbComRead(u_int8_t* buf, int len);

#endif