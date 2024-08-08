#include "bsp_key.h"
#include "stdbool.h"

//========================================================================
// 函数: bsp_keyScan_20ms 
// 描述: .
// 参数: None.
// 返回: None.
//========================================================================
bool key0Val=0;//按键按下置1，松开置0
bool key0OneClicFlag=0;//按键单击标志位  触发取反
bool key0TwoClicFlag=0;//按键双击标志位  触发取反
bool key0LonClicFlag=0;//按键长按标志位  触发取反
uint8_t clicTimeSpan_x20ms = 15;//双击时间间隔 默认300ms
/*
void bsp_keyScan_20ms()
{
	static bool key0ValPrevious=0;
	static uint8_t clicCnt=0,timeOutCnt=0;
	
	if(HAL_GPIO_ReadPin(KEY0_GPIO_Port,KEY0_Pin))
	{
		key0Val=1;
		if(key0ValPrevious != key0Val)//按键按下
		{
			clicCnt++;
			timeOutCnt=0;
			if(clicCnt == 1)//单击
				key0OneClicFlag =~ key0OneClicFlag;
			else if(clicCnt == 2)//双击
				key0TwoClicFlag =~ key0TwoClicFlag;
			else 
				key0TwoClicFlag =~ key0TwoClicFlag;//超过两次也算双击
		}
		else
		{
			timeOutCnt++;
			if(timeOutCnt > clicTimeSpan_x20ms)
			{
				timeOutCnt = 0;
				clicCnt = 0;
			}
		}
		key0ValPrevious = key0Val;
	}
}
*/
