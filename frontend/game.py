import pygame
import random
import sys
import requests

# Inicializa o Pygame
pygame.init()

# Definir as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definir o tamanho da tela
WIDTH, HEIGHT = 500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Digitação Rápida")

# Fonte
font = pygame.font.Font(None, 30)

# Palavras por fase
words_phase_1 = ["apple", "banana", "cat", "dog", "elephant", "fish", "guitar", "house", "ice", "jungle"]
words_phase_2 = words_phase_1 + ["kiwi", "lemon", "mouse", "night", "ocean", "parrot", "queen", "rose", "sun", "tree"]
words_phase_3 = words_phase_2 + ["universe", "vaccine", "water", "xylophone", "yellow", "zebra"]

# Função para verificar colisões
def check_collision(new_word, words_on_screen):
    for word in words_on_screen:
        if (new_word["x"] < word["x"] + font.size(word["text"])[0] and
            new_word["x"] + font.size(new_word["text"])[0] > word["x"] and
            new_word["y"] < word["y"] + font.size(word["text"])[1] and
            new_word["y"] + font.size(new_word["text"])[1] > word["y"]):
            return True
    return False

# Função para desenhar a tela
def draw_screen(words, score, phase, user_input):
    screen.fill(WHITE)

    # Exibir a fase atual
    phase_text = font.render(f"Fase: {phase}", True, BLACK)
    screen.blit(phase_text, (10, 10))

    # Exibir a pontuação
    score_text = font.render(f"Pontuação: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 10))

    # Mostrar palavras na tela
    for word in words:
        word_text = font.render(word["text"], True, BLACK)
        screen.blit(word_text, (word["x"], word["y"]))
        word["y"] += word["speed"]

        if word["y"] > HEIGHT:
            word["y"] = 0
            word["x"] = random.randint(50, WIDTH - 200)
            word["speed"] = random.uniform(0.5 + (phase - 1) * 0.2, 1.5 + (phase - 1))

    # Exibir entrada do usuário
    user_input_text = font.render(user_input, True, BLACK)
    screen.blit(user_input_text, (WIDTH // 2 - 100, HEIGHT - 50))

    pygame.display.flip()

# Função para enviar pontuações ao servidor Django
def send_score_to_server(username, score, phase):
    url = "http://127.0.0.1:8000/api/submit-score/"
    data = {
        "username": username,
        "score": score,
        "phase": phase
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print("Pontuação enviada com sucesso!")
        else:
            print("Erro ao enviar pontuação:", response.json())
    except Exception as e:
        print("Erro na conexão com o servidor:", e)

# Função principal
def main():
    clock = pygame.time.Clock()
    user_input = ""
    score = 0
    phase = 1
    word_list = words_phase_1
    words_on_screen = []

    # Gerar palavras iniciais
    while len(words_on_screen) < 10:
        word = random.choice(word_list)
        new_word = {"text": word, 
                    "x": random.randint(50, WIDTH - 200), 
                    "y": random.randint(-300, -50), 
                    "speed": random.uniform(0.5, 1.0)}
        if not check_collision(new_word, words_on_screen):
            words_on_screen.append(new_word)

    username = input("Digite seu nome de jogador: ")
    game_running = True

    while game_running:
        draw_screen(words_on_screen, score, phase, user_input)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    word_found = False
                    for word in words_on_screen:
                        if word["text"] == user_input:
                            words_on_screen.remove(word)
                            score += 10
                            word_found = True
                            break

                    if not word_found:
                        score -= 5
                    user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        if not words_on_screen:
            if phase == 1:
                phase = 2
                word_list = words_phase_2
                while len(words_on_screen) < 25:
                    word = random.choice(word_list)
                    new_word = {"text": word, 
                                "x": random.randint(50, WIDTH - 200), 
                                "y": random.randint(-300, -50), 
                                "speed": random.uniform(0.5, 1.0)}
                    if not check_collision(new_word, words_on_screen):
                        words_on_screen.append(new_word)
            elif phase == 2:
                phase = 3
                word_list = words_phase_3
                while len(words_on_screen) < 45:
                    word = random.choice(word_list)
                    new_word = {"text": word, 
                                "x": random.randint(50, WIDTH - 200), 
                                "y": random.randint(-300, -50), 
                                "speed": random.uniform(0.5, 1.0)}
                    if not check_collision(new_word, words_on_screen):
                        words_on_screen.append(new_word)
            else:
                send_score_to_server(username, score, phase)
                print("Fim do jogo!")
                game_running = False

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
