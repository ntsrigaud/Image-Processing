#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION

#include "stb_image.h"
#include "stb_image_write.h"

#include <cstdlib>
#include <iostream>
#include <string>

constexpr double R_WEIGHT = 0.299;
constexpr double G_WEIGHT = 0.587;
constexpr double B_WEIGHT = 0.114;

int main() {
  try {
    std::string input_png = "lena.png";
    std::string output_png = "lena_gray.png";

    int width = 0;
    int height = 0;
    int channels = 0;
    unsigned char *img =
        stbi_load(input_png.c_str(), &width, &height, &channels, 3);
    if (!static_cast<bool>(img)) {
      throw std::runtime_error("Failed to load image: " + input_png);
    }

    // Convert to grayscale in-place
    for (int i = 0; i < width * height * 3; i += 3) {
      unsigned char r = img[i];
      unsigned char g = img[i + 1];
      unsigned char b = img[i + 2];
      auto gray = static_cast<unsigned char>((R_WEIGHT * r) + (G_WEIGHT * g) +
                                             (B_WEIGHT * b));
      img[i] = img[i + 1] = img[i + 2] = gray;
    }

    if (!static_cast<bool>(stbi_write_png(output_png.c_str(), width, height, 3,
                                          img, width * 3))) {
      stbi_image_free(img);
      throw std::runtime_error("Failed to save image: " + output_png);
    }

    stbi_image_free(img);
    std::cout << "Grayscale PNG saved to " << output_png << "\n";

    // Optional: open the file
    std::string cmd;
#if defined(_WIN32)
    cmd = "start " + output_png;
#elif defined(__APPLE__)
    cmd = "open " + output_png;
#elif defined(__linux__)
    cmd = "xdg-open " + output_png;
#endif
    if (!cmd.empty()) {
      std::system(cmd.c_str());
    }

  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
  return 0;
}
