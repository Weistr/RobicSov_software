#include "motionPlanter.h"

#include "bsp_uart.h"
#include "crc16modbus.h"
#include "usart.h"
#include "XdriveCom.h"
#include "crc16modbus.h"
#include "bsp_led.h"
#include "cubeMotion.h"

#include <string.h>
#include <math.h>
int32_t i32_abs(int32_t in)
{
	if (in > 0)
	{
		return in;
	}
	else return -in;
	
}

int8_t i32_polAdj(int32_t A,int32_t B)//AB同号输出1，异号输出0
{
	if((A+B) == (i32_abs(A)+ i32_abs(B))) return 1;
	else return 0;
}
/******************************************************************************************************************************/
/******************************************************************************************************************************/
/******************************************************************************************************************************/
/****************************************  梯形加速位置插补器(只能输入终点)   ****************************************/
/**
 * 控制流程
 * 1.计算当前位置与目标位置差poserror
 * 2.当前应该加速还是减速：当前速度speedest > 目标速度trackSpeed必定减速，反之：
 * 预测如果以当前位置减速，在目标位置之后到达则减速。反之加速
*/

extern uint8_t userMode;
int16_t speedSpan = 32;

int16_t trackSpeedPss;//过程速度,必须为正
int16_t trackAcc;//加速度,必须为正
int16_t trackAccEnd;
int32_t trackPosEnd;//终点位置
int16_t trackSpeedEnd=0;//终点速度

int32_t vctPos;//位置向量,由起点指向终点
int32_t lenPos;//位置向量的模
int32_t lenPos2;//

int32_t tx;//目标速度减速到0移动的距离
int32_t txa;
int32_t sx;//起始速度减速到0移动的距离
int32_t softPos;//中间变量，位置
int16_t softSpeed=0;//
int16_t softAcc;//
int16_t softAccEnd;//

uint8_t sphere=0;//trackTriger 与 Motor_Digital_Track互斥信号量
uint8_t step=0;
uint8_t cvflag=0;

uint8_t trackPoint_Finish = 0;
void trackTriger()
{
	step=0;
	/*******************初始化参数******************************************************/
	trackSpeedPss = i32_abs(trackSpeedPss);//强制转为正数
	trackAcc = i32_abs(trackAcc);//强制转为正数
	trackAccEnd = i32_abs(trackAccEnd);//强制转为正数
/*
	if(trackPosEnd > posMax)trackPosEnd=posMax;//限制输入
	if(trackPosEnd < posMin)trackPosEnd=posMin;
	if(trackSpeedPss > speedMax)trackPosEnd=speedMax;
	if(trackAcc > accMax)trackAcc=accMax;
*/



//	softSpeed = motor_control.est_speed;//读取传感器的值
//	softPos = motor_control.est_location;

	vctPos = trackPosEnd - softPos;//位置向量,由起点指向终点
	lenPos = i32_abs(vctPos);//位置向量的模
	
	tx = trackSpeedPss*trackSpeedPss / (2*trackAccEnd);//目标速度减速到0移动的距离
	txa = trackSpeedPss*trackSpeedPss / (2*trackAcc);//0加速目标速度移动的距离
	sx = softSpeed*softSpeed / (2*trackAccEnd);//起始速度减速到0移动的距离
	
	/**************运算**********************************************************/
	if(i32_polAdj(vctPos,softSpeed)||(softSpeed==0))//pos与速度同方向，即速度指向终点
	{
		lenPos2 = i32_abs(sx-lenPos);
		if(sx > lenPos)//减速到0超过终点
		{
			if(lenPos2 > tx + txa)//减速到0再加速超过期望速度
			{
				if(vctPos>0)trackSpeedPss = -trackSpeedPss;//vt与vpos反向
				cvflag = 1;//有匀速过程
			}
			else if(lenPos2 == tx + txa)//刚好达到
			{
				if(vctPos>0)trackSpeedPss = -trackSpeedPss;//vt与vpos反向
				cvflag = 0;//无匀速过程
			}
			else//减速到0再加速无法达到期望速度
			{
				trackSpeedPss = sqrt(2*lenPos2*trackAcc*trackAccEnd/(trackAcc+trackAccEnd));//重设期望速度
				if(vctPos > 0)trackSpeedPss = -trackSpeedPss;////vt与vpos反向
				cvflag = 0;//无匀速过程
			}
		}
		else if(sx < lenPos)//不会超过终点
		{
			if(lenPos > tx + txa)//减速到0再加速超过期望速度
			{
				if(vctPos < 0)trackSpeedPss = -trackSpeedPss;//vt与vpos同向
				//vt不变
				cvflag = 1;//有匀速过程
			}
			else if(lenPos == tx + txa)//刚好达到
			{
				if(vctPos < 0)trackSpeedPss = -trackSpeedPss;//vt与vpos同向
				//vt不变
				cvflag = 0;//无匀速过程
			}
			else//减速到0再加速无法达到期望速度
			{
				trackSpeedPss = sqrt(2*lenPos*trackAcc*trackAccEnd/(trackAcc+trackAccEnd));//重设期望速度
				if(vctPos < 0)trackSpeedPss = -trackSpeedPss;//vt与vpos同向
				cvflag = 0;//无匀速过程
			}
		}
		else//刚好终点
		{
			if(vctPos < 0)trackSpeedPss = -trackSpeedPss;//vt与vpos同向
			cvflag = 0;//无匀速过程
		}
	}
	else//pos与速度反向，即速度远离终点
	{
		lenPos2 = sx+lenPos;
		if(lenPos2 > tx + txa)//减速到0再加速超过期望速度
		{
			if(vctPos < 0)trackSpeedPss = -trackSpeedPss;//vt与vpos同向
			//vt不变
			cvflag = 1;//有匀速过程
		}
		else if(lenPos2 == tx + txa)//刚好达到
		{
			if(vctPos < 0)trackSpeedPss = -trackSpeedPss;//vt与vpos同向
			//vt不变
			cvflag = 0;//无匀速过程
		}
		else//减速到0再加速无法达到期望速度
		{
			trackSpeedPss = sqrt(2*lenPos2*trackAcc*trackAccEnd/(trackAcc+trackAccEnd));//重设期望速度
			if(vctPos < 0)trackSpeedPss = -trackSpeedPss;//vt与vpos同向
			cvflag = 0;//无匀速过程
		}
	}
	/**************结束**********************************************************/
	
	if(trackSpeedPss>0)softAcc = trackAcc;//加速度方向与期望速度方向相同
	else softAcc = -trackAcc;
	if(trackSpeedPss>0)softAccEnd = trackAccEnd;//加速度方向与期望速度方向相同
	else softAccEnd = -trackAccEnd;
}


/******************************************************************************************************************************/
/******************************************************************************************************************************/
/******************************************************************************************************************************/

void Motor_Digital_Track()
{
	static uint8_t cnt=0;
	switch (step)
	{
	case 0:/**速度向vt靠近*/
		cnt=0;
		if(i32_abs(softSpeed - trackSpeedPss) <= trackAcc) //回环判定
		{
			softSpeed = trackSpeedPss;
			if(cvflag==0)step=2;//无匀速过程
			else step = 1;//有匀速过程
		}				
		else if(softSpeed > trackSpeedPss)
			softSpeed -= trackAcc; 
		else if(softSpeed < trackSpeedPss)
			softSpeed += trackAcc; 
		break;
	case 1://匀速
		if(i32_abs(softPos - trackPosEnd) <= tx)
		{
			step=2;
		}	
		break;
	case 2:/**速度向acce靠近*/
		if(i32_abs(softSpeed - softAcc) <= trackAccEnd)//回环判定,速度最小为2acc
		{
			softSpeed = softAcc,step=3;
		}
		else if(softSpeed > softAcc)
			softSpeed -= trackAccEnd; 
		else if(softSpeed < softAcc)
			softSpeed += trackAccEnd; 			
		break;
	}
	/**位置向终点靠近*/
	int32_t absSpeed=i32_abs(softSpeed);
	if(step==3)
	{
		if(cnt<3)cnt++;	
		else 
			softPos = trackPosEnd;	
	}

	if(i32_abs(trackPosEnd - softPos) <= absSpeed)//回环判定,
	{
		softPos = trackPosEnd;
		softSpeed = 0;
		step=4;
		trackPoint_Finish = 1;
	}		
	else 
		softPos += softSpeed;

}




















