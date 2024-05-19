import pygame

pygame.init()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

n = int(input("Введіть бажану кількість елементів піраміди: "))

rect_width = width/6
rect_height = 0.87*rect_width/n

floor = pygame.Rect((0, 520), (width, height-520))

zone1 = pygame.Rect((width/4-width/10,520),(width/5, 40))
zone2 = pygame.Rect((width/2-width/10,520),(width/5, 40))
zone3 = pygame.Rect((3*width/4-width/10,520),(width/5, 40))

def draw_stacks(stacks):
    for stack in stacks:
        if len(stack) > 1:
            for rect in stack[1:]:
                pygame.draw.rect(screen, 'black', rect, width=3)
    pygame.display.flip()
    
def generate_n_rects(n: int, stack: list):
    for i in range(n):
        new_rect = pygame.Rect((stack[0] - rect_width/2 + rect_height*i*0.577, floor.top - rect_height*(i+1)), (rect_width - 2*i*rect_height*0.577, rect_height))
        stack.append(new_rect)
    return stack

# Animated movement of a rectangle

velocity_up = (0, -1)
velocity_down = (0, 1)

def move_rect(stack1: list[pygame.Rect], stack2: list[pygame.Rect]):
    if len(stack1) > 1:
        item = stack1.pop()
    
        # pick the rectangle up
        while item.bottom > floor.top - 0.87*rect_width:
            pygame.draw.rect(screen, 'white', item)
            item.move_ip(velocity_up)
            pygame.draw.rect(screen, 'black', item, width=3)
            draw_stacks(stacks)
            pygame.display.flip()
    
        # move it to the other place
        if stack2[0] > item.centerx:
            direction = 1
        else:
            direction = -1
        while item.centerx != stack2[0]:
            pygame.draw.rect(screen, 'white', item)
            item.move_ip(direction, 0)
            pygame.draw.rect(screen, 'black', item, width=3)
            draw_stacks(stacks)
            pygame.display.flip()
        
        # put it down
        while item.bottom < (stack2[-1].top if len(stack2)>1 else floor.top):
            pygame.draw.rect(screen, 'white', item)
            item.move_ip(velocity_down)
            pygame.draw.rect(screen, 'black', item, width=3)
            draw_stacks(stacks)
            pygame.display.flip()
            
        stack2.append(item)

stack1 = [width/4,]
stack2 = [width/2,]
stack3 = [3*width/4,]

stacks = [stack1, stack2, stack3]

def move_pile(N, stack1, stack2):
    if len(stack1) < 2:
        return None

    if N==1:
        move_rect(stack1, stack2)
    else:
        stack_temp = [stack for stack in stacks if stack != stack1 and stack != stack2][0]
        move_pile(N-1, stack1, stack_temp)
        move_rect(stack1, stack2)
        move_pile(N-1, stack_temp, stack2)

# Починаємо малювати

generate_n_rects(n, stack1)

screen.fill("white")
pygame.draw.rect(screen, 'yellow', floor)
pygame.draw.rect(screen, 'gray', zone1)
pygame.draw.rect(screen, 'gray', zone2)
pygame.draw.rect(screen, 'gray', zone3)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # pygame.draw.rect(screen, 'black', rect, width=3)
    draw_stacks(stacks)

    pygame.display.flip()  # Refresh on-screen display
    
    move_pile(n, stack1, stack3)
