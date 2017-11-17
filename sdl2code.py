def buildCode(rects):
    CCode = ""
    
    for rect in rects:
        CCode += "drawRect(" + str(rect[0])  + ", " + str(rect[1]) + ", " + str(rect[2]) + ", " + str(rect[3]) + ", " + "0xFFFFFFFF" + ", " + "screen);\n"
    
    file = open("main.c", "w")
    contents = """#include <SDL2/SDL.h>

#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 600

SDL_Event event;
SDL_Window *window = NULL;
SDL_Surface *screen = NULL;

void exit_msg(char *msg) {
    printf(msg);
    exit(-1);
}

void cleanup() {
    // free window
    SDL_DestroyWindow(window);
    // quite SDL
    SDL_Quit();
}

void drawRect(int x, int y, int w, int h, int color, SDL_Surface *screen) {
    SDL_Rect rect;
    rect.x = x;
    rect.y = y;
    rect.w = w;
    rect.h = h;
    SDL_FillRect(screen, &rect, color);
}

int main(int argc, char* args[]) {
    // setup SDL
    if(SDL_Init(SDL_INIT_EVERYTHING) == -1)
        exit_msg("Couldn't init SDL");

    // setup SDL window
    window = SDL_CreateWindow("SDL Examples", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    if(window == NULL)
        exit_msg("Couldn't init SDL Window");

    while(1) {
        // check for pending events
        while(SDL_PollEvent(&event)) {
            // quit was requested
            if(event.type == SDL_QUIT) {
                cleanup();
                return 0;
            // keyboard button was hit
            } else if (event.type == SDL_KEYDOWN) {
                // check which key was hit
                switch(event.key.keysym.sym) {
                    // quit
                    case 'q':
                        cleanup();
                        return 0;
                }
            }
        }

        // Get window surface
        screen = SDL_GetWindowSurface(window);

        // Fill background with black
        SDL_FillRect(screen, NULL, 0x000000);
        
        """ + CCode + """
        
        // Update window
        SDL_UpdateWindowSurface(window);
    }

    return 0;
}"""

    file.write(contents)
