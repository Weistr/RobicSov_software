XdriceCom_x86_64: main.o usbCom.o xdriveCom.o crc16modbus.o  
	gcc -o $^
%.o : %.c
	gcc -c -o $@ $<

clean:
	rm *.o 