#ifndef _CUBEMOTION_H
#define _CUBEMOTION_H
#include "user_main.h"
typedef struct 
{
    int16_t speedPss;//转面时速度
    int16_t acc;
    int16_t accEnd;    
}wristMotionTypedef;
typedef struct
{
    uint8_t motorid;
    int32_t rstPos;
    wristMotionTypedef motion[3];//0:空转速度，1：换面速度，2：转面速度
    uint8_t status;
    int32_t posNow;//当前位置
    int32_t speedNow;
}roboWristTypedef;
typedef struct
{
    uint8_t motorid;    
    int32_t rstPos;
    int32_t g_openPos;
    int32_t g_closeCurrent;

    uint8_t status;
    int32_t posNow;//当前位置
    int32_t speedNow;
}roboGripperTypedef;


//部件定义
#define Lg 0 //左夹爪
#define Rg 1 //
#define Lw 2 //左手腕
#define Rw 3
//角度限制
#define wristPosMax 270//最大270, 不能小于180, 必须为90整数倍
#define wristPosMin -270//最小-270，不能大于-180, 必须为390整数倍
/*action*/
//动作定义
#define w_cw90 '0'//顺时针90，腕动作
#define w_ccw90 '1'//逆时针90，腕动作
#define w_r180 '2' //转180，腕动作
#define w_horizon '3' //水平,腕动作
#define w_rst '4' //复位，腕动作

#define f_cw90 '0' //面动作
#define f_ccw90 '1' 
#define f_r180 '2'

#define g_close '1'//夹爪闭
#define g_open '2'
#define g_rst '0'

#define defaultSta 0

#define serialAction_checkCode_OK 0
#define serialAction_checkCode_warning_sameRcv 0x01
#define serialAction_checkCode_error_illgelChar 0xF0
#define serialAction_checkCode_error_open2Gri 0xF1
#define serialAction_checkCode_error_enptyRotate 0xF3
#define serialAction_checkCode_error_90degCof 0xF2

#define actionStrLenMax 600 

extern roboWristTypedef roboWrist[];
extern roboGripperTypedef roboGripper[];
extern char actionSerialStr[];
extern uint8_t serialActionStartFlag;
extern uint16_t cubeStrStepCord;//

void serialActionStart(void);//任务启动
void roboInit(void);
void serialActionTask(void);
uint8_t serialConfict_Test(char* strin,uint16_t strlen,uint8_t LGpresta,uint8_t RGpresta,uint8_t LWpresta,uint8_t RWpresta);


#define xdrive_motor 0
#define zdt_motor 1
#define wrist_motor_type zdt_motor



#endif

