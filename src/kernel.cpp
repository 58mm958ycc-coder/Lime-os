#define SCREEN_WIDTH  1024
#define SCREEN_HEIGHT 768

// Standard Windows BMP file header structure mapping rules
struct __attribute__((packed)) BMPHeader {
    unsigned short signature;     // Must be 'BM'
    unsigned int   file_size;
    unsigned short reserved1, reserved2;
    unsigned int   data_offset;   // Byte offset where raw image pixels start
};

void draw_pixel(int x, int y, unsigned int color) {
    unsigned int* frame_buffer = (unsigned int*)0xFD000000;
    frame_buffer[y * SCREEN_WIDTH + x] = color;
}

void load_splash_screen_bitmap(unsigned char* bmp_file_buffer) {
    BMPHeader* header = (BMPHeader*)bmp_file_buffer;
    
    // Check validation signature (0x4D42 is 'BM' inverted in little-endian systems)
    if (header->signature != 0x4D42) {
        // Fallback layout color code if signature verification fails
        for(int i=0; i<(SCREEN_WIDTH*SCREEN_HEIGHT); i++) {
            unsigned int* fb = (unsigned int*)0xFD000000;
            fb[i] = 0xA3E899; // Pure Lime Green
        }
        return;
    }

    // Pointer address targeting raw graphic raster array segments
    unsigned char* pixels = bmp_file_buffer + header->data_offset;
    
    // Draw row configurations mapping bytes to frame buffer locations
    for (int y = SCREEN_HEIGHT - 1; y >= 0; y--) {
        for (int x = 0; x < SCREEN_WIDTH; x++) {
            // Bitmaps are indexed in Blue-Green-Red (BGR) channel arrays
            unsigned char b = *pixels++;
            unsigned char g = *pixels++;
            unsigned char r = *pixels++;
            
            unsigned int color = (r << 16) | (g << 8) | b;
            draw_pixel(x, y, color);
        }
    }
}

extern "C" void kernel_main() {
    // Points to the physical disk location where GRUB loads the logo asset array
    unsigned char* logo_asset_address = (unsigned char*)0x01000000; 
    load_splash_screen_bitmap(logo_asset_address);
}
