#ifndef _XDRIVECOM_H
#define _XDRIVECOM_H
#include "user_main.h"
#include "stdbool.h"
void motorPosControl(uint8_t id, int32_t pos, int32_t speed);
void motorSpeedControl(uint8_t id, int32_t speed);
void motorCurrControl(uint8_t id, int16_t Curr);
void motorStop(uint8_t id);
void motorRcvStatusUpdate(uint8_t id);

extern int32_t XdPosRcv,XdSpeedRcv;
extern uint8_t idRcv;
extern bool xdRcvFinsh_Falg;
#endif
