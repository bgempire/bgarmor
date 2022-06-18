---
layout: page
title: BGArmor
permalink: /
---

# BGArmor
Welcome to the BGArmor manual! If you're new to BGArmor, take a look at the
[Quickstart Guide]({{ site.baseurl }}/quickstart)
and start using BGArmor in your project right now.

## Introduction
BGArmor is a Blender Game Engine and UPBGE tool that allows you to package your
game data files and launch them separated from the blenderplayer executable.
It's available on Windows and Linux.

This project was inspired by BPPlayer, but it aims to be more compatible and portable.
It also features a project development structure to aid the game development
workflow and ease the release process.

BGArmor also aims to provide a toolchain of tasks to automate the process of game release, including tasks to package the game data files and generate releases, a launcher and blenderplayer icon changer (on Windows) and others.

### Note About Licensing
BGArmor is under the MIT license and do not bundle any Blender or UPBGE components, however any BGE and UPBGE game should comply with the [GPL license](https://download.blender.org/release/GPL3-license.txt). In summary, although a game packaged with BGArmor do not exposes its source code, the source code should be publicly available somewhere else.

## Index
{%- for section in site.data.toc %}
- [{{ section.title }}]({{ section.url }})
{%- if section.links %}
    {%- for link in section.links %}
    - [{{ link.title }}]({{ link.url }})
    {%- endfor %}
{%- endif %}
{%- endfor %}
