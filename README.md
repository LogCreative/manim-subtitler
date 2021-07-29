# manim-subtitler
A LaTeX subtitler with the support of manim.

> If you want an open-and-use experience, please fork this repo and replace the content of `test/main.srt` to your exported subtitle. After the commit, you could check Actions->[The latest action]->Artifacts to get your subtitle video!

## Install manim

Check out [manim](https://github.com/3b1b/manim) webpage to learn how to install manim. Please install the newest version of manim (1.1.0).

The easiest way could be
```
pip install manimgl
```

## Parse subtitle

run in command line:
```
cd src
python parser.py path/to/subtitle.srt
```

## Render the animation

After parsing, the intermediate interface will be in `subtitle.csv`.
```
manimgl render.py -w
```
You can change the output path to the video in `custom_config.yml`.

## Customization

The customization work will be implemented by an HTML file. In this stage, you could try to change to different animation in `render.py`. Read [manim documentation](https://docs.manim.org.cn/animation/index.html) for details.

About the subtitle `.srt` file. In the current stage, the overlapping of text blocks is not allowed. You can output the subtitle file from Premiere 2021 directly in order to match your video.

```
MIT License
(c) LogCreative 2021
```