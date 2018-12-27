import serial, time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as figtk
from matplotlib.backend_bases import key_press_handler
from tkinter import *

#Conexão com o arduino  115200
arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout = 0)

contador = 0
y=[]
x=[]
z=[]

def enviar():
	
	global x
	global y
	global z
	extra = []

	dado = (float(valor.get())*100)
	global contador
	try:
		while(True):
			janela.update()
			plt.subplot(211)#Seleciona a area que o gráfico será plotado
			contador += 1
			arduino.write(str(dado).encode())
			arduino.flush()
			while (arduino.inWaiting() == 0):
				pass
			leitura = (arduino.readline())
			altura = float(leitura[1:5])
			pwm = float(leitura[6:11])
			print ("altura : " , float(altura))
			print ("pwm : " , float(pwm))
			x.append(contador)
			y.append(altura)
			z.append(pwm)
			extra.append(dado/100)
			plt.plot(x, y, c = (0,0,0)) #Plota a altura que a bola está
			plt.plot(x, extra, c = (0,1,0)) #plota a linha com a altura desejada
			plt.ylim(0,60)
			plt.xlim(x[0], x[0] + 100)
			fig.canvas.draw()
			plt.xlabel("Gráfico da altura")
			plt.subplot(212)
			plt.plot(x , z , c = (0,0,0))
			plt.ylim(0,100)
			plt.xlim(x[0], x[0] + 100)		
			plt.xlabel("Gráfico do PWM")
			fig.canvas.draw()
			if contador % 100 == 0 :
				plt.clf()
				x=[]
				y=[]
				z=[]
				extra = []
				plt.subplot(211)
				plt.clf()
		
	except KeyboardInterrupt:		
		pass

#Definindo janela e botões
janela = Tk()
janela.title("SisMicro")
Label(janela, text = "Digite a altura desejada ").grid(row=0, column=0) 
#Caixa de texto para inserir a altura
valor = Entry(janela) 
valor.grid(row=1, column=0)

fig = plt.figure(figsize=(6,6))
FIGURE = figtk(fig, master=janela)
FIGURE.get_tk_widget().grid(row = 3, column = 0)

def quit():
    janela.quit()
    janela.destroy()

#botão
Button(janela, text = "Enviar", command=enviar).grid(row=2, column=0)
Button(janela, text = "Fechar", command=quit).grid(row=0, column=1)

janela.mainloop()