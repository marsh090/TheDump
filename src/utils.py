from PIL import ImageGrab, Image
import os
import winsound
import pyautogui
import mouse
import time

def beep():
    winsound.Beep(1000, 500)  # Toca um beep de 1000 Hz por 500 ms

def save_image_from_clipboard(save_path):
    image = pyautogui.screenshot()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    image.save(save_path)
    print(f"Imagem salva em: {save_path}")

def wait_for_mouse_click():
    beep()  # Toca um beep para indicar que o usuário deve clicar
    print("Aguardando o clique do mouse...")
    while True:
        if mouse.is_pressed(button='left'):
            position = pyautogui.position()
            print(f"Posição do clique: {position}")
            while mouse.is_pressed(button='left'):
                # Espera o botão ser liberado para evitar múltiplas detecções
                time.sleep(0.1)
            beep()  # Toca um beep para indicar que o clique foi registrado
            return position
        time.sleep(0.1)

def pick_colors_paint():
    print("Clique na cor preta do Paint.")
    black = wait_for_mouse_click()
    
    colors = calculate_paint_colors(black)
    return colors

def calculate_paint_colors(black):
    """
    Calcula a posição das 20 cores base do paint sabendo que cada cor tem 19 pixels de largura e 19 pixels de altura.
    As cores estão distribuidas em um grid de 2 linhas e 10 colunas.
    Adiciona também o codigo da cor em hexadecimal.
    Da esquerda para a direita, de cima para baixo, as cores são:
    - black: #000000
    - dark_gray: #7f7f7f
    - dark_red: #880015
    - red: #ed1c24
    - orange: #ff7f27
    - yellow: #fff200
    - dark_green: #22b14c
    - cyan: #00a2e8
    - blue: #3f48cc
    - purple: #a349a4
    - white: #ffffff
    - light_gray: #c3c3c3
    - brown: #b97a57
    - pink: #ffaec9
    - gold: #ffc90e
    - light_yellow: #efe4b0
    - light_green: #b5e61d
    - light_cyan: #99d9ea
    - light_blue: #7092be
    - light_purple: #c8bfe7
    """
    colors = []
    for i in range(2):
        for j in range(10):
            x = black[0] + 22 * j
            y = black[1] + 22 * i
            colors.append((x, y))
    return colors

def canva_size():
    print("Clique no canto superior esquerdo do canvas.")
    upper_left = wait_for_mouse_click()
    print(f"Posição do canto superior esquerdo do canvas: {upper_left}")
    
    print("Clique no canto inferior direito do canvas.")
    lower_right = wait_for_mouse_click()
    print(f"Posição do canto inferior direito do canvas: {lower_right}")
    
    width = lower_right[0] - upper_left[0]
    height = lower_right[1] - upper_left[1]
    print(f"Tamanho do canvas: {width} x {height}")

    return upper_left, lower_right, width, height

def colors_test():
    colors = pick_colors_paint()
    upper_left, lower_right, width, height = canva_size()
    
    for color in colors:
        pyautogui.moveTo(color)
        pyautogui.click()
        time.sleep(0.1)

        # Move para o centro do canvas + distancia entre o preto e a cor atual (calculada com base nas cores de colors)
        x = upper_left[0] + width / 2 + (color[0] - colors[0][0])
        y = upper_left[1] + height / 2 + (color[1] - colors[0][1])
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(0.1)

def distancia():
    """
    Calcula a distância entre dois pontos baseado no clique do mouse.
    """
    print("Clique no primeiro ponto.")
    p1 = wait_for_mouse_click()
    print(f"Posição do primeiro ponto: {p1}")
    
    print("Clique no segundo ponto.")
    p2 = wait_for_mouse_click()
    print(f"Posição do segundo ponto: {p2}")
    
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    print(f"Distância: {x} x {y}")
    return x, y

def draw():
    """
    Essa função irá pegar a imagem da área de transferência, ler os pixels e desenhar no paint usando as funções e bibliotecas disponiveis.
    """
    # Pega a imagem da área de transferência
    image = ImageGrab.grabclipboard()
    if image is None:
        print("Não há imagem na área de transferência.")
        return
    
    # Pega as cores do paint
    colors = pick_colors_paint()
    upper_left, lower_right, width, height = canva_size()
    
    # Calcula a distância entre os pixels
    x, y = distancia()
    
    # Desenha a imagem no paint
    for i in range(0, image.width, x):
        for j in range(0, image.height, y):
            # Pega a cor do pixel
            pixel = image.getpixel((i, j))
            # Calcula a distância entre a cor do pixel e as cores do paint
            distances = [abs(pixel[0] - color[0]) + abs(pixel[1] - color[1]) + abs(pixel[2] - color[2]) for color in colors]
            # Pega a cor mais próxima
            color_index = distances.index(min(distances))
            # Move para a cor
            pyautogui.moveTo(colors[color_index])
            # Clica
            pyautogui.click()
            # Move para o pixel
            x = upper_left[0] + width / 2 + i
            y = upper_left[1] + height / 2 + j
            pyautogui.moveTo(x, y)
            # Clica
            pyautogui.click()
            time.sleep(0.1)

if __name__ == "__main__":
    #colors_test()
    #distancia()

    draw()