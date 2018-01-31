#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

#define PIN 13

class PixelRenderer {

  public:

    PixelRenderer () = default;

    void init () {

      m_strip.begin();
      m_strip.show();

    };

    Adafruit_NeoPixel& getStrip () { return m_strip; };

    void draw (const char data[120]) {

      for (char i = 0; i < 40; ++i) {
        char start = i * 3;
        m_strip.setPixelColor(i, m_strip.Color(data[start], data[start + 1], data[start + 2]));
      }
      m_strip.show();

    }

  private:

    Adafruit_NeoPixel m_strip = Adafruit_NeoPixel(40, PIN, NEO_GRB + NEO_KHZ800);;

};

enum class Character {
  A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z,
  N1, N2, N3, N4, N5, N6, N7, N8, N9, N0,
  SPACE, PERIOD, COMMA, QUESTION, EXCLAMATION, DOLLAR, POUND, DASH, SLASH, PLUS, EQUALS, AMPERSAND, LPAREN, RPAREN, QUOTE
};

class Letter {

  public:

    Letter (Character character, char r, char g, char b)
    : m_character(character), m_r(r), m_g(g), m_b(b) {};

    Letter ()
    : m_character(Character::SPACE), m_r(0), m_g(0), m_b(0) {};

    Character getCharacter () const noexcept { return m_character; };
    char getR () const noexcept { return m_r; };
    char getG () const noexcept { return m_g; };
    char getB () const noexcept { return m_b; };

    char getWidth () {

      switch (m_character) {

        case Character::I:
        case Character::PERIOD:
        case Character::EXCLAMATION:
        case Character::QUOTE:
          return 1;

        case Character::SPACE:
        case Character::COMMA:
        case Character::DASH:
        case Character::LPAREN:
        case Character::RPAREN:
          return 2;

        case Character::M:
          return 4;

        default:
          return 3;
      
      }

    }

    static bool m_grid_a[15];
    static bool m_grid_b[15];
    static bool m_grid_c[15];
    static bool m_grid_d[15];
    static bool m_grid_e[15];
    static bool m_grid_f[15];
    static bool m_grid_g[15];
    static bool m_grid_h[15];
    static bool m_grid_i[5];
    static bool m_grid_j[15];
    static bool m_grid_k[15];
    static bool m_grid_l[15];
    static bool m_grid_m[15];
    static bool m_grid_n[20];
    static bool m_grid_o[15];
    static bool m_grid_p[15];
    static bool m_grid_q[15];
    static bool m_grid_r[15];
    static bool m_grid_s[15];
    static bool m_grid_t[15];
    static bool m_grid_u[15];
    static bool m_grid_v[15];
    static bool m_grid_w[15];
    static bool m_grid_x[15];
    static bool m_grid_y[15];
    static bool m_grid_z[15];
    static bool m_grid_1[10];
    static bool m_grid_2[15];
    static bool m_grid_3[15];
    static bool m_grid_4[15];
    static bool m_grid_5[15];
    static bool m_grid_6[15];
    static bool m_grid_7[15];
    static bool m_grid_8[15];
    static bool m_grid_9[15];
    static bool m_grid_0[15];
    static bool m_grid_space[10];
    static bool m_grid_period[5];
    static bool m_grid_comma[10];
    static bool m_grid_question[15];
    static bool m_grid_exclamation[5];
    static bool m_grid_dollar[15];
    static bool m_grid_pound[15];
    static bool m_grid_dash[10];
    static bool m_grid_slash[15];
    static bool m_grid_plus[15];
    static bool m_grid_equals[15];
    static bool m_grid_ampersand[15];
    static bool m_grid_lparen[10];
    static bool m_grid_rparen[10];
    static bool m_grid_quote[5];

  private:

    Character m_character;
    char m_r;
    char m_g;
    char m_b;

};

bool Letter::m_grid_a[15] = {
  0, 1, 0,
  1, 0, 1,
  1, 1, 1,
  1, 0, 1,
  1, 0, 1
};

bool Letter::m_grid_b[15] = {
  1, 1, 0,
  1, 0, 1,
  1, 1, 0,
  1, 0, 1,
  1, 1, 0
};

bool Letter::m_grid_c[15] {
  0, 1, 0,
  1, 0, 1,
  1, 0, 0,
  1, 0, 1,
  0, 1, 0
};

bool Letter::m_grid_d[15] {
  1, 1, 0,
  1, 0, 1,
  1, 0, 1,
  1, 0, 1,
  1, 1, 0
};

bool Letter::m_grid_e[15] {
  1, 1, 1,
  1, 0, 0,
  1, 1, 1,
  1, 0, 0,
  1, 1, 1
};

bool Letter::m_grid_f[15] {
  1, 1, 1,
  1, 0, 0,
  1, 1, 1,
  1, 0, 0,
  1, 0, 0
};

bool Letter::m_grid_g[15] {
  0, 1, 0,
  1, 0, 1,
  1, 0, 0,
  1, 1, 1,
  0, 1, 0
};

bool Letter::m_grid_h[15] {
  1, 0, 1,
  1, 0, 1,
  1, 1, 1,
  1, 0, 1,
  1, 0, 1
};

bool Letter::m_grid_i[5] {
  1,
  1,
  1,
  1,
  1
};

bool Letter::m_grid_j[15] {
  1, 1, 1,
  0, 1, 0,
  0, 1, 0,
  0, 1, 0,
  1, 1, 0
};

bool Letter::m_grid_k[15] {
  1, 0, 1,
  1, 0, 1,
  1, 1, 0,
  1, 0, 1,
  1, 0, 1
};

bool Letter::m_grid_l[15] {
  1, 0, 0,
  1, 0, 0,
  1, 0, 0,
  1, 0, 0,
  1, 1, 1
};

bool Letter::m_grid_m[15] {
  1, 0, 1,
  1, 1, 1,
  1, 0, 1,
  1, 0, 1,
  1, 0, 1
};

bool Letter::m_grid_n[20] {
  1, 0, 0, 1,
  1, 1, 0, 1,
  1, 0, 1, 1,
  1, 0, 0, 1,
  1, 0, 0, 1
};

bool Letter::m_grid_o[15] {
  0, 1, 0,
  1, 0, 1,
  1, 0, 1,
  1, 0, 1,
  0, 1, 0
};

bool Letter::m_grid_p[15] {
  1, 1, 0,
  1, 0, 1,
  1, 1, 0,
  1, 0, 0,
  1, 0, 0
};

bool Letter::m_grid_q[15] {
  0, 1, 0,
  1, 0, 1,
  1, 0, 1,
  1, 1, 1,
  0, 1, 1
};

bool Letter::m_grid_r[15] {
  1, 1, 0,
  1, 0, 1,
  1, 1, 0,
  1, 0, 1,
  1, 0, 1
};

bool Letter::m_grid_s[15] {
  0, 1, 1,
  1, 0, 0,
  0, 1, 0,
  0, 0, 1,
  1, 1, 0
};

bool Letter::m_grid_t[15] {
  1, 1, 1,
  0, 1, 0,
  0, 1, 0,
  0, 1, 0,
  0, 1, 0
};

bool Letter::m_grid_u[15] {
  1, 0, 1,
  1, 0, 1,
  1, 0, 1,
  1, 0, 1,
  1, 1, 1
};

bool Letter::m_grid_v[15] {
  1, 0, 1,
  1, 0, 1,
  1, 0, 1,
  1, 0, 1,
  0, 1, 0
};

bool Letter::m_grid_w[15] {
  1, 0, 1,
  1, 0, 1,
  1, 0, 1,
  1, 1, 1,
  1, 0, 1
};

bool Letter::m_grid_x[15] {
  1, 0, 1,
  1, 0, 1,
  0, 1, 0,
  1, 0, 1,
  1, 0, 1
};

bool Letter::m_grid_y[15] {
  1, 0, 1,
  1, 0, 1,
  0, 1, 0,
  0, 1, 0,
  0, 1, 0
};

bool Letter::m_grid_z[15] {
  1, 1, 1,
  0, 0, 1,
  0, 1, 0,
  1, 0, 0,
  1, 1, 1
};

bool Letter::m_grid_1[10] {
  1, 1,
  0, 1,
  0, 1,
  0, 1,
  0, 1
};

bool Letter::m_grid_2[15] {
  0, 1, 0,
  1, 0, 1,
  0, 1, 0,
  1, 0, 0,
  1, 1, 1
};

bool Letter::m_grid_3[15] {
  1, 1, 0,
  0, 0, 1,
  0, 1, 0,
  0, 0, 1,
  1, 1, 0 
};

bool Letter::m_grid_4[15] {
  1, 0, 1,
  1, 0, 1,
  1, 1, 1,
  0, 0, 1,
  0, 0, 1
};

bool Letter::m_grid_5[15] {
  1, 1, 1,
  1, 0, 0,
  1, 1, 0,
  0, 0, 1,
  1, 1, 0
};

bool Letter::m_grid_6[15] {
  0, 1, 1,
  1, 0, 0,
  1, 1, 0,
  1, 0, 1,
  0, 1, 0
};

bool Letter::m_grid_7[15] {
  1, 1, 1,
  0, 0, 1,
  0, 0, 1,
  0, 1, 0,
  1, 0, 0,
};

bool Letter::m_grid_8[15] {
  0, 1, 0,
  1, 0, 1,
  0, 1, 0,
  1, 0, 1,
  0, 1, 0
};

bool Letter::m_grid_9[15] {
  0, 1, 0,
  1, 0, 1,
  0, 1, 1,
  0, 0, 1,
  1, 1, 0
};

bool Letter::m_grid_0[15] {
  0, 1, 0,
  1, 0, 1,
  1, 1, 1,
  1, 0, 1,
  0, 1, 0
};

bool Letter::m_grid_space[10] {
  0, 0,
  0, 0,
  0, 0,
  0, 0,
  0, 0
};

bool Letter::m_grid_period[5] {
  0,
  0,
  0,
  0,
  1
};

bool Letter::m_grid_comma[10] {
  0, 0,
  0, 0,
  0, 0,
  0, 1,
  1, 0
};

bool Letter::m_grid_question[15] {
  1, 1, 0,
  0, 0, 1,
  0, 1, 0,
  0, 0, 0,
  0, 1, 0
};

bool Letter::m_grid_exclamation[5] {
  1,
  1,
  1,
  0,
  1
};

bool Letter::m_grid_dollar[15] {
  0, 1, 1,
  1, 1, 0,
  1, 1, 0,
  0, 1, 1,
  1, 1, 0
};

bool Letter::m_grid_pound[15] {
  1, 0, 1,
  1, 1, 1,
  1, 0, 1,
  1, 1, 1,
  1, 0, 1
};

bool Letter::m_grid_dash[10] {
  0, 0,
  0, 0,
  1, 1,
  0, 0,
  0, 0
};

bool Letter::m_grid_slash[15] {
  0, 0, 1,
  0, 0, 1,
  0, 1, 0,
  1, 0, 0,
  1, 0, 0
};

bool Letter::m_grid_plus[15] {
  0, 0, 0,
  0, 1, 0,
  1, 1, 1,
  0, 1, 0,
  0, 0, 0
};

bool Letter::m_grid_equals[15] {
  0, 0, 0,
  1, 1, 1,
  0, 0, 0,
  1, 1, 1,
  0, 0, 0
};

bool Letter::m_grid_ampersand[15] {
  0, 1, 0,
  1, 0, 1,
  0, 1, 0,
  1, 1, 1,
  0, 1, 1
};

bool Letter::m_grid_lparen[10] {
  0, 1,
  1, 0,
  1, 0,
  1, 0,
  0, 1
};

bool Letter::m_grid_rparen[10] {
  1, 0,
  0, 1,
  0, 1,
  0, 1,
  1, 0
};

bool Letter::m_grid_quote[5] {
  1,
  0,
  0,
  0,
  0
};

template<size_t SIZE>
class Word {

  public:

    Word (Letter* letters) {

      m_letters = letters;

    };

    int getWidth () {

      int width = 0;
      for (int i = 0; i < SIZE; ++i) {
        width += m_letters[i].getWidth();
        ++width;
      }
      --width;

      return width;

    }

    void render (PixelRenderer& renderer, int offset) {

      char screen[120];       // screen data of 24-bit pixels (R, G, then B char)
      int remaining = offset; // remaining columns to offset
      char skip = 0;          // number of columns to skip in letter
      bool started = false;   // whether or not we've started drawing letters
      char drawn = 0;         // number of columns drawn (and index of column to write to next)
      char toDraw = 8;        // number of columns remaining until the end of the screen

      // loop over each letter
      for (int i = 0; i < SIZE; ++i) {

        // if we're checking for skipped letters still
        if (!started) {

          // if we're out of columns to offset
          if (remaining <= 0) {

            skip = remaining + m_letters[i].getWidth();
            started = true; // no longer skipping letters

          } else { // still have columns to offset

            // subtract the length of this letter and it's subsequent spacing
            remaining -= m_letters[i].getWidth() + 1;
            continue; // and start over

          }

        } else { // not checking for skipped letters anymore

          skip = 0;

        }

        const bool* pixelGrid = nullptr; // pointer to a bool array of pixel data for the current letter (misuse may cause segfault)

        // check type of character and point pixelGrid at its the address of its pixel grid
        switch (m_letters[i].getCharacter()) {

          case Character::A:
            pixelGrid = Letter::m_grid_a;
            break;

          case Character::B:
            pixelGrid = Letter::m_grid_b;
            break;

          case Character::C:
            pixelGrid = Letter::m_grid_c;
            break;

          case Character::D:
            pixelGrid = Letter::m_grid_d;
            break;

          case Character::E:
            pixelGrid = Letter::m_grid_e;
            break;

          case Character::F:
            pixelGrid = Letter::m_grid_f;
            break;

          case Character::G:
            pixelGrid = Letter::m_grid_g;
            break;

          case Character::H:
            pixelGrid = Letter::m_grid_h;
            break;

          case Character::I:
            pixelGrid = Letter::m_grid_i;
            break;

          case Character::J:
            pixelGrid = Letter::m_grid_j;
            break;

          case Character::K:
            pixelGrid = Letter::m_grid_k;
            break;

          case Character::L:
            pixelGrid = Letter::m_grid_l;
            break;

          case Character::M:
            pixelGrid = Letter::m_grid_m;
            break;

          case Character::N:
            pixelGrid = Letter::m_grid_n;
            break;

          case Character::O:
            pixelGrid = Letter::m_grid_o;
            break;

          case Character::P:
            pixelGrid = Letter::m_grid_p;
            break;

          case Character::Q:
            pixelGrid = Letter::m_grid_q;
            break;

          case Character::R:
            pixelGrid = Letter::m_grid_r;
            break;

          case Character::S:
            pixelGrid = Letter::m_grid_s;
            break;

          case Character::T:
            pixelGrid = Letter::m_grid_t;
            break;

          case Character::U:
            pixelGrid = Letter::m_grid_u;
            break;

          case Character::V:
            pixelGrid = Letter::m_grid_v;
            break;

          case Character::W:
            pixelGrid = Letter::m_grid_w;
            break;

          case Character::X:
            pixelGrid = Letter::m_grid_x;
            break;

          case Character::Y:
            pixelGrid = Letter::m_grid_y;
            break;

          case Character::Z:
            pixelGrid = Letter::m_grid_z;
            break;

          case Character::N1:
            pixelGrid = Letter::m_grid_1;
            break;

          case Character::N2:
            pixelGrid = Letter::m_grid_2;
            break;

          case Character::N3:
            pixelGrid = Letter::m_grid_3;
            break;

          case Character::N4:
            pixelGrid = Letter::m_grid_4;
            break;

          case Character::N5:
            pixelGrid = Letter::m_grid_5;
            break;

          case Character::N6:
            pixelGrid = Letter::m_grid_6;
            break;

          case Character::N7:
            pixelGrid = Letter::m_grid_7;
            break;

          case Character::N8:
            pixelGrid = Letter::m_grid_8;
            break;

          case Character::N9:
            pixelGrid = Letter::m_grid_9;
            break;

          case Character::N0:
            pixelGrid = Letter::m_grid_0;
            break;

          case Character::SPACE:
            pixelGrid = Letter::m_grid_space;
            break;

          case Character::PERIOD:
            pixelGrid = Letter::m_grid_period;
            break;

          case Character::COMMA:
            pixelGrid = Letter::m_grid_comma;
            break;

          case Character::QUESTION:
            pixelGrid = Letter::m_grid_question;
            break;

          case Character::EXCLAMATION:
            pixelGrid = Letter::m_grid_exclamation;
            break;

          case Character::DOLLAR:
            pixelGrid = Letter::m_grid_dollar;
            break;

          case Character::POUND:
            pixelGrid = Letter::m_grid_pound;
            break;

          case Character::DASH:
            pixelGrid = Letter::m_grid_dash;
            break;

          case Character::SLASH:
            pixelGrid = Letter::m_grid_slash;
            break;

          case Character::PLUS:
            pixelGrid = Letter::m_grid_plus;
            break;

          case Character::EQUALS:
            pixelGrid = Letter::m_grid_equals;
            break;

          case Character::AMPERSAND:
            pixelGrid = Letter::m_grid_ampersand;
            break;

          case Character::LPAREN:
            pixelGrid = Letter::m_grid_lparen;
            break;

          case Character::RPAREN:
            pixelGrid = Letter::m_grid_rparen;
            break;

          case Character::QUOTE:
            pixelGrid = Letter::m_grid_quote;
            break;

        }

        // if there's still room to draw
        if (toDraw > 0) {

          char start = 0; // stores actual index of screen data for the top left pixel's R channel
          
          // loop for this letter's width
          for (char j = 0; j < m_letters[i].getWidth(); ++j) {

            // if we are supposed to be skipping columns of this letter
            if (skip > 0) {
              
              --skip; // decrement skip
              continue; // and start over (j increments)
            
            } else if (skip < 0) { // negative skip means pre-letter margin

              // loop for each negative skip
              for (; skip < 0; ++skip) {

                // if there's still room to draw
                if (toDraw > 0) {

                  start = drawn * 3; // R channel of first available column

                  // draw a blank column
                  for (char x = 0; x < 5; ++x) {

                    char offset = x * 8 * 3;

                    screen[offset + start] = 0;
                    screen[offset + start + 1] = 0;
                    screen[offset + start + 2] = 0;

                  }

                  // move to next column
                  --toDraw;
                  ++drawn;

                } else {

                  break; // no room to draw, so quit trying

                }

              }
            
            }

            // if there's still room to draw
            if (toDraw > 0) {

              start = drawn * 3; // R channel of first available column

              // draw column of letter
              for (char x = 0; x < 5; ++x) {

                char offset = x * 8 * 3;
                char at = x * m_letters[i].getWidth() + j;

                screen[offset + start] = pixelGrid[at] ? m_letters[i].getR() : 0;
                screen[offset + start + 1] = pixelGrid[at] ? m_letters[i].getG() : 0;
                screen[offset + start + 2] = pixelGrid[at] ? m_letters[i].getB() : 0;

              }

              // move to next column
              --toDraw;
              ++drawn;

            } else {

              break; // no room to draw, so quit trying

            }

          }

          // if there's still room to draw
          if (toDraw > 0) {

            start = drawn * 3; // R channel of first available column

            // draw column of letter
            for (char x = 0; x < 5; ++x) {

              char offset = x * 8 * 3;

              screen[offset + start] = 0;
              screen[offset + start + 1] = 0;
              screen[offset + start + 2] = 0;

            }

            // move to next column
            --toDraw;
            ++drawn;

          } else {

            break; // no room to draw, so quit trying

          }

        } else {

          break;

        }

      }

      // if there's still room to draw (after drawing all the letters)
      if (toDraw > 0) {

        // loop for the remaining columns
        for (char i = 0; i < toDraw; ++i) {

          char start = drawn * 3; // R channel of first available column

          // draw a blank column
          for (char x = 0; x < 5; ++x) {

            char offset = x * 8 * 3;

            screen[offset + start] = 0;
            screen[offset + start + 1] = 0;
            screen[offset + start + 2] = 0;

          }

          // move to next column
          --toDraw;
          ++drawn;

        }

      }

      // draw the screen data to the RGB matrix
      renderer.draw(screen);

    }

  private:

    Letter* m_letters;

};

auto renderer = PixelRenderer();
Letter letters[19] = {
  Letter(Character::A, 16, 0, 0),
  Letter(Character::L, 0, 16, 0),
  Letter(Character::E, 0, 0, 16),
  Letter(Character::X, 16, 16, 0),
  Letter(Character::SPACE, 0, 0, 0),
  Letter(Character::I, 16, 0, 0),
  Letter(Character::S, 16, 0, 0),
  Letter(Character::SPACE, 0, 0, 0),
  Letter(Character::A, 0, 16, 0),
  Letter(Character::SPACE, 0, 0, 0),
  Letter(Character::C, 0, 0, 16),
  Letter(Character::O, 0, 0, 16),
  Letter(Character::O, 0, 0, 16),
  Letter(Character::L, 0, 0, 16),
  Letter(Character::SPACE, 0, 0, 0),
  Letter(Character::G, 0, 16, 16),
  Letter(Character::U, 0, 16, 16),
  Letter(Character::Y, 0, 16, 16),
  Letter(Character::EXCLAMATION, 16, 16, 16)
};
auto theWord = Word<19>(letters);

int offset = -8;

void setup() {

  renderer.init();

}

void loop() {

  theWord.render(renderer, offset);
  ++offset;
  if (offset >= theWord.getWidth() + 8) {
    offset = -8;
  }
  delay(100);

}

