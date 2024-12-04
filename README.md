# rpiLed
Hey, I wanted some of those neat wall lights...

Sometimes they are hexagonal, other times they are triangular...

I wanted them, but I didn't want to buy them...


So, I
  - found 3d models and printed some: https://www.thingiverse.com/thing:4686921
  - wired up 12 leds from a WS2812B "indivudually addressable" strip in 3 sections of 4 leds in each triangle
  - grabbed a Raspberry Pi 3 B+ (Raspberry Pi OS Lite)
  - need a beefy power supply if I ever want to run lots of these https://www.amazon.com/gp/product/B06XK2DDW4/ref=ppx_yo_dt_b_asin_title_o02_s01?ie=UTF8&psc=1 (if the link dies it is a 20A 5V power supply)
  - wrote a bunch of python code (found in this repo) to control the leds

...and this is what it looks like:
![qapa6JU](https://user-images.githubusercontent.com/28834331/168857862-4777be3f-f134-44e3-944e-e714bc9a099c.jpeg)
![lRoUSmw](https://user-images.githubusercontent.com/28834331/168857881-5cd15baa-9221-4b2e-a948-087c7185743d.jpeg)
![GtuW6bU](https://user-images.githubusercontent.com/28834331/168857901-3b307cda-8179-4a67-9b2d-99ec2fd9c9a3.jpeg)
![Z7mXNbk](https://user-images.githubusercontent.com/28834331/168857920-7c7fbf42-dbbb-4765-a868-170a0c9c5b17.jpeg)

The code in the rpi_ws281x/ directory I found online and used in my project.  I don't recall exactly where the files came from, but they are untouched and their comments cite authorship.  Everything else I wrote.

# setup

I haven't setup this on a fresh RPi in a long time.  So, I don't recall all of the steps.  Searching for the original repos of rpi_ws281x/ content would probably have more detail on setup.  I'll improve this section when I have to redo the setup myself :).  But I think you have to do at least this:

```pip3 install adafruit-circuitpython-neopixel```

# stuff to do

There is much more code to write as there are only a couple patterns that multiple triangles can do in concert with each other.  There are many simple patterns an individual triangle can do alone.  But, to have a coherent display of colors with multiple triangles...things get a little complex.

