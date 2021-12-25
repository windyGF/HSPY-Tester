# -*- coding: utf_8 -*-
import serial
import time
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu


def mod(com="com12", addr=0, valnum=1):
    red = []
    alarm = ""
    try:
        # 设定串口为从站
        master = modbus_rtu.RtuMaster(serial.Serial(port=com,
                                                    baudrate=9600, bytesize=8, parity='N', stopbits=1))
        master.set_timeout(5.0)
        master.set_verbose(True)

        # 读保持寄存器
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 0, 1, 500)  # 设置电压
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, 1, 1000)  # 设置电流
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 6, 1, 1)  # 设置按键锁定
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 4, 1, 1)  # 设置电源开启
        time.sleep(4)

        red = master.execute(1, cst.READ_HOLDING_REGISTERS, addr, valnum)  # 这里可以修改需要读取的功能码
        print(red)
        alarm = "正常"
        return list(red), alarm

    except Exception as exc:
        print(str(exc))
        alarm = (str(exc))

    return red, alarm  # 如果异常就返回[],故障信息


if __name__ == "__main__":
    mod("com12", 2, 2)
