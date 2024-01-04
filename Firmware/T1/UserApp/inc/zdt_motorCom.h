#ifndef _ZDT_COM_H
#define _ZDT_COM_H
#include "user_main.h"

void zdt_motorEnanleCtl(uint8_t id,uint8_t choice);
void zdt_motorTrackCtl(uint8_t id, int32_t pos,int16_t acc_P,int16_t acc_N,int16_t spdpss);
void zdt_uartRcv(void);
void zdt_zeroPosTrig(uint8_t id);
void zdt_zeroPosSet(uint8_t id,uint8_t save);
void zdt_readPos(uint8_t id);
void zdt_readPosError(uint8_t id);
void zdt_readEncoderVal(uint8_t id);
void zdt_readSpeed(uint8_t id);


#define zdt_enable 1
#define zdt_disable 0
#define zdt_parmSave 1
#define zdt_parmNotSave 0


typedef struct
{
	uint8_t motorid;    
	uint16_t rstPos;
	uint16_t EncoderVal;
	int16_t speed;
	int16_t speedAbs;
	int32_t pos;
	int32_t posError;
	int32_t posErrorAbs;
	uint8_t cmdstatus;//E2:err  02: ok
	uint8_t perr_rcvd_flag;
	uint8_t spderr_rcvd_flag;
}zdtMotorTypedef;
extern zdtMotorTypedef zdtMotor[];
#endif
