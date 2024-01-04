#ifndef _MOTION_PLANTER_H
#define _MOTION_PLANTER_H
#include "user_main.h"

extern int16_t trackSpeedPss;//过程速度,必须为正
extern int16_t trackAcc;//加速度,必须为正
extern int16_t trackAccEnd;
extern int32_t trackPosEnd;//终点位置
extern int16_t trackSpeedEnd;//终点速度
extern int32_t softPos;//输出位置
extern int16_t softSpeed;//
extern uint8_t trackPoint_Finish;
void trackTriger(void);
void Motor_Digital_Track(void);
int32_t i32_abs(int32_t in);
#endif
