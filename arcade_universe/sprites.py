from sprite import Sprite

import numpy

def get_sprites(s):
    d = {}
    mapping = {'.': 0,
               'x': 1}
    for name, block in s.items():
        name = name.strip()
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n')
        desc = []
        for line in lines[1:]:
            desc.append(map(mapping.get, line))
        d[name] = Sprite(name, patch=desc)
    return d

spritedesc = { 
"BLIP":
"""
.x.
xxx
.x.
""",

"CROSS":
"""
.x.
.x.
xxx
.x.
.x.
""",

"CATERPILLAR":
"""
.xx.
xxxx
.xx.
xxxx
.xx.
xxxx
.xx.
xxxx
.xx.
xxxx
.xx.
""",

"SPIDER":
"""
..x.....x..
..x.....x..
...x...x...
xx..x.x..xx
..xxxxxxx..
....xxx....
..xxxxxxx..
xx..x.x..xx
...x...x...
..x.....x..
..x.....x..
""",

"MINIBUG":
"""
x.x
.x.
xxx
.x.
x.x
""",
"BALL":
"""
.xx.
xxxx
xxxx
.xx.
""",

"EMPTYBALL":
"""
.xx.
x..x
x..x
.xx.
""",

"ROACH":
"""
.xx....xx.
x..x..x..x
....xx....
..xxxxxx..
.x.xxxx.x.
..xxxxxx..
.x.xxxx.x.
..xxxxxx..
.x..xx..x.
""",

"ANT":
"""
x...x
.x.x.
..x..
.xxx.
x.x.x
.xxx.
x.x.x
.xxx.
x.x.x
""",
"X":
"""
x.x
.x.
x.x
""",

"SUPERX":
"""
xx...xx
xx...xx
..x.x..
...x...
..x.x..
xx...xx
xx...xx
""",
"FLAKE":
"""
.x.x.x.
xx...xx
..x.x..
x..x..x
..x.x..
xx...xx
.x.x.x.
""",
"SQUARE":
"""
xxx
x.x
xxx
""",
"HELIX":
"""
..x....
..x....
..xxxxx
..x.x..
xxxxx..
....x..
....x..
""",
"SIERPINSKI":
"""
...x...
..x.x..
.x.x.x.
x.x.x.x
""",
"DIAMOND":
"""
.x.
x.x
x.x
.x.
""",
"LADYBUG":
"""
.x.x.
..x..
xx.xx
.x.x.
x.x.x
""",
"CENTIPEDE":
"""
.x...x.
x.x.x.x
...x...
.xxxxx.
x..x..x
.xxxxx.
x..x..x
.xxxxx.
x..x..x
.xxxxx.
x..x..x
.xxxxx.
x..x..x
.xxxxx.
x..x..x
.xx.xx.
x.....x
""",

"LINE":
"""
x
x
x
""",

"DIAGONAL":
"""
x..
.x.
..x
""",

"SMALLBALL":
"""
.x.
x.x
.x.
""",
"S":
"""
.xx.
x..x
.x..
..x.
x..x
.xx.
""",
"FATBUG":
"""
x...x
.xxx.
.x.x.
.xxx.
.x.x.
.xxx.
x...x
""",
"C":
"""
xx
x.
xx
""",
"SPIRAL":
"""
xxxxxx
x....x
x.xx.x
x.x..x
x.xxxx
""",
"DRAGONFLY":
"""
..x.
.x..
x.x.
...x
""",
"WALKER":
"""
..x.x.
...xxx
x.xxx.
.xxx.x
xxx...
.x.x..
""",

"CRAWLER":
"""
....x.x.
.....xxx
..x.xxx.
...xxx.x
x.xxx...
.xxx.x..
xxx.....
.x.x....
""",
"ANCHOR":
"""
..x..
.xxx.
..x..
x.x.x
.xxx.
..x..
""",
"SKULL":
"""
.xxx.
x.x.x
x.x.x
.xxx.
..x..
""",
"ASTERISK":
"""
..x..
x.x.x
.xxx.
x.x.x
..x..
""",
"CANDY":
"""
...x.
...xx
..x..
xx...
.x...
""",
"H":
"""
x.x
xxx
x.x
""",
"DUMBBELL":
"""
x..x
xxxx
x..x
""",
"FLYBOX":
"""
x.xxx.x
.xx.xx.
..xxx..
""",

"INVADER2":
"""
...xx...
..xxxx..
.xxxxxx.
xx.xx.xx
xxxxxxxx
.x.xx.x.
x......x
.x....x.
""",
"INVADER2":
"""
...xx...
..xxxx..
.xxxxxx.
xx.xx.xx
xxxxxxxx
..x..x..
.x.xx.x.
x.x..x.x
""",

"INVADER3":
"""
..x.....x..
...x...x...
..xxxxxxx..
.xx.xxx.xx.
xxxxxxxxxxx
x.xxxxxxx.x
x.x.....x.x
...xx.xx...
""",

"UFO":
"""
......xxxx......
...xxxxxxxxxx...
..xxxxxxxxxxxx..
.xx.xx.xx.xx.xx.
xxxxxxxxxxxxxxxx
..xxx..xx..xxx..
...x........x...
""",
"PALMTREE":
"""
.x.x.
x.x.x
.xxx.
x.x.x
..x..
""",
"HOUSE":
"""
..x..
.xxx.
xxxxx
xx.xx
xx.xx
""",
"CAR":
"""
.xxx.
xxxxx
.x.x.
""",
"PUPPYFACE":
"""
.xxx.
x.x.x
.x.x.
..x..
""",
"CHERRIES":
"""
..x......
.x.x.....
.x.x.....
.x..x....
.x...xxx.
.xx..xxxx
xxxx.xxxx
xxxx..xx.
.xx......
""",

"W":
"""
x,,,,.x
x..x..x
.x.x.x.
..xxx..
""",
"FLOWER":
"""
.x.x.
xx.xx
..x..
xx.xx
.x.x.
""",
"HEART":
"""
.x...x.
xxx.xxx
xxxxxxx
.xxxxx.
..xxx..
...x...
""",
"CANADA":
"""
....x....
...xxx...
.x.xxx.x.
xxxxxxxxx
.xxxxxxx.
..xxxxx..
.xxxxxxx.
....x....
""",
"TETRISL":
"""
x.
x.
xx
""",
"TETRISJ":
"""
.x
.x
xx
""",

"TETRISS":
"""
.xx
xx.
""",
"TETRISZ":
"""
xx.
.xx
""",

"TETRIST":
"""
xxx
.x.
""",
"TETRISO":
"""
xx
xx
""",
"TETRISI":
"""
x
x
x
x
""",

"CORNER":
"""
x.
xx
""",
"INFINITE":
"""
.x.x.
x.x.x
x.x.x
.x.x.
""",
"COMB":
"""
.xxxxx.
x.x.x.x
""",
"KEY":
"""
.xxx.
x...x
x...x
.xxx.
..x..
..x..
.xx..
..x..
.xx..
""",
"BOTTLE":
"""
.x.
.x.
xxx
xxx
xxx
xxx
""",

"PI":
"""
xxxxx
.x.x.
.x.x.
""",

"STAIRS":
"""
x..
xx.
xxx
""",

"Y":
"""
x...x
.x.x.
..x..
..x..
""",
"ANGEL":
"""
....x..
.xx.xx.
.xxxxxx
..x.x..
xxxxx..
.xx....
..x....
""",
"GULL":
"""
.xx.xx.
x..x..x
""",
"JOYPAD":
"""
..xxx..
..x.x..
xxxxxxx
x.x.x.x
xxxxxxx
..x.x..
..xxx..
""",
"GLIDER":
"""
.x.
..x
xxx
""",
"CRAB":
"""
.xxxx.
x.xx.x
.xxxx.
x....x
.x..x.
""",
"PENTF":
"""
.xx
xx.
.x.
""",

"PENTF2":
"""
xx.
.xx
.x.
""",

"PENTI":
"""
x
x
x
x
x
""",

"PENTL":
"""
x.
x.
x.
xx
""",

"PENTJ":
"""
.x
.x
.x
xx
""",

"PENTN":
"""
.x
.x
xx
x.
""",

"PENTN2":
"""
x.
x.
xx
.x
""",

"PENTP":
"""
xx
xx
x.
""",

"PENTQ":
"""
xx
xx
.x
""",

"PENTT":
"""
xxx
.x.
.x.
""",

"PENTU":
"""
x.x
xxx
""",

"PENTV":
"""
x..
x..
xxx
""",
"PENTW":
"""
x..
xx.
.xx
""",
"PENTX":
"""
.x.
xxx
.x.
""",
"PENTY":
"""
.x
xx
.x
.x
""",
"PENTY2":
"""
x.
xx
x.
x.
""",
"PENTZ":
"""
xx.
.x.
.xx
""",
"PENTS":
"""
.xx
.x.
xx.
"""
}
sprites_db = get_sprites(spritedesc)



__doc__ ="""

``spriteland.sprites`` contains one field, ``sprites_db`` that maps a name to a
:class:`Sprite <spriteland.sprite.Sprite>` object. The supported sprites, along with
their names, are as follows (<space> = 0 and x = 1):

""" #+ "\n".join(["  " + line for line in spritedesc.split("\n")])

for name, sprite in sorted(sprites_db.iteritems()):
    name = name.lower()
    __doc__ += ".. _sprite_%s:\n\n" % name
    __doc__ += ".. parsed-literal::\n\n"
    __doc__ += "\n".join("  " + line for line in str(sprite).split("\n"))
    __doc__ += "\n\n"



# PYRAMID
# x.x.x
# x.x..
# x.xxx
# x....
# xxxxx


#import pprint as pp
#pp.pprint(sprites_db)

#sprites = get_sprites(spritedesc)

#b = sprites['TETRISL']
# print b
# print b.rotate(90)
# print b.rotate(180)
# print b.rotate(270)
# print b.scale(3)
# print b.scale(3, 1)
# print b.hflip()
# print b.vflip()
