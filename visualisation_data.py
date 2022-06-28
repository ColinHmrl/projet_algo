import pygame

def draw_nodes_and_bases_routes(nodes, window, route_list):
    # draw nodes and bases routes
    #window.fill((255, 255, 255))
    """    for nodex in nodes:
        
        for nodey in nodes:
            # draw line from nodex to nodey
            pygame.draw.line(window, (100, 100, 100), nodex, nodey, 2)
            """

    for nodex in nodes:
        pygame.draw.circle(window, "#0D5C63", nodex, 20)

    for index in range(len(nodes)):
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = font.render(str(index), True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (nodes[index][0] , nodes[index][1])
        window.blit(text_surface, text_rect)

    for i in range(len(route_list[0])):
        pygame.draw.line(window, (100, 100, 100), nodes[route_list[0][i][0]], nodes[route_list[0][i][1]], 2)

    pygame.display.update()

    while True:
        if pygame.event.get(pygame.QUIT):
            break

    
    pygame.quit()