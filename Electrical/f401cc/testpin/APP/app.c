#include "app.h"
#include "freertos.h"
#include "task.h"
#include "cmsis_os2.h"
#include "bsp_key.h"
//========================================================================
// 函数: test1  task
// 描述: .
// 参数: None.
// 返回: None.
//========================================================================
osThreadId_t Task1Handle;
const osThreadAttr_t Task1Attributes = {
  .name = "task1",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};


void task1_entry(void *argument)
{
  for(;;)
  {
		//bsp_keyScan_20ms();
		osDelayUntil(xTaskGetTickCount()+20);
  }
}

void sys_init()
{
	taskENTER_CRITICAL();//进入临界段
	
	Task1Handle = osThreadNew(task1_entry, NULL, &Task1Attributes);
	
	taskEXIT_CRITICAL();//退出临界段
	
}











