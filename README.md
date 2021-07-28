# manim-subtitler
A LaTeX subtitler with the support of manim.

## Install manim

Check out [manim](https://github.com/3b1b/manim) webpage to learn how to install manim.

The easiest way could be
```
pip install manimgl
```

## Parse Subtitle

run in command line:
```
cd src
python parser.py [path to subtitle.srt]
```

## Render the animation

After parsing, the intermediate interface will be in `subtitle.csv`.
```
manimgl render.py -w
```
You can change the output path to the video in `custom_config.yml`.

![](src/videos/DisplayLines.mp4)