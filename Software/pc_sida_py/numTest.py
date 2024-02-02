
motionResult = ['RW0RG1LW0RG2LW4RG1RW4LG2RW6LG1RG2RW4RG1LW6LG2LW4LG1LW1RW0LW2LG2LW1LG1RW4RG0LG0', 'E6', '0D']

def calculate_crc16(pmotionResult):  # CRC校验
    # sarray=发送数组
    data = pmotionResult[0]
    crc = 0xFFFF
    for char in data:
        crc ^= ord(char)
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    # 计算校验值并输出结果
    crc = hex(crc)[2:].zfill(4).upper()
    pmotionResult[1] += crc[2]+crc[3]
    pmotionResult[2] += crc[0]+crc[1]

    #print("CRC16校验值为:", crc)
    #print(motionResult)

    array = []
    for j in range(len(pmotionResult)):
        if j == 0:
            for i in range(len(pmotionResult[j])):
                array.append(int(hex(ord(pmotionResult[j][i]))[2:], 16))
        else:
            array.append(int(pmotionResult[j], 16))
    return array

rstmotion=[]
sta2 = []
flag2=0
cnt=0
for i in range(int(len(motionResult[0])/3)):
    if i==0 :
        sta1 = motionResult[0][-3:]
    else:
        sta1 = motionResult[0][-3-i*3:-i*3]
    if(sta1[1]=='W'):
        cnt += 1
        sta2 += sta1
        if(cnt == 2):
            break

print('--last sta---')
print(sta2)  
if sta2[2]=='0' and sta2[5]=='0':
    print("无需复位手爪")
elif sta2[2]=='0':
    rstmotion += sta2[3]
    rstmotion += 'W'
    rstmotion += '0'
elif sta2[5]=='0':
    rstmotion += sta2[0]
    rstmotion += 'W'
    rstmotion += '0'
elif (int(sta2[2])%2 != 0) :
    rstmotion += sta2[0]
    rstmotion += 'W'
    rstmotion += '0'
    rstmotion += sta2[3]
    rstmotion += 'W'
    rstmotion += '0'
elif (int(sta2[5])%2 != 0) :
    rstmotion += sta2[3]
    rstmotion += 'W'
    rstmotion += '0'
    rstmotion += sta2[0]
    rstmotion += 'W'
    rstmotion += '0'
else :
    rstmotion = 'LW0RW0'
rstmotion = ''.join(rstmotion)
print('--motion---')
print(rstmotion)  
rstmotion = calculate_crc16([rstmotion,"",""])