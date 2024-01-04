#ifndef _USER_MAIN_H
#define _USER_MAIN_H
#include "main.h"
typedef struct 
{
	uint8_t Run;               //任务状态：Run/Stop
	uint16_t TIMCount;         //定时计数器
	uint16_t TRITime;          //重载计数器
	void (*TaskHook) (void); //任务函数
} TASK_COMPONENTS;       

//========================================================================
//                             外部函数和变量声明
//========================================================================

void Task_Marks_Handler_Callback(void);
void Task_Pro_Handler_Callback(void);
void user_main(void);


#define BYTE0(dwTemp)       ( *( (char *)(&dwTemp)		) )
#define BYTE1(dwTemp)       ( *( (char *)(&dwTemp) + 1) )
#define BYTE2(dwTemp)       ( *( (char *)(&dwTemp) + 2) )
#define BYTE3(dwTemp)       ( *( (char *)(&dwTemp) + 3) )

#endif
