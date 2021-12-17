import sys
import pygame as pg

pg.font.init()
myfont = pg.font.SysFont('Helvetica', 14)

class Vertex():
    def __init__(self, x, y, width):
        self.rect = pg.Rect(x, y, width, width)
        self.x = x
        self.y = y
        self.width = width
        self.dragging = False
        self.neighbors = []
        self.addingneighbor = False

    def adjoin(self, vertex):
        self.neighbors.append(vertex)

class Graph():
    def __init__(self):
        self.vertices = []

    

def main():
    SCREENWIDTH = 1280
    SCREENHEIGHT = 960
    screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    clock = pg.time.Clock()
    rect = pg.Rect(300, 220, 20, 20)
    spacing_button = pg.Rect(0,SCREENHEIGHT - 20,140,20)
    spacing_button_text = myfont.render('distribute points', False, (0, 0, 0))
    vertex1 = Vertex(300, 220, 20)
    vertexlist = [vertex1]
    addingneighbor = False
    add = True

    velocity = (0, 0)
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:

                    for vertex in vertexlist:
                        if vertex.rect.collidepoint(event.pos[0], event.pos[1]) == True: # if you clicked on a vertex
                            add = False # don't add a new vertex if we're clicking on old ones
                            if not addingneighbor: # meaning that this is the first vertex in the pair of vertices that we're joining
                                addingneighbor = True # get ready to adjoin another vertex to the one we just clicked
                                addvertex = vertex # save this vertex so we can adjoin it to the next one we click
                                print("click next vertex")
                            else: # meaning that this is the second vertex in the pair of vertices that we're joining
                                if vertex.rect.collidepoint(event.pos[0], event.pos[1]) == True: # if you actually click on a vertex
                                    vertex.adjoin(addvertex) # add the first vertex as a neighbor to the one you just clicked on 
                                    addingneighbor = False # we don't want to add any more neighbors
                                    addingneighbor = False
                                    print("the vertex at position " + str(vertex.x) + ", " + str(vertex.y) + " is now neighbors with the vertex at position " + str(addvertex.x) + ", " + str(addvertex.y))
                                    break
                                else:
                                    print("no")
                    if add:
                        vertexlist.append(Vertex(event.pos[0], event.pos[1], 20))
                    add = True


                    # print(len(vertexlist))

                if event.button == 1:
                    for vertex in vertexlist:
                        if vertex.rect.collidepoint(event.pos):
                            vertex.dragging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = vertex.rect.x - mouse_x
                            offset_y = vertex.rect.y - mouse_y
                            break

            elif event.type == pg.MOUSEBUTTONUP:
                for vertex in vertexlist:
                    if event.button == 1:
                        vertex.dragging = False

            elif event.type == pg.MOUSEMOTION:
                for vertex in vertexlist:
                    if vertex.dragging == True:
                        mouse_x, mouse_y = event.pos
                        vertex.rect.x = mouse_x + offset_x
                        vertex.rect.y = mouse_y + offset_y


        mouse = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()



        # if mouse[0] and not rect.collidepoint(pg.mouse.get_pos()):
        #   rect.y += 10

        # if rect.collidepoint(pg.mouse.get_pos()):
        #   mouse = pg.mouse.get_pressed()
        #   print("mouse is on the rect")
            # if mouse[0]:
            #   rect.x = pg.mouse.get_pos()[0] - rect.width//2
            #   rect.y = pg.mouse.get_pos()[1] - rect.height//2



        keys = pg.key.get_pressed()
        if keys[pg.K_a]:  #to move left
            rect.x -= 4
        if keys[pg.K_d]: #to move right
            rect.x += 4
        if keys[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()


        screen.fill((40, 40, 40))
        for vertex in vertexlist:
            for neighbor in vertex.neighbors:
                pg.draw.line(screen, (75,100,10), (vertex.rect.x + vertex.rect.width // 2, vertex.rect.y + vertex.rect.width // 2), (neighbor.rect.x + neighbor.rect.width // 2, neighbor.rect.y + neighbor.rect.width // 2))
                pg.draw.rect(screen, (150, 200, 20), neighbor.rect)
            pg.draw.rect(screen, (150, 200, 20), vertex.rect)
            pg.draw.rect(screen, (100, 100, 100), spacing_button)
            screen.blit(spacing_button_text, (6,SCREENHEIGHT - 20))
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()