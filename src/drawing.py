from PIL import Image as img
from PIL import ImageGrab
from pynput.mouse import Controller
import keyboard
import os.path
import winsound
import pyautogui
import sys
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
from colormath.color_diff import delta_e_cie2000

# Essa parte afetárá completamente a qualidade
# Nessa configuração atual o desenho é feito em torno de 1 minuto
espacoPixels = 3
tipoConversao = 'RGB'
quantidadeCores = 18
tamanhoImagemX = 100
tamanhoImagemY = 100
pularBranco = True
pyautogui.PAUSE = 1/1000 # Essa variavel é o tempo de espera entre cada pixel, quanto menor mais rápido o desenho
gp_colors = [(0, 0, 0),(102, 102, 102),(0, 80, 205),(255, 255, 255),(170, 170, 170),(38, 201, 255),(1, 116, 32),(153, 0, 0),(150, 65, 18),(17, 176, 60),(255, 0, 19),(255, 120, 41),(176, 112, 28),(153, 0, 78),(203, 90, 87),(255, 193, 38),(255, 0, 143),(254, 175, 168)]

'''
#Para configuração de qualidade máximma utilize assim:
espacoPixels = 1 #Diminua tamanho do Pincel pra 1px neste caso (entre 1 e 10... ajuste conforme o tamanho do pincel)
tipoConversao = 'RGB' (I,F,P,RGB)
quantidadeCores = 256 (entre 0 e 16 milhões mas 256 costuma ser muito bom)
tamanhoImagemX = 250 (entre 20 e 350)
tamanhoImagemY = 250  (entre 20 e 350)
pularBranco = False
pyautogui.PAUSE = 1/1000

#Vai levar de 10 à 20 minutos a imagem nessa configuração, qualidade HD
'''



globalConfig = []



def beep(freq):
    return winsound.Beep(freq, 1000)

def restarApp():
    os.execl(sys.executable, sys.executable, *sys.argv)


def ler_file(file):
    with open(file) as f:
        return list(map(int,(str(f.read()).split(','))))


def write_file(name, array):
    f= open(name,"w");
    f.write(','.join((str(v) for v in array)));
    f.close();

def configurarBOT():
    brush_position = None
    color_positions = {}

    print("Pressione ALT+X para começar a configurar a posição do pincel.")
    brush_position = triggerAltX()  # Save the brush position

    for color in gp_colors:
        print(f"Posicione o cursor sobre a cor {color} e pressione ALT+X.")
        color_position = triggerAltX()
        color_positions[color] = color_position  # Save the position for this color

    # Now write the brush and color positions to the config file
    with open("configs.log", "w") as file:
        file.write(f"brush:{brush_position}\n")
        for color, position in color_positions.items():
            file.write(f"{color}:{position}\n")

    print("Configuração concluída com sucesso!")
    beep(500)  # Signal the end of configuration with a beep

    
def find_closest_color(target_rgb, gp_colors):
    target_color = sRGBColor(*target_rgb, is_upscaled=True)
    target_color_lab = convert_color(target_color, LabColor)

    closest_color = min(
        gp_colors,
        key=lambda color: delta_e_cie2000(
            target_color_lab,
            convert_color(sRGBColor(*color, is_upscaled=True), LabColor)
        )
    )

    return closest_color

lastRGB = "255,255,255"
def pixelar(R, G, B, canvas, ax, ay, color_positions):
    global lastRGB
    target_rgb = (R, G, B)
    if lastRGB != target_rgb:
        lastRGB = target_rgb
        closest_color = find_closest_color(target_rgb, gp_colors)
        color_position = color_positions[closest_color]
        pyautogui.click(color_position[0], color_position[1])
    pyautogui.click(canvas[0]+(ax*espacoPixels), canvas[1]+(ay*espacoPixels))

def screenshot():
    im = ImageGrab.grabclipboard()
    try:
        im.thumbnail((tamanhoImagemX,tamanhoImagemY), img.ANTIALIAS)
    except:
        print("Erro na imagem copiada, tente copiar e dar CTRL + B novamente")
        restarApp()
    beep(1000)
    return im.convert(tipoConversao, palette=img.WEB, colors=quantidadeCores).convert('RGB')

def checkPixel(imageMapPixels, x,y, tox, toy):
    if "{0}_{1}".format(x+tox, y+toy) not in imageMapPixels or  "{0}_{1}".format(x, y) not in imageMapPixels:
        return False
    return imageMapPixels["{0}_{1}".format(x, y)] != imageMapPixels["{0}_{1}".format(x+tox, y+toy)]

def mapImageToDictionary(imagem):
    imageMapPixels = {};
    imageMapColor = {}
    largura, altura = imagem.size
    for y in range(altura):
        for x in range(largura):
            pixel = imagem.getpixel((x, y))
            rgb = "%d,%d,%d" % ((pixel[0]), (pixel[1]), (pixel[2]));
            pixel = "%d_%d" % (x,y);
            if rgb not in imageMapColor.keys():
                imageMapColor[rgb] = []
            imageMapColor[rgb].append([x,y])
            imageMapPixels[pixel] = rgb
    return [imageMapPixels, imageMapColor]

def receberImagem():
    print('Carregando imagem ...')
    canvas = list(Controller().position)
    pyautogui.click(brush_position[0], brush_position[1])
    print('Mapeando imagem ...')
    imagem = screenshot()
    imageMapPixels, imageMapColor = mapImageToDictionary(imagem)
    print("Contabilizado cores: ", len(imageMapColor), "\n\nImagem processada com sucesso!")
    winsound.Beep(1500, 100)
    for rgb in imageMapColor.keys():
        R, G, B = (map(int,(rgb.split(','))))
        if R > 200 and G > 200 and B > 200 and pularBranco:
            continue
        conta = -1
        while(conta < len(imageMapColor[rgb]) - 1):
            if keyboard.is_pressed("ctrl+i"):
                restarApp()
            conta += 1
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], -1, -1):
                continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], 1, 1):
                continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], -1, 0):
                    continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], 0, -1):
                    continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], 1, 0):
                    continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], 0, 1):
                    continue
            pixelar(R,G,B, canvas, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], color_positions)
            del imageMapPixels["{0}_{1}" .format( imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1])]

    for rgb in imageMapColor.keys():
        R, G, B = (map(int,(rgb.split(','))))
        if R > 200 and G > 200 and B > 200 and pularBranco:
            continue
        conta = -1
        while(conta < len(imageMapColor[rgb]) - 1):
            if keyboard.is_pressed("ctrl+i"):
                restarApp()
            conta += 1
            if  "{0}_{1}" .format( imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1]) not in imageMapPixels:
                continue
            pixelar(R,G,B, canvas, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], color_positions)

    input('Desenho completado!')
    restarApp()


def triggerAltX():
    # Wait for the "alt+x" key to be released
    # This ensures that subsequent calls wait for a new key press
    released = False
    while not released:
        if not keyboard.is_pressed('alt+x'):
            released = True

    # Now wait for the next "alt+x" key press
    pressed = False
    while not pressed:
        if keyboard.is_pressed('alt+x'):
            pressed = True
            (x, y) = Controller().position
            return (x, y)

def read_configurations(filename="configs.log"):
    color_positions = {}
    brush_position = (0, 0)

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                key_value = line.strip().split(':')
                if key_value[0] == 'brush':
                    brush_position = tuple(map(int, key_value[1].strip('()').split(',')))
                else:
                    color = tuple(map(int, key_value[0].strip('()').split(',')))
                    position = tuple(map(int, key_value[1].strip('()').split(',')))
                    color_positions[color] = position
    except FileNotFoundError:
        print(f"Error: The configuration file {filename} does not exist.")
    except Exception as e:
        print(f"An error occurred while reading the configurations: {e}")

    return brush_position, color_positions

def iniciarPrograma():
    global brush_position, color_positions

    # Loop indefinitely until the user decides to exit the program
    while True:
        if os.path.exists('configs.log'):
            # If the config file exists, load the brush and color positions
            brush_position, color_positions = read_configurations('configs.log')
            print("\nConfigurações carregadas com sucesso.\n")
        else:
            # If the config file doesn't exist, run the configuration process
            print("\n\n\n=========== PRIMEIRA EXECUÇÃO DO BOT, VAMOS CONFIGURAR ===============\n")
            configurarBOT()

        print("Pressione CTRL+B para começar a desenhar, ou CTRL+C para sair.")
        try:
            while True:
                if keyboard.is_pressed("ctrl+b"):
                    receberImagem()
                    break
                if keyboard.is_pressed("ctrl+c"):
                    print("Programa encerrado pelo usuário.")
                    return
        except KeyboardInterrupt:
            print("Programa interrompido pelo usuário.")
            break

    iniciarPrograma()

iniciarPrograma()