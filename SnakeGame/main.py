import pygame, sys, time, random

pygame.init()

play_surface = pygame.display.set_mode((500, 500))
font = pygame.font.Font(None, 30)

fps = pygame.time.Clock()

# Definir algunos colores
AZUL = (0, 153, 221)
WHITE = (255, 255, 255)
RED = (231, 130, 132)
GREEN = (152, 195, 121)
COLOR_SNAKE_HEAD = (120, 133, 65)


def food():
    random_pos = random.randint(0, 49) * 10
    food_pos = [random_pos, random_pos]
    return food_pos


def main():
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    change = "RIGHT"
    run = True
    food_pos = food()
    score = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and change != "LEFT":
                    change = "RIGHT"
                if event.key == pygame.K_LEFT and change != "RIGHT":
                    change = "LEFT"
                if event.key == pygame.K_UP and change != "DOWN":
                    change = "UP"
                if event.key == pygame.K_DOWN and change != "UP":
                    change = "DOWN"

        if change == "RIGHT":
            snake_pos[0] += 10
        if change == "LEFT":
            snake_pos[0] -= 10
        if change == "UP":
            snake_pos[1] -= 10
        if change == "DOWN":
            snake_pos[1] += 10

        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            food_pos = food()  # re reinicia la comida en otra posicion
            score += 1
        else:
            snake_body.pop()  # para eliminar la ultima posicion

        play_surface.fill((53, 53, 53))
        for pos in snake_body:
            pygame.draw.rect(play_surface, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(
            play_surface, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10)
        )
        pygame.draw.rect(
            play_surface,
            COLOR_SNAKE_HEAD,
            pygame.Rect(snake_body[0][0], snake_body[0][1], 10, 10),
        )

        # Dibujar el rectángulo de fondo para el puntaje
        score_rect = pygame.Rect(10, 10, 50, 30)
        pygame.draw.rect(play_surface, AZUL, score_rect, 0, 5)

        # Renderizar el texto del puntaje y centrarlo dentro del rectángulo de fondo
        text = font.render(str(score), True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = score_rect.center
        play_surface.blit(text, text_rect)

        if score < 10:
            fps.tick(10)
        elif score >= 10 and score < 20:
            fps.tick(15)
        else:
            fps.tick(20)

        if snake_pos[0] <= 0 or snake_pos[0] >= 500:
            run = False
            print("YOU LOSE")
        if snake_pos[1] <= 0 or snake_pos[1] >= 500:
            run = False
            print("YOU LOSE")

        pygame.display.flip()


main()

pygame.quit()
