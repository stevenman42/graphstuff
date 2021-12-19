import sys
import pygame

pygame.font.init()
myfont = pygame.font.SysFont('Helvetica', 14)

class Vertex():
    def __init__(self, x, y, width):
        self.rect = pygame.Rect(x, y, width, width)
        self.x = x
        self.y = y
        self.width = width
        self.dragging = False
        self.neighbors = []
        self.addingneighbor = False
        self.name = ""
        self.draw_outline = False
        self.outline = pygame.Rect(self.rect.x - 5, self.rect.y - 5, 30, 30)
        self.offset_x = 0
        self.offset_y = 0

    def adjoin(self, vertex):
        if not vertex in self.neighbors:
            self.neighbors.append(vertex)

    def setx(self, x):
        self.rect.x = x
        self.x = x
        self.outline = pygame.Rect(x - 5, self.rect.y - 5, 30, 30)

    def sety(self, y):
        self.rect.y = y
        self.y = y
        self.outline = pygame.Rect(self.rect.x - 5, y - 5, 30, 30)

    def snap(self): # places the vertex on the closest point of a lattice
        self.setx( int(round(self.x / 10, -1)*10)) # rounds to the nearest 100
        self.sety( int(round(self.y / 10, -1)*10)) # rounds to the nearest 100



def print_latex(vertexlist, SCREENWIDTH, SCREENHEIGHT):
    scale = 10
    output = "\\begin{tikzpicture}[shorten >=1pt,->]\n\\tikzstyle{vertex}=[circle,fill=black!35,minimum size=12pt,inner sep=2pt]\n"

    for v in range(len(vertexlist)):

        x_pos = str((-1*vertexlist[v].x + SCREENWIDTH / 2)*scale / SCREENWIDTH)
        y_pos = str((-1*vertexlist[v].y + SCREENHEIGHT / 2)*scale / SCREENHEIGHT)

        output += "\\node[vertex] (G_" + str(v+1) + ") at (" + x_pos + ", " + y_pos + ") {" + str(v+1) + "};\n"
        vertexlist[v].name = "G_" + str(v+1)

        # print("the vertex " + vertexlist[v].name + " at position (" + str(vertexlist[v].x) + ", " + str(vertexlist[v].y) + ") has x_pos: " + x_pos + " and y_pos: " + y_pos  )

    output += "\\draw "
    for vertex in vertexlist:
        for neighbor in vertex.neighbors:
            output += "(" + vertex.name + ") -- (" + neighbor.name + ") "
    output += "-- cycle;\n"
    output += "\\end{tikzpicture}"

    print(output)



def main():
    SCREENWIDTH = 1280
    SCREENHEIGHT = 960
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    clock = pygame.time.Clock()
    rect = pygame.Rect(300, 220, 20, 20)
    spacing_button = pygame.Rect(0,SCREENHEIGHT - 20,140,20)
    spacing_button_text = myfont.render('distribute points', False, (0, 0, 0))
    # vertex1 = Vertex(300, 220, 20)
    vertexlist = []
    addingneighbor = False
    add = True

    # multiple vertices can be selected by clicking and dragging
    selecting = False
    selection = pygame.Rect(0,0,0,0)
    selected_vertices = []

    velocity = (0, 0)
    done = False



    while not done:
        for event in pygame.event.get():

            for vertex in vertexlist:
                if (vertex.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] == 1) or vertex in selected_vertices:
                    vertex.draw_outline = True
                else:
                    vertex.draw_outline = False

            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print_latex(vertexlist, SCREENWIDTH, SCREENHEIGHT)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:

                    for vertex in vertexlist:
                        if vertex.rect.collidepoint(pygame.mouse.get_pos()) == True:
                            add = False
                            vertex.addingneighbor = True
                            addingneighbor = True
                            addvertex = vertex
                            print("release the right mouse button on the next vertex")

                    if add:
                        vertexlist.append(Vertex(event.pos[0] - 10, event.pos[1] - 10, 20))
                        break
                    add = True

                if event.button == 1:

                    if spacing_button.collidepoint(pygame.mouse.get_pos()) == True:
                        for vertex in vertexlist:
                            vertex.snap()
                        break

                    clicked_a_vertex = False
                    for vertex in vertexlist:
                        vertex.draw_outline = False
                        if vertex.rect.collidepoint(event.pos):
                            for v in selected_vertices:
                                v.dragging = True
                            # vertex.dragging = True
                            # for v in selected_vertices:
                            #     v.dragging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = vertex.rect.x - mouse_x
                            offset_y = vertex.rect.y - mouse_y
                            clicked_a_vertex = True
                            break
                    if not clicked_a_vertex:

                        print("begin selection")
                        selecting = True
                        selection.x = event.pos[0]
                        selection.topleft = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:

                if selecting:


                    selecting = False
                    for vertex in vertexlist:
                        if vertex.rect.colliderect(selection):
                            print("true")
                            if not vertex in selected_vertices:
                                selected_vertices.append(vertex)
                        else:
                            try:
                                selected_vertices.remove(vertex)
                            except ValueError:
                                pass
                    print(selected_vertices)
                    print(selection.width)

                    selection.x = 0
                    selection.y = 0
                    selection.width = 0
                    selection.height = 0


                for vertex in vertexlist:
                    if event.button == 3:
                        if vertex.rect.collidepoint(pygame.mouse.get_pos()):
                            if addingneighbor and not addvertex == vertex:
                                addvertex.adjoin(vertex) # add the first vertex as a neighbor to the one you just clicked on
                                addvertex.addingneighbor = False
                                addingneighbor = False
                                # print("the vertex at position " + str(vertex.x) + ", " + str(vertex.y) + " is now neighbors with the vertex at position " + str(addvertex.x) + ", " + str(addvertex.y))
                        vertex.addingneighbor = False # we don't want to add any more neighbors
                    if event.button == 1:
                        vertex.dragging = False
                        vertex.setx(vertex.rect.x)
                        vertex.sety(vertex.rect.y)

            elif event.type == pygame.MOUSEMOTION:



                for vertex in vertexlist:

                    if vertex.rect.colliderect(selection):
                        vertex.draw_outline = True

                    if vertex.dragging == True:
                        mouse_x, mouse_y = event.pos
                        vertex.rect.x = mouse_x + offset_x
                        vertex.rect.y = mouse_y + offset_y

            if selecting:
                selection.width = pygame.mouse.get_pos()[0] - selection.x
                selection.height = pygame.mouse.get_pos()[1] - selection.y


        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()


        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()


        screen.fill((40, 40, 40))

        for vertex in vertexlist:
            if vertex.addingneighbor and addingneighbor:
                pygame.draw.line(screen, (100,100,100), (vertex.x + 10, vertex.y + 10), pygame.mouse.get_pos())

            if vertex.draw_outline:
                pygame.draw.rect(screen, (100, 150, 0), vertex.outline, 3)
            for neighbor in vertex.neighbors:
                pygame.draw.line(screen, (75,100,10), (vertex.rect.x + vertex.rect.width // 2, vertex.rect.y + vertex.rect.width // 2), (neighbor.rect.x + neighbor.rect.width // 2, neighbor.rect.y + neighbor.rect.width // 2))
                pygame.draw.rect(screen, (150, 200, 20), neighbor.rect)
            pygame.draw.rect(screen, (150, 200, 20), vertex.rect)
            pygame.draw.rect(screen, (100, 100, 100), spacing_button)
            screen.blit(spacing_button_text, (6,SCREENHEIGHT - 20))

        if selecting:
            pygame.draw.rect(screen, (35, 35, 35), selection, 3)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
    sys.exit()