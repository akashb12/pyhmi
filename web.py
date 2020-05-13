from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient as Modbusserialclient
import tkinter as tk
import tkinter.messagebox
import pyodbc
from datetime import datetime
# import matplotlib as mpl
# mpl.use('agg')
import numpy
import matplotlib.pyplot as plt
import pandas as pd
from PIL import ImageTk,Image



# this is for creating window and geometry is applied to window(main window)
window=tk.Tk()
window.title("PYHMI")
window.geometry("500x500")
window.config(background='black')
window.maxsize(500,500)

# current date and time is displayed on screen
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S ')
clock=tk.Label(window,text=formatted_date)
clock.pack(side='right',anchor='se')


# canvas1=tk.Canvas(window,width=100,height=50).pack()
# c = ModbusClient(host='localhost', port=9999, auto_open=True,debug=True)
def win5():
    #this window is for modbustcp connection
    window5 = tk.Tk()
    window5.title("MODBUS TCP/IP")
    window5.geometry("400x400")
    window5.config(background="black")
    window5.maxsize(400, 400)
    clock5 = tk.Label(window5, text=formatted_date)
    clock5.pack(side='right', anchor='se')

    # this is for tcpip connection
    # en.get is used to take the entry from entryform
    def connecttcp():
        global client
        client = ModbusTcpClient(host=en.get(), port=en1.get())
        connection = client.connect()
        print(type(client))
    #this labels,entry,buttons are used for tcp/ip connection
    # label50 = tk.Label(window, text="Select Type Of Communication", font=("Ariel Bold", 15), bg='yellow')
    modbustcp = tk.Label(window5, text="   MODBUSTCP/IP    ", font=("Ariel Bold", 20),width=25,bg='blue')
    modbustcp.place(x=0,y=0)
    ipaddr = tk.Label(window5, text=" Enter IP Address   ", font=("Ariel Bold", 15) )
    ipaddr.place(x=110,y=40)
    # this is the entry form where we will insert ip address
    en = tk.Entry(window5, text=1)
    en.place(x=140,y=70)
    portnolb = tk.Label(window5, text=" Enter Port Number ", font=("Ariel Bold", 15) )
    portnolb.place(x=110,y=90)
    en1 = tk.Entry(window5, text=2)
    en1.place(x=140,y=120)
    # when this button is pressed it will call connecttcp method
    but5 = tk.Button(window5, text="connect", font=("Ariel Bold", 10) , command=connecttcp)
    but5.place(x=170,y=140)

def win6():
    window6 = tk.Tk()
    window6.title("MODBUS ASCII")
    window6.geometry("400x400")
    window6.config(background="black")
    window6.maxsize(400, 400)
    clock6 = tk.Label(window6, text=formatted_date)
    clock6.pack(side='right', anchor='se')
    # this method is for ascii communication

    def modbusascii():
        client = Modbusserialclient(method=methoden.get(), port=asciiporten.get(), baudrate=baudrateen.get(), timeout=3, parity=pairityen.get(), stopbits=1,
                                    bytesize=8)
        connection = client.connect()

    asciilb = tk.Label(window6, text="   MODBUS ASCII    ", font=("Ariel Bold", 20),width=25,bg='blue' )
    asciilb.place(x=0,y=0)
    methodlb = tk.Label(window6, text=" Enter Method    ", font=("Ariel Bold", 15)  )
    methodlb.place(x=110,y=40)
    methoden = tk.Entry(window6, text=100)
    methoden.place(x=125,y=70)
    asciiportlb = tk.Label(window6, text="     Enter Port     ",font=("Ariel Bold", 15) )
    asciiportlb.place(x=110,y=90)
    asciiporten = tk.Entry(window6, text=101)
    asciiporten.place(x=125,y=120)
    baudratelb = tk.Label(window6, text=" Enter BaudRate ",font=("Ariel Bold", 15)  )
    baudratelb.place(x=110,y=140)
    baudrateen = tk.Entry(window6, text=3)
    baudrateen.place(x=130,y=170)
    pairitylb = tk.Label(window6, text="     Enter Parity    ",font=("Ariel Bold", 15) )
    pairitylb.place(x=110,y=190)
    pairityen = tk.Entry(window6, text=3)
    pairityen.place(x=130,y=220)
    asciibut = tk.Button(window6, text="connect",font=("Ariel Bold", 10), command=modbusascii)
    asciibut.place(x=160,y=240)

# creating windows

def win2():


   # creating window 2
   window2=tk.Tk()
   window2.title("counter read and reset")
   window2.geometry("700x1800")
   window2.config(background="black")
   window2.maxsize(700, 1800)
   clock1 = tk.Label(window2, text=formatted_date)
   clock1.pack(side='right', anchor='se')

   # counter read code
   def read():

      # insert ip address,number of registers to read and unit id
      reg = client.read_holding_registers(address=int(addressr.get()),count= int(countr.get()), unit=int(unitr.get()))
      regs1=reg.registers[0]


      print("reading register values")
      if regs1:
         print(regs1)
      else:
         print("error")
      #when label has text=regs1 means  it will display regs1 value
      resultlb.config(text=regs1)
      valueinreglb = tk.Label(frame1, text="value in register", font=("Ariel Bold", 10), width=19)
      valueinreglb.place(x=0, y=103)

      # CONNECTION WITH SQL SERVER
      # connection string
      # this is used as a connectionstring to connect with sql server


      conn =pyodbc.connect("Driver={"+str(driver.get())+"};Server="+str(server.get())+";Database="+str(database.get())+";Trusted_Connection="+str(trust.get())+";")
      # connection start
      cursor = conn.cursor()

      cursor.execute('insert into '+str(table.get())+'('+str(xen.get())+','+str(yen.get())+') values(?,?)',
                     (formatted_date, regs1)

                     )

      conn.commit()
      conn.close()
   # for plotting graph
   # matplotlib is used for plotting graphs
   def plot():
         conn = pyodbc.connect("Driver={" + str(driver.get()) + "};Server=" + str(server.get()) + ";Database="+str(database.get()) + ";Trusted_Connection=" + str(trust.get()) + ";")
         cursor = conn.cursor()
         # 'select datetime,count  from pytb2'
         query = queryen.get()
         # pandas are used to read from sqlserver
         tm = pd.read_sql(query, conn)
         tm1 = tm.head(100)
         #datetime count
         plt.plot(tm1[xen.get()], tm1[yen.get()])
         plt.scatter(tm1[xen.get()], tm1[yen.get()])
         plt.xlabel(xenname.get(), fontsize=16)
         plt.ylabel(yenname.get(), fontsize=16)
         plt.title("REAL TIME COUNT MONITORING ", fontsize=25)
         plt.show()
   # counter reset code
   def clicked():
      client.write_register(0,0,unit=1)

      # a=int(b.get())
      print("write value to register")

      tk.messagebox.showinfo("RESET", "Reset successful Please click on Read Register")
      # label3=tk.Label(window,text="register reset successful")
      # label3.pack()
      # label4.config(text=a)
   frame1 = tk.Frame(window2, bg='blue', height=100, borderwidth=6, relief='sunken')
   frame1.place(x=200,y=0)
   readreg = tk.Label(frame1, text="Reading Registers",width=35, font=("Ariel Bold", 10),bg='green')
   readreg.pack()



   # for reading provide adress,count,unit
   modadd = tk.Label(frame1, text="Enter Modbus Address",width=40 )
   modadd.pack(anchor='nw')
   addressr = tk.Entry(frame1, text=210)
   addressr.pack(anchor='nw')
   modcount = tk.Label(frame1, text="Enter Count",width=40 )
   modcount.pack(anchor='nw')
   countr = tk.Entry(frame1, text=211)
   countr.pack(anchor='nw')
   modunit = tk.Label(frame1, text="Enter Unit",width=40  )
   modunit.pack(anchor='nw')
   unitr = tk.Entry(frame1, text=212)
   unitr.pack(anchor='nw')
   sqlserver = tk.Label(frame1, text="Enter Database Details",width=35, font=("Ariel Bold", 10),bg='green' )
   sqlserver.pack(anchor='nw')
   driverlb=tk.Label(frame1, text="Enter Driver Name",width=40 )
   driverlb.pack(anchor='nw')
   driver = tk.Entry(frame1,text=218)
   driver.pack(anchor='nw')
   serverlb = tk.Label(frame1, text="Enter Server Name",width=40)
   serverlb.pack(anchor='nw')
   server = tk.Entry(frame1,text=219)
   server.pack(anchor='nw')
   databaselb = tk.Label(frame1, text="Enter Database Name",width=40  )
   databaselb.pack(anchor='nw')
   database = tk.Entry(frame1, text=220)
   database.pack(anchor='nw')
   Tablelb = tk.Label(frame1, text="Enter Table Name",width=40  )
   Tablelb.pack(anchor='nw')
   table = tk.Entry(frame1, text=222)
   table.pack(anchor='nw')
   xlb = tk.Label(frame1, text="Enter Database column Name",width=40  )
   xlb.pack(anchor='nw')
   xen = tk.Entry(frame1, text=214)
   xen.pack(anchor='nw')
   ylb = tk.Label(frame1, text="Enter Database column Name",width=40  )
   ylb.pack(anchor='nw')
   yen = tk.Entry(frame1, text=215)
   yen.pack(anchor='nw')

   trustlb = tk.Label(frame1, text="Trusted Connection",width=40  )
   trustlb.pack(anchor='nw')
   trust= tk.Entry(frame1, text=221)
   trust.pack(anchor='nw')
   readbut = tk.Button(frame1, text="READ_REGISTERS", bg='yellow', width=30, font=("Ariel Bold", 10), command=read)
   readbut.pack()
   writebut = tk.Button(frame1, text="RESET", bg='yellow', width=30, font=("Ariel Bold", 10), command=clicked)
   writebut.pack()
   resultlb = tk.Label(frame1, text="Result", width=10, font=("Ariel Bold", 10))
   resultlb.pack(side='right', anchor='nw')

   # for plotting
   frame2 = tk.Frame(window2, bg='blue', height=100, borderwidth=6, relief='sunken')
   frame2.place(x=200,y=580)
   graphlb = tk.Label(frame2, text="Plotting Graphs",width=35, font=("Ariel Bold", 10),bg='green' )
   graphlb.pack()

   querylb = tk.Label(frame2, text="Enter Query",width=40 )
   querylb.pack(anchor='nw')
   queryen = tk.Entry(frame2, text=213)
   queryen.pack(anchor='nw')


   xlbname = tk.Label(frame2, text="Give Name For X Label",width=40 )
   xlbname.pack(anchor='nw')
   xenname = tk.Entry(frame2, text=216)
   xenname.pack(anchor='nw')
   ylbname = tk.Label(frame2, text="Give Name For Y Label",width=40 )
   ylbname.pack(anchor='nw')
   yenname = tk.Entry(frame2, text=217)
   yenname.pack(anchor='nw')
   pltbut = tk.Button(frame2, text="GENERATE GRAPHS",bg='yellow', width=30, font=("Ariel Bold", 10), command=plot)
   pltbut.pack()
def win8():


   # creating window 2
   window8=tk.Tk()
   window8.title("counter read and reset")
   window8.geometry("700x1800")
   window8.config(background="black")
   window8.maxsize(700, 1800)
   clock1 = tk.Label(window8, text=formatted_date)
   clock1.pack(side='right', anchor='se')

   # counter read code
   def reada():

      # insert ip address,number of registers to read and unit id
      rega = client.read_holding_registers(address=int(addressr1.get()),count= int(countr1.get()), unit=int(unitr1.get()))
      regsa1=rega.registers[0]


      print("reading register values")
      if regsa1:
         print(regsa1)
      else:
         print("error")
      #when label has text=regs1 means  it will display regs1 value
      resultlb1.config(text=regsa1)
      valueinreglb1 = tk.Label(frame1, text="value in register", font=("Ariel Bold", 10), width=19)
      valueinreglb1.place(x=0, y=103)

      # CONNECTION WITH SQL SERVER
      # connection string
      # this is used as a connectionstring to connect with sql server


      conn =pyodbc.connect("Driver={"+str(driver1.get())+"};Server="+str(server1.get())+";Database="+str(database1.get())+";Trusted_Connection="+str(trust1.get())+";")
      # connection start
      cursor = conn.cursor()

      cursor.execute('insert into '+str(table1.get())+'('+str(xen1.get())+','+str(yen1.get())+') values(?,?)',
                     (formatted_date, regsa1)

                     )

      conn.commit()
      conn.close()
   # for plotting graph
   # matplotlib is used for plotting graphs
   def plota():
         conn = pyodbc.connect("Driver={" + str(driver1.get()) + "};Server=" + str(server1.get()) + ";Database="+str(database1.get()) + ";Trusted_Connection=" + str(trust1.get()) + ";")
         cursor = conn.cursor()


         # 'select datetime,count  from pytb2'
         query = queryen1.get()
         # pandas are used to read from sqlserver
         tm = pd.read_sql(query, conn)
         tm1 = tm.head(100)
         #datetime count
         plt.plot(tm1[xen1.get()], tm1[yen1.get()])
         plt.scatter(tm1[xen1.get()], tm1[yen1.get()])
         plt.xlabel(xenname1.get(), fontsize=16)
         plt.ylabel(yenname1.get(), fontsize=16)
         plt.title("REAL TIME COUNT MONITORING ", fontsize=25)
         plt.show()






   # counter reset code
   def clickeda():
      client.write_register(address=int(addressr1.get()),value=0,unit=1)

      # a=int(b.get())
      print("write value to register")

      tk.messagebox.showinfo("RESET", "Reset successful Please click on Read Register")
      # label3=tk.Label(window,text="register reset successful")
      # label3.pack()
      # label4.config(text=a)
   frame1 = tk.Frame(window8, bg='blue', height=100, borderwidth=6, relief='sunken')
   frame1.place(x=200,y=0)
   readreg1 = tk.Label(frame1, text="Reading Registers",width=35, font=("Ariel Bold", 10),bg='green')
   readreg1.pack()



   # for reading provide adress,count,unit
   modadd1 = tk.Label(frame1, text="Enter Modbus Address",width=40 )
   modadd1.pack(anchor='nw')
   addressr1 = tk.Entry(frame1, text=310)
   addressr1.pack(anchor='nw')
   modcount1 = tk.Label(frame1, text="Enter Count",width=40 )
   modcount1.pack(anchor='nw')
   countr1 = tk.Entry(frame1, text=311)
   countr1.pack(anchor='nw')
   modunit1 = tk.Label(frame1, text="Enter Unit",width=40 )
   modunit1.pack(anchor='nw')
   unitr1 = tk.Entry(frame1, text=312)
   unitr1.pack(anchor='nw')


   sqlserver1 = tk.Label(frame1, text="Enter Database Details",width=35, font=("Ariel Bold", 10),bg='green'  )
   sqlserver1.pack(anchor='nw')

   driverlb1=tk.Label(frame1, text="Enter Driver Name",width=40 )
   driverlb1.pack(anchor='nw')
   driver1 = tk.Entry(frame1,text=413)
   driver1.pack(anchor='nw')
   serverlb1 = tk.Label(frame1, text="Enter Server Name",width=40 )
   serverlb1.pack(anchor='nw')
   server1 = tk.Entry(frame1,text=414)
   server1.pack(anchor='nw')
   databaselb1 = tk.Label(frame1, text="Enter Database Name",width=40 )
   databaselb1.pack(anchor='nw')
   database1 = tk.Entry(frame1, text=415)
   database1.pack(anchor='nw')
   Tablelb1 = tk.Label(frame1, text="Enter Table Name",width=40 )
   Tablelb1.pack(anchor='nw')
   table1 = tk.Entry(frame1, text=416)
   table1.pack(anchor='nw')
   xlb1 = tk.Label(frame1, text="Enter Database column Name",width=40 )
   xlb1.pack(anchor='nw')
   xen1 = tk.Entry(frame1, text=417)
   xen1.pack(anchor='nw')
   ylb1 = tk.Label(frame1, text="Enter Database column Name ",width=40 )
   ylb1.pack(anchor='nw')
   yen1 = tk.Entry(frame1, text=418)
   yen1.pack(anchor='nw')


   trustlb1 = tk.Label(frame1, text="Trusted Connection",width=40 )
   trustlb1.pack(anchor='nw')
   trust1= tk.Entry(frame1, text=419)
   trust1.pack(anchor='nw')
   readbut1 = tk.Button(frame1, text="READ_REGISTERS", bg='yellow', width=30, font=("Ariel Bold", 10), command=reada)
   readbut1.pack()
   writebut1 = tk.Button(frame1, text="RESET", bg='yellow', width=30, font=("Ariel Bold", 10), command=clickeda)
   writebut1.pack()
   resultlb1 = tk.Label(frame1, text="Result", width=10, font=("Ariel Bold", 10))
   resultlb1.pack(side='right', anchor='nw')

   # for plotting
   frame2 = tk.Frame(window8, bg='blue', height=100, borderwidth=6, relief='sunken')
   frame2.place(x=200,y=580)
   graphlb1 = tk.Label(frame2, text="Plotting Graphs",width=35, font=("Ariel Bold", 10),bg='green' )
   graphlb1.pack()

   querylb1 = tk.Label(frame2, text="Enter Query",width=40 )
   querylb1.pack(anchor='nw')
   queryen1 = tk.Entry(frame2, text=320)
   queryen1.pack(anchor='nw')


   xlbname1 = tk.Label(frame2, text="Give Name For X Label",width=40 )
   xlbname1.pack(anchor='nw')
   xenname1 = tk.Entry(frame2, text=321)
   xenname1.pack(anchor='nw')
   ylbname1 = tk.Label(frame2, text="Give Name For Y Label",width=40 )
   ylbname1.pack(anchor='nw')
   yenname1 = tk.Entry(frame2, text=322)
   yenname1.pack(anchor='nw')
   pltbut1 = tk.Button(frame2, text="GENERATE GRAPHS",bg='yellow', width=30, font=("Ariel Bold", 10), command=plota)
   pltbut1.pack()

# window 2 over

# WINDOW 3
def win3():
   window3 = tk.Tk()
   window3.title("Read Discrete Inputs")
   window3.geometry("300x320")
   window3.config(background="black")
   window3.maxsize(300, 320)
   clock2= tk.Label(window3, text=formatted_date)
   clock2.pack(side='right', anchor='se')

   # CONVEYER CHECK
   # to read discrete inputs
   def conv():
      x1 = client.read_discrete_inputs(address=int(addressdisc.get()), count=1,unit=int(unitdisc.get()))
      print(x1.bits[0])
      # bits[0] means if adress is 1281 then it will display content of 1281
      if x1.bits[0] == True:
         run = 'green'
      else:
         run = 'red'

      worklb.config(bg=run)
   frame2 = tk.Frame(window3, bg='blue', borderwidth=6, relief='sunken')
   frame2.place(x=60,y=0)
   modadd = tk.Label(frame2, text="Enter Modbus Address",width=25 )
   modadd.pack(anchor='nw')
   addressdisc = tk.Entry(frame2, text=300)
   addressdisc.pack(anchor='nw')
   modunit = tk.Label(frame2, text="Enter Unit",width=25 )
   modunit.pack(anchor='nw')
   unitdisc = tk.Entry(frame2, text=301)
   unitdisc.pack(anchor='nw')
   worklb = tk.Label(frame2, text="WORKING ", width=22, font=("Ariel Bold", 10))
   worklb.pack()


   checkbt=tk.Button(frame2,text="CHECK",command=conv)
   checkbt.pack()

   def bagson():

      y0=client.read_coils(address=int(addressdisc1.get()),count=1,unit=int(unitdisc1.get()))
      print(y0.bits[0])

      if y0.bits[0]==True:
        run1='green'
      else:
         run1='red'
      worklb1.config(bg=run1)


   frame3 = tk.Frame(window3, bg='blue', borderwidth=6, relief='sunken')
   frame3.place(x=60,y=150)
   modadd1 = tk.Label(frame3, text="Enter Modbus Address",width=25 )
   modadd1.pack(anchor='nw')
   addressdisc1 = tk.Entry(frame3, text=302)
   addressdisc1.pack(anchor='nw')
   modunit1 = tk.Label(frame3, text="Enter Unit",width=25 )
   modunit1.pack(anchor='nw')
   unitdisc1 = tk.Entry(frame3, text=303)
   unitdisc1.pack(anchor='nw')
   worklb1 = tk.Label(frame3, text="WORKING", width=22, font=("Ariel Bold", 10))
   worklb1.pack()
   checkbt1 = tk.Button(frame3, text="CHECK", command=bagson)
   checkbt1.pack()






# WINDOW 3 OVER


def win4():
   window4 = tk.Tk()
   window4.title("Read Discrete Inputs")
   window4.geometry("300x320")
   window4.config(background="black")
   window4.maxsize(300, 320)
   clock4 = tk.Label(window4, text=formatted_date)
   clock4.pack(side='right', anchor='se')
   def sens():
      t0 = client.read_discrete_inputs(address=int(addressdisc2.get()),count= 1,unit=int(unitdisc2.get()))

      if t0.bits[0] == True:
         run2 = 'green'
      else:
         run2 = 'red'
      worklb2.config(bg=run2)



   frame4 = tk.Frame(window4, bg='blue', borderwidth=6, relief='sunken')
   frame4.place(x=60,y=0)
   modadd2 = tk.Label(frame4, text="Enter Modbus Address",width=25 )
   modadd2.pack(anchor='nw')
   addressdisc2 = tk.Entry(frame4, text=304)
   addressdisc2.pack(anchor='nw')
   modunit2 = tk.Label(frame4, text="Enter Unit",width=25 )
   modunit2.pack(anchor='nw')
   unitdisc2 = tk.Entry(frame4, text=305)
   unitdisc2.pack(anchor='nw')
   worklb2 = tk.Label(frame4, text="WORKING", width=22, font=("Ariel Bold", 10))
   worklb2.pack()
   # label7 = tk.Label(frame4, text="  Bag Length Sensor    ", width=20, font=("Ariel Bold", 10))
   # label7.pack()
   checkbt2 = tk.Button(frame4, text="CHECK", command=sens)
   checkbt2.pack()

   def sens1():
      t1 = client.read_discrete_inputs(address=int(addressdisc3.get()),count=1,unit=int(unitdisc3.get()))

      if t1.bits[0]==True:
        run3='green'
      else:
         run3='red'
      worklb3.config(bg=run3)


   frame5 = tk.Frame(window4, bg='blue', borderwidth=6, relief='sunken')
   frame5.place(x=60,y=150)
   modadd3 = tk.Label(frame5, text="Enter Modbus Address",width=25 )
   modadd3.pack(anchor='nw')
   addressdisc3 = tk.Entry(frame5, text=306)
   addressdisc3.pack(anchor='nw')
   modunit3 = tk.Label(frame5, text="Enter Unit",width=25 )
   modunit3.pack(anchor='nw')
   unitdisc3 = tk.Entry(frame5, text=307)
   unitdisc3.pack(anchor='nw')
   worklb3 = tk.Label(frame5, text="WORKING", width=22, font=("Ariel Bold", 10))
   worklb3.pack()
   # label8 = tk.Label(frame5, text="  Speed Sensor    ", width=20, font=("Ariel Bold", 10))
   # label8.pack()
   checkbt3 = tk.Button(frame5, text="CHECK", command=sens1)
   checkbt3.pack()

# window 1 widgets
# here there are buttons present which on press will enter to next screen
titlelb = tk.Label(window, text="PYHMI",width=17,font=("Ariel Bold",40),bg='blue')
titlelb.place(x=1,y=1)
# image=Image.open("1.PNG")
img=Image.open("nalogo.png")
img=img.resize((67,64),Image.ANTIALIAS)
img=ImageTk.PhotoImage(img)


# image=img.__reduce__(250,250)
# #
label=tk.Label(window,image=img)
label.place(x=0,y=0)


label50=tk.Label(window,text="Select Type Of Communication",font=("Ariel Bold",15),bg='yellow')
label50.place(x=110,y=66)
but4 = tk.Button(text="      MODBUS TCP/IP       ",font=("Ariel Bold",10), command=win5)
but4.place(x=170,y=96)


but5 = tk.Button(text="        MODBUS ASCII       ",font=("Ariel Bold",10), command=win6)
but5.place(x=170,y=123)
frame6 = tk.Frame(window, bg='blue', borderwidth=6,width=32, relief='sunken')
frame6.place(x=60,y=155)
label51=tk.Label(frame6,text="INDEX",width=32,font=("Ariel Bold",15),fg='red',bg='yellow')
label51.pack()

but1=tk.Button(frame6,text="Register read and reset", width=30,font=("Ariel Bold",15),command=win2)
but1.pack()
win8=tk.Button(frame6,text="Register read and reset", width=30,font=("Ariel Bold",15),command=win8)
win8.pack()

but2 = tk.Button(frame6,text="   Read Discrete Inputs      ", width=30,font=("Ariel Bold",15), command=win3)
but2.pack()

but3 = tk.Button(frame6,text="      Read Discrete Inputs       ", width=30,font=("Ariel Bold",15), command=win4)
but3.pack()
namelb = tk.Label(window, text="NAKSH AUTOMATION",width=45,font=("Ariel Bold",15),bg='blue')
namelb.place(x=1,y=360)



window.mainloop()

