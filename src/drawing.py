from PIL import ImageGrab, Image
import os
import winsound
import pyautogui
import mouse
import time

def beep():
    winsound.Beep(1000, 500)  # Toca um beep de 1000 Hz por 500 ms

def save_image_from_clipboard(save_path):
    image = ImageGrab.grabclipboard()
    if isinstance(image, Image.Image):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        image.save(save_path)
        print(f"Imagem salva em: {save_path}")
        return True
    else:
        print("Não há imagem na área de transferência.")
        return False

def wait_for_mouse_click():
    beep()  # Toca um beep para indicar que o usuário deve clicar
    print("Aguardando o clique do mouse...")
    mouse.wait(button='left', target_types='down')
    position = pyautogui.position()
    print(f"Posição do clique: {position}")
    beep()  # Toca um beep para indicar que o clique foi registrado
    return position

def pick_colors_paint():
    print("Clique na cor preta do Paint.")
    black = wait_for_mouse_click()
    return calculate_paint_colors(black)

def calculate_paint_colors(black):
    colors = {}
    for i in range(2):
        for j in range(10):
            color_hex = pyautogui.pixel(black[0] + 22 * j, black[1] + 22 * i)
            color = {
                'hex': color_hex,
                'x': black[0] + 22 * j,
                'y': black[1] + 22 * i
            }
            colors[color_hex] = color
    return colors

def canva_size():
    print("Clique no canto superior esquerdo do canvas.")
    upper_left = wait_for_mouse_click()
    print("Clique no canto inferior direito do canvas.")
    lower_right = wait_for_mouse_click()
    width = lower_right[0] - upper_left[0]
    height = lower_right[1] - upper_left[1]
    print(f"Tamanho do canvas: {width} x {height}")
    return upper_left, lower_right, width, height

def get_closest_color(colors, pixel):
    closest_color = None
    closest_distance = float('inf')
    for color_hex, color in colors.items():
        distance = sum((a - b) ** 2 for a, b in zip(color['hex'], pixel))
        if distance < closest_distance:
            closest_distance = distance
            closest_color = color
    return closest_color

def draw():
    image = ImageGrab.grabclipboard()
    if image is None:
        print("Não há imagem na área de transferência.")
        return
    colors = pick_colors_paint()
    upper_left, lower_right, width, height = canva_size()
    for x in range(0, image.width, 10):  # Ajuste o passo conforme necessário
        for y in range(0, image.height, 10):  # Ajuste o passo conforme necessário
            pixel = image.getpixel((x, y))
            color = get_closest_color(colors, pixel)
            pyautogui.moveTo(color['x'], color['y'])
            pyautogui.click()
            pyautogui.moveTo(upper_left[0] + x, upper_left[1] + y)
            pyautogui.click()

if __name__ == "__main__":
    draw()
