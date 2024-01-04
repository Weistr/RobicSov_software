#ifndef _OPICOM_H
#define _OPICOM_H
#include "user_main.h"

void OpiUartTask(void);
void OpiRcvTask(void);
extern uint8_t originMod;
#endif
