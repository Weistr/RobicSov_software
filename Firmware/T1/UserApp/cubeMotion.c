#include "cubeMotion.h"
#include "bsp_uart.h"
#include "usart.h"
#include "bsp_led.h"
#include "XdriveCom.h"
#include "motionPlanter.h"
#include <string.h>
#include "zdt_motorCom.h"


/******************************************************************************************************************************/
/******************************************************************************************************************************/
/******************************************************************************************************************************/

// 手腕参数
#if(wrist_motor_type == xdrive_motor)
roboWristTypedef roboWrist[2] =
    {
        // 电机id  rstPos    空转速度  加速度  减速度  换面速度  加速度  减速度  转面速度  加速度  减速度    status     posNow(deg)
        {  1,      50482,     10000,     450,     30,      8000,    200,   20,    10000,     200,     20,      defaultSta,     0 ,     0},  // Lw左腕
        {  0,      47000,     10000,     450,     30,      8000,    200,   20,    10000,     200,     20,      defaultSta,     0,      0} // Rw腕
};
#endif
#if(wrist_motor_type == zdt_motor)
roboWristTypedef roboWrist[2] =
			{
			    /*电机id  rstPos    空转速度  加速度  减速度  换面速度  加速度  减速度  转面速度  加速度  减速度    status     posNow(deg)
        {  3,      64163,     10000,    500,    400,    10000,    500,    400,    10000,    500,    400,      defaultSta,     0 ,     0},  // Lw左腕
        {  2,      3262,      10000,    500,    400,    10000,    500,    400,    10000,    500,    400,      defaultSta,     0,      0} // Rw腕
*/
				//
         //电机id  rstPos    空转速度  加速度  减速度  换面速度  加速度  减速度  转面速度  加速度  减速度    status     posNow(deg)
        {  3,      64163,     30000,    10000,   8000, 30000,   5200,  4800,    30000,   10000,    9000,      defaultSta,     0 ,     0},  // Lw左腕
        {  2,      3262,      30000,    10000,   8000, 30000,   5200,  4800,    30000,   10000,    9000,      defaultSta,     0,      0} // Rw腕

		};
#endif
// 手爪参数
roboGripperTypedef roboGripper[2] =
    {
        // djid  rstPos  g_openPos  g_closeCurrent      status
        {  1,    23553,  34220,      -2000,               defaultSta,  0,  0}, // Lg
        {  4,    26997,  37828,     -2000,               defaultSta,  0,  0} // Rg
};	
#define minicurrent  800

#define roboGripper0_close_pos 22677
#define roboGripper1_close_pos 26234

/**指令**/
//首字母L,R代表左右
//第二个字母代表机械部件
//第三个代表指令编号

//LG0: 左夹爪复位
//LG1: 左夹爪闭合禁止长时间夹
//LG2: 左夹爪open
//LG3: 左夹爪轻轻闭合（小电流闭合）
//
//LW0: 左腕90度（面向电机逆时针为正）
//LW1: 左腕-90度
//LW2: 左腕180
//LW3: 左腕-180
//LW4 类推+90或-90
/***************************************************************************/
/**********************复位,初始化****************************************/
/***************************************************************************/

/**
 * @brief 初始化机器
*/
void roboInit()
{
	LED0_ON();

	for(uint8_t j=0;j<3;j++)
	{
		for(uint8_t i=0;i<4;i++)
		{
			if(i<2)//xdrive
			{
				do
				{
					if(i==0)
					motorRcvStatusUpdate(4);
					else
						motorRcvStatusUpdate(i);
					HAL_Delay(100);
				}while(xdRcvFinsh_Falg == 0);
				xdRcvFinsh_Falg = 0;
			}
			else//zdt
			{
				uint8_t LR=0;
				if(i == zdtMotor[0].motorid)LR=0;
				else if(i == zdtMotor[1].motorid)LR=1;
				do
				{
					zdt_readEncoderVal(i);
					HAL_Delay(100);
				}while(zdtMotor[LR].cmdstatus != 0x02);				
			}
		}
	}
	zdt_zeroPosTrig(2);
	HAL_Delay(20);
	zdt_zeroPosTrig(3);
	HAL_Delay(20);
	/*
  if(i32_abs(roboWrist[0].rstPos - roboWrist[0].posNow) > (roboWrist[0].posNow - (roboWrist[0].rstPos-51200)))
		roboWrist[0].rstPos-=51200;
  if(i32_abs(roboWrist[1].rstPos - roboWrist[1].posNow) > (roboWrist[1].posNow - (roboWrist[1].rstPos-51200)))
		roboWrist[1].rstPos-=51200;
  if(i32_abs(roboGripper[0].rstPos - roboGripper[0].posNow) > (roboGripper[0].posNow - (roboGripper[0].rstPos-51200)))
		roboGripper[0].rstPos-=51200;
  if(i32_abs(roboGripper[1].rstPos - roboGripper[1].posNow) > (roboGripper[1].posNow - (roboGripper[1].rstPos-51200)))
		roboGripper[1].rstPos-=51200;
	
*/
	/*
	int32_t posL = roboWrist[0].posNow;//左腕电机位置
	int32_t posR = roboWrist[1].posNow;//右腕电机位置
	int32_t errorL = (posL-roboWrist[0].rstPos)%25600;
	int32_t errorR = (posR-roboWrist[1].rstPos)%25600;//180的余数
	int32_t absErrorL,absErrorR;
	if(errorL<0)absErrorL=-errorL;
	else absErrorL = errorL;
	if(errorR<0)absErrorR=-errorR;
	else absErrorR = errorR;
	*/
	


		memset(actionSerialStr,0,actionStrLenMax);
		memcpy(actionSerialStr,"LW0RW0LG0RG0",12);
		serialActionStart();


	//roboWrist[0].posNow = roboWrist[0].rstPos;
	//roboWrist[1].posNow = roboWrist[1].rstPos;	
		//memset(actionSerialStr,0,actionStrLenMax);
		//memcpy(actionSerialStr,"RW0LW0LG3RG3",12);
		//serialActionStart();
	
}






/******************************************************************************************************************************/
/****************************动作串模式**************************************************************************************************/
/******************************************************************************************************************************/
//监测是否有冲突步骤，同时为90度
uint8_t serialConfict_Test(char* strin,uint16_t strlen,uint8_t LGpresta,uint8_t RGpresta,uint8_t LWpresta,uint8_t RWpresta)
{

	uint8_t retVal = 0x00;
	uint8_t LWsta,RWsta,LGsta,RGsta;
		uint8_t roboActivedPart = 0;	
	
	for (uint16_t i = 0; i < strlen; i+=3)
	{
		//字符串格式检查
		if((strin[i]!= 'L')&&(strin[i]!= 'R'))
			return serialAction_checkCode_error_illgelChar;//首字母不为LR
		if((strin[i+1]!= 'W')&&(strin[i+1]!= 'G'))
			return serialAction_checkCode_error_illgelChar;//2字母不为WG
		if((strin[i+2]< '0')||(strin[i+2]> '6'))
			return serialAction_checkCode_error_illgelChar;//3不为数字或超范围
		
		

		
		//状态赋值
		if(strin[i]=='L')
			if(strin[i+1]=='G')
			{
				roboActivedPart = 0;
				__nop();
				LGsta = strin[i+2];
				if(LGsta == LGpresta)
				{
					retVal = serialAction_checkCode_OK;
					LGpresta = LGsta;
				}
					
			}
			
			
		if(strin[i]=='R')
			if(strin[i+1]=='G')
			{
				roboActivedPart = 1;
				RGsta = strin[i+2];
				if(RGsta == RGpresta)
				{
					retVal = serialAction_checkCode_warning_sameRcv;
					RGpresta = RGsta;
				}	
			}
		if(strin[i]=='L')
			if(strin[i+1]=='W')
			{
				roboActivedPart = 2;
				LWsta = strin[i+2];
				if(LWsta == LWpresta)
				{
					retVal = serialAction_checkCode_warning_sameRcv;
					LWpresta = LWsta;
				}
					
			}
		if(strin[i]=='R')
			if(strin[i+1]=='W')
			{
				roboActivedPart = 3;
				RWsta = strin[i+2];
				if(RWsta == RWpresta)
				{
					retVal = serialAction_checkCode_warning_sameRcv;
					RWpresta = RWsta;
				}
			}

			
		//90度冲突检查
		if(
			(((LWsta=='1')||(LWsta=='2')||(LWsta=='5')||(LWsta=='6')) && (roboActivedPart == 3))||//左爪不水平右腕转
			(((RWsta=='1')||(RWsta=='2')||(RWsta=='5')||(RWsta=='6')) && (roboActivedPart == 2))//右爪不水平左腕转
			)
		{
			__nop();
				return serialAction_checkCode_error_90degCof;
			
		}


		//两夹爪同时张开
		if((LGsta == '2')&&(RGsta == '2'))
			return serialAction_checkCode_error_open2Gri;	
				
		//没夹就转
		/*
		if(
			((LGsta != '1')&&(roboActivedPart == 2)) || 
			((RGsta != '1')&&(roboActivedPart == 3))
			)
			return serialAction_checkCode_error_enptyRotate;*/
		
	}
	return retVal;
}



/**
 * @brief 动作串
*/
char actionSerialStr[actionStrLenMax];

uint8_t trackFinish = 0;//轨迹触发完成
uint8_t trigFinish=0;//轨迹点生成完成
uint8_t motArrive=0;//电机到达位置
uint8_t motormod=0xFF;
int32_t golPos;
uint16_t cubeStrStep = 0,cubeStrStepCord = 0;

uint8_t serialActionStartFlag = 0;
void serialActionStart()//任务启动
{
	serialActionStartFlag = 1;
	trackFinish = 1;
	LED_MODE = LED0blinkWithCycle;
}
uint8_t partId,opsPartId;
uint8_t miniCurrFlag = 0;

void serialActionTask()
{
	static uint8_t zdt_send_finish = 0;
	int8_t golSta=0;
	if((actionSerialStr[cubeStrStep] ==0) && (serialActionStartFlag == 1))//动作串完成
	{
		cubeStrStepCord = cubeStrStep;
		cubeStrStep=0;
		serialActionStartFlag = 0;
		LED_MODE = LED0constON;
		uartWiteDataToBuffer((uint8_t*)"\r\nserial action finish!",23);
		uartTrigSendStr();
	}	
	if(serialActionStartFlag == 1)//任务启动
	{
		//轨迹触发
		if(trackFinish == 1)//触发条件是，轨迹生成完成
		{
			trackFinish = 0;
			trackPoint_Finish = 0;
			if (actionSerialStr[cubeStrStep]=='L')
			{
				partId = 0;
				opsPartId = 1;
			}			
			else if(actionSerialStr[cubeStrStep]=='R')
			{
				partId = 1;
				opsPartId = 0;
			}		

			//指令解析					
			if(actionSerialStr[cubeStrStep+1]=='G')//手爪
			{
				switch (actionSerialStr[cubeStrStep+2])
				{
				case '2'://夹爪开	
					golPos = roboGripper[partId].g_openPos;
					motormod = 0;//固定位置						
					break;
				case '1'://夹爪闭
					miniCurrFlag = 0;
					golPos = roboGripper[partId].rstPos;//其实无所谓
					motormod = 1;//电流模式						
					break;	
				
				case '3'://夹爪闭小电流
					miniCurrFlag = 1;
					golPos = roboGripper[partId].rstPos;//其实无所谓
					motormod = 1;//电流模式						
					break;	
				
				case '0'://夹爪复位
					golPos = roboGripper[partId].rstPos;
					motormod = 0;//固定位置						
					break;											

				}							
				trigFinish = 1;
			}
			
			else if(actionSerialStr[cubeStrStep+1]=='W')//手腕
			{
				/*绝对位置模式*/
				motormod = 2;
				golSta=actionSerialStr[cubeStrStep+2]-'0';
				
				
				//xdrive 电机
				#if(wrist_motor_type == xdrive_motor)
				if (golSta==0)
				{
					golPos = roboWrist[partId].rstPos;
					//roboWrist[partId].posNow = 0;
				}
				else if(golSta%2!=0)
				{
					golPos = (golSta/2+1)*12800 + roboWrist[partId].rstPos;
					//roboWrist[partId].posNow = (posn/2+1)*90;
				}
				else
				{
					golPos = -golSta/2*12800 + roboWrist[partId].rstPos;
					//roboWrist[partId].posNow = -posn/2*90;
				}
				#endif	
				
				
				
				//zdt电机
				#if(wrist_motor_type == zdt_motor)
				if (golSta==0)
				{
					golPos = 0;
					//roboWrist[partId].posNow = 0;
				}
				else if(golSta%2!=0)
				{
					golPos = (golSta/2+1)*900;
					//roboWrist[partId].posNow = (posn/2+1)*90;
				}
				else
				{
					golPos = -golSta/2*900;
					//roboWrist[partId].posNow = -posn/2*90;
				}
				#endif			
			}
			

			uint8_t idchoice=0;
			if(((roboGripper[partId].status) == g_close) && ((roboGripper[opsPartId].status) == g_open))//换面
				idchoice = 1;
			else if(((roboGripper[partId].status) == g_open) && ((roboGripper[opsPartId].status) == g_close))//空转
				idchoice = 0;
			else if(((roboGripper[partId].status) == g_close) && ((roboGripper[opsPartId].status) == g_close))//转面
				idchoice = 2;
			else
			{
				idchoice = 0;//换面最慢
				//uartPrintString(&huart1,"\r\nGripper status error!");
				//goto errorHandler;
			}
			softPos = roboWrist[partId].posNow;
			trackAcc = roboWrist[partId].motion[idchoice].acc;
			trackAccEnd = roboWrist[partId].motion[idchoice].accEnd;
			trackSpeedPss = roboWrist[partId].motion[idchoice].speedPss;
			trackPosEnd = golPos;
			#if(wrist_motor_type == xdrive_motor)
			trackTriger();
			#endif
			#if(wrist_motor_type == zdt_motor)
	
			#endif
			trigFinish = 1;	
		}//轨迹触发END
		//轨迹生成
		#define speedErrorMin 2000
		#define robo_gripper_open_stabled_cnt5ms_n 2
		
		#define robo_preDelay_cnt5ms_n 2
		#define perroMin 500
		#define gripper_clap_stabled_cnt5ms_n 6
		#define gripper_speedErrorMin 2000
		if(trigFinish == 1)//轨迹生成条件是，触发完成
		{
			static uint8_t robo_stabled_cnt=0,robo_preDelay_cnt=0;		
			int32_t perro=0,speedRcv=0;
			switch (motormod)
			{
				case 0://夹爪张开，复位		
					/**持续发送直到位置到达*/
					motorPosControl(roboGripper[partId].motorid,golPos,0);	
					perro = XdPosRcv - golPos;
					if (perro < 0)perro = -perro;
					speedRcv = XdSpeedRcv;
					if (speedRcv < 0)speedRcv = -speedRcv;	
					if (perro < perroMin)
					{
						//if (speedRcv < speedErrorMin)
						{			
							robo_stabled_cnt++;
							if(robo_stabled_cnt > robo_gripper_open_stabled_cnt5ms_n)
							{
								robo_stabled_cnt=0;
								trackFinish = 1;
								trigFinish = 0;
								cubeStrStep+=3;
								if(golPos == roboGripper[partId].rstPos)
								roboGripper[partId].status = g_rst;
								if(golPos == roboGripper[partId].g_openPos)
								roboGripper[partId].status = g_open;
								break;
							}
						}
						
					}else robo_stabled_cnt=0;

					
					break;
				case 1://夹爪闭合
					/**持续发送直到位置到达*/
					speedRcv = XdSpeedRcv;
					if (speedRcv < 0)speedRcv = -speedRcv;	
				motorCurrControl(roboGripper[partId].motorid,roboGripper[partId].g_closeCurrent);
				
				
					if(miniCurrFlag == 1)
					{
						if(roboGripper[partId].g_closeCurrent < 0)
							motorCurrControl(roboGripper[partId].motorid,-minicurrent);
						else
							motorCurrControl(roboGripper[partId].motorid,minicurrent);
					}
					else
					{
						motorCurrControl(roboGripper[partId].motorid,roboGripper[partId].g_closeCurrent);
					}
					
					if(robo_preDelay_cnt > robo_preDelay_cnt5ms_n)
					{
						int32_t gpos;
						if(partId==0)gpos = roboGripper0_close_pos;
						else if(partId==1)gpos = roboGripper1_close_pos;
						
						if(miniCurrFlag == 1)gpos += 300;
						if (XdPosRcv < gpos)
						{
							//if (speedRcv < gripper_speedErrorMin)
							{			
								robo_stabled_cnt++;
								if(robo_stabled_cnt > gripper_clap_stabled_cnt5ms_n)
								{
									robo_stabled_cnt=0;
									robo_preDelay_cnt = 0;
									trackFinish = 1;
									trigFinish = 0;
									cubeStrStep+=3;	
									roboGripper[partId].status = g_close;
									break;
								}
							}
							
						}else robo_stabled_cnt=0;
					}
					robo_preDelay_cnt++;

					break;	
				case 2://手腕转动

					//xdrive电机
					#if(wrist_motor_type == xdrive_motor)
					Motor_Digital_Track();
					motorPosControl(roboWrist[partId].motorid,softPos,0);					
					if(trackPoint_Finish==1)
					{
						perro = XdPosRcv - golPos;
						if (perro < 0)perro = -perro;
						speedRcv = XdSpeedRcv;
						if (speedRcv < 0)speedRcv = -speedRcv;	
						if (perro < perroMin)
						{
							if (speedRcv < speedErrorMin)
							{			
								robo_stabled_cnt++;
								if(robo_stabled_cnt > robo_stabled_cnt5ms_n)
								{
									robo_stabled_cnt=0;
									trackFinish = 1;
									trigFinish = 0;
									roboWrist[partId].status = golSta;
									cubeStrStep+=3;	
									break;
								}
							}
							else robo_stabled_cnt=0;
						}	
					}
					#endif


					//zdt电机
					#define zdtPosErrMin 15 //1度
					#define zdtSpeedErrMin 60
					#define wrist_stabled_cnt5ms_n 5
					#if(wrist_motor_type == zdt_motor)
					
					if(zdt_send_finish == 1)//数据发出去了
					{
						static uint8_t cnt = 0;
						if(cnt < 5)
						{
							cnt++;
						}
						else//数据发出5*5ms以后
						{
							if(zdtMotor[partId].cmdstatus == 0x02)//数据发送成功
							{
								if((i32_abs(zdtMotor[partId].pos - golPos) < zdtPosErrMin)&&(zdtMotor[partId].perr_rcvd_flag == 1))//位置在误差范围内
								{
									zdtMotor[partId].perr_rcvd_flag = 0;//收到数据标志位清0
									//if((zdtMotor[partId].speedAbs < zdtSpeedErrMin)&&(zdtMotor[partId].spderr_rcvd_flag == 1))//速度在误差范围内
									{
										zdtMotor[partId].spderr_rcvd_flag = 0;//收到数据标志位清0
										robo_stabled_cnt++;
										if(robo_stabled_cnt > wrist_stabled_cnt5ms_n)
										{
											cnt=0;
											zdt_send_finish = 0;
											robo_stabled_cnt=0;
											trackFinish = 1;
											trigFinish = 0;
											roboWrist[partId].status = golSta;
											cubeStrStep+=3;	
											break;
										}
									}
									zdt_readSpeed(zdtMotor[partId].motorid);//读取速度误差
								}
								else
								{
									zdt_readPos(zdtMotor[partId].motorid);//读取位置误差
								}
								
							}
							//数据发送成功END

							else//数据没发送成功
							{
								zdt_send_finish = 0;
								cnt = 0;	
							}
							//数据没发送成功END
						}
						//5*5ms END
					}
					if (zdt_send_finish == 0)//数据没发出去
					{
						zdt_motorTrackCtl(roboWrist[partId].motorid,golPos,trackAcc,trackAccEnd,trackSpeedPss);
						zdt_send_finish = 1;
						
					}
					
					#endif
					break;
				
			}//switch END
		}//轨迹生成END
	}//mod选择end

}

#define posnMax 3
#define posnMin -3
//0:正转，1:反转，2:180度，3:水平 4：复位
char ralativeToAbs_action(char in)
{
	static int8_t absPos = 0;
	switch (in)
	{
	case w_cw90:
		if(absPos == posnMax)
			absPos -= 3;
		else 
			absPos += 1;
		break;
	case w_ccw90:
		if(absPos == posnMin)
			absPos += 3;
		else 
			absPos -= 1;
		break;
	case w_r180:
		if (absPos > 0)
			absPos -= 2;
		else 
			absPos += 2;
		break;
	case w_horizon:
		if((absPos!=0)&&(absPos%2 != 0))//当前夹爪不水平
		{
			if(absPos > 0)
			absPos -= 1;
			else
			absPos += 1;
		}
		break;
	case w_rst:
		absPos = 0;
		break;
	}
	char retval;
	switch (absPos)
	{
	case 0:
		retval = 0;
		break;
	case 1:
		retval = 1;
		break;
	case -1:
		retval = 2;
		break;
	case 2:
		retval = 3;
		break;
	case -2:
		retval = 4;
		break;
	case 3:
		retval = 5;
		break;
	case -3:
		retval = 6;
		break;
	case 4:
		retval = 7;
		break;
	case -4:
		retval = 8;
		break;
	}
	return (retval+'0');
}
/***************************************************************************/
/**********************魔方面状态****************************************/
/***************************************************************************/

//const char faces_default[6]={'U','D','L','R','F','B'};//默认面
//char faces_now[6];//当前面
/*
void cubeFacesRst()//将当前面设为默认
{
    for(uint8_t i=0;i<6;i++)faces_now[i]=(char)faces_default[i];
}*/
/**
 * @brief 更新魔方面状态
 * @param cord 坐标轴 0,x 1,y
 * @param rotate 旋转次数,90度为1次，右手螺旋
*/
/*
void cubeFaceUpdate(uint8_t cord,int8_t rotate)
{
    char tmp;
    #define U 0
    #define D 1
    #define L 2
    #define R 3
    #define F 4
    #define B 5
    //x=F R B L    
    if(cord == 0)//绕x轴旋转
    {
        if(rotate > 0)
        {
            for (uint8_t i = 0; i < rotate; i++)
            {
                tmp = faces_now[L];
                faces_now[L]=faces_now[B];
                faces_now[B]=faces_now[R];
                faces_now[R]=faces_now[F];
                faces_now[F]=tmp;
            }
        }
        else if(rotate < 0)
        {
            for (uint8_t i = 0; i < -rotate; i++)
            {
                tmp = faces_now[F];
                faces_now[F]=faces_now[R];
                faces_now[R]=faces_now[B];
                faces_now[B]=faces_now[L];
                faces_now[L]=tmp;
            }            
        }
    }
    else if(cord==1)//绕y轴旋转 y=F D B U
    {
        if(rotate > 0)
        {
            for (uint8_t i = 0; i < rotate; i++)
            {
                tmp = faces_now[U];
                faces_now[U]=faces_now[B];
                faces_now[B]=faces_now[D];
                faces_now[D]=faces_now[F];
                faces_now[F]=tmp;
            }
        }
        else if(rotate < 0)
        {
            for (uint8_t i = 0; i < -rotate; i++)
            {
                tmp = faces_now[F];
                faces_now[F]=faces_now[D];
                faces_now[D]=faces_now[B];
                faces_now[B]=faces_now[U];
                faces_now[U]=tmp;
            }            
        }        
    }
}*/
/***************************************************************************/
/**********************夹爪和臂动作控制**************************************/
/***************************************************************************/


/**
 * @param part 部件，Lg,Rg,Lw Rw
 * @param action 当部件为夹爪时，取g_close g_open rst，手腕时见宏定义
 * @retval 机器累计转的步 可直接读取 roboStepsSum;
*/

uint8_t roboStepsSum=0;
uint16_t actCnt=0;
uint8_t roboActionAdd(char* act)
{
	static char previous_act[3];
	
	if(memcmp(previous_act,act,3)!=0)//防止重复步骤
	{

		actionSerialStr[actCnt] = act[0];
		actionSerialStr[actCnt+1] = act[1];
		if(act[1]=='W')
			actionSerialStr[actCnt+2] = ralativeToAbs_action(act[2]);
		else actionSerialStr[actCnt+2] = act[2];
		actCnt+=3;
		roboStepsSum++;
	}
	memcpy(previous_act,act,3);
	return 0;
}



/***************************************************************************/
/**********************魔方转面****************************************/
/***************************************************************************/

/**
 * @brief 转动魔方的一个面，相对坐标系
 * @param cubeFace 要转的面，顺时针为负，右手螺旋，正面F,左上U。x轴垂直U面向外，y轴垂直R面向外
 * @param rotate cw90 ccw90 r180 
 * @retval 魔方坐标系转动情况 见宏定义
*/

int8_t cubeSerialRotateFace(char* rotateStr)
{
	static uint8_t rotateStrCnt=0;
	char bufStr[3];
	if(rotateStr[rotateStrCnt+1]==' ')//顺转90
	bufStr[2] = ralativeToAbs_action(w_cw90);
	else if(rotateStr[rotateStrCnt+1]=='\'')
	bufStr[2] = ralativeToAbs_action(w_ccw90);
	else if(rotateStr[rotateStrCnt+1]=='2')
	bufStr[2] = ralativeToAbs_action(w_r180);

	switch (rotateStr[rotateStrCnt])
	{
	case 'U'://左换右转
		roboActionAdd("LG1");//左爪闭
		roboActionAdd("RG2");//右爪开
		roboActionAdd("RW3");//右腕水平
		roboActionAdd("LW2");//左腕换面
		roboActionAdd("RG1");
		bufStr[0] = 'R';
		bufStr[1] = 'W';
		roboActionAdd(bufStr);
		break;
	
	default:
		break;
	}
	return 0;
}

