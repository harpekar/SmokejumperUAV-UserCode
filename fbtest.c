#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/fb.h> 
#include <sys/mman.h>

struct framebuffer {
    int file;
    struct fb_fix_screeninfo info_fix;
    struct fb_var_screeninfo info_var;
    size_t size;
    uint8_t * buffer;
};

struct bgra {  //Blue, Green, Red, Alpha (opacity) --default format for BITMAP images
    uint8_t b;
    uint8_t g;
    uint8_t r;
    uint8_t a;
};

void error_out(char const * const message, int const code) {
    fputs(message, stderr);
    exit(code);
}

char * fb_map_location(
    struct framebuffer const * const fb,
    size_t const x,
    size_t const y
) {
    return (x + fb->info_var.xoffset) * (fb->info_var.bits_per_pixel / 8) +
           (y + fb->info_var.yoffset) * (fb->info_fix.line_length       ) +
           fb->buffer;
}

void write_pixel(
    uint8_t * const location,
    size_t const bit_depth,
    struct bgra const color
) {
    switch (bit_depth) {
    case 32:
        *((struct bgra *) location) = color;
        break;

    case 16:
    default:
        *((uint16_t *) location) = (
            (color.r / 16) << 11 |
            (color.g / 16) << 5  |
            (color.b / 16) << 0
        );
        break;
    }
}

void fb_initialize(
    struct framebuffer * const fb,
    char const * const filename
) {
    fb->file = open(filename, O_RDWR);
    if (fb->file == 0)
        error_out("Error opening device file\n", 1);

    if (ioctl(fb->file, FBIOGET_FSCREENINFO, &fb->info_fix))
        error_out("Error reading fixed info\n", 2);

    if (ioctl(fb->file, FBIOGET_VSCREENINFO, &fb->info_var))
        error_out("Error reading variable info\n", 3);

    fb->size = (
        fb->info_var.xres *
        fb->info_var.yres *
        fb->info_var.bits_per_pixel
    ) / 8;
    fb->buffer = mmap(
        0, fb->size,
        PROT_READ | PROT_WRITE, MAP_SHARED,
        fb->file, 0
    );
    if ((int) fb->buffer == -1)
        error_out("Error mapping device to memory", 4);
}

void fb_deallocate(struct framebuffer * const fb) {
    munmap(fb->buffer, fb->size);
    close(fb->file);
}

int main(int argc, char* argv[]) {
    if (argc < 2)
        error_out("Please provide a framebuffer file (/dev/fb0)\n", 1);

    struct framebuffer fb;
    fb_initialize(&fb, argv[1]);
    printf(
        "Framebuffer: [ %dx%d ], %d bits per pixel\n",
        fb.info_var.xres, fb.info_var.yres,
        fb.info_var.bits_per_pixel
    );

    size_t x, y;
    for (x = 100; x < 200; x++) {
        for (y = 100; y < 200; y++) {
            struct bgra color = {
                100,
                0   + (x - 50),
                100 - (y - 100) / 2,
                0
            };
            write_pixel(
                fb_map_location(&fb, x, y),
                fb.info_var.bits_per_pixel,
                color
            );
        }
    }

    fb_deallocate(&fb);
    return 0;
}
