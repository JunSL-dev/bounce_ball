'''
b = normal block
p = player
s = star
l = linear block to left
r = linear block to right
e = easy block
k = skill block
'''

levels = [
    [
        "                              ",
        "                              ",
        "                              ",
        "b                             ",
        "b                             ",
        "b p                           ",
        "b                             ",
        "bbbb bb  bb bb                ",
        "                              ",
        "                              ",
        "b               l            b",
        "b                            b",
        "                             b",
        "  r                        s b",
        "                           bb ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
    ],
    [
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "   p                          ",
        "  b                           ",
        "  b                           ",
        "   bbb                        ",
        "  b  b                        ",
        "  b  b    s     s             ",
        "  bs     eeeeeeeee  lb        ",
        "   bb   bb bb b b b           ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
    ],
    [
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "             b               b",
        "             b             p b",
        "             b               b",
        "             b            k  b",
        "             b               b",
        "             b           bbbb ",
        "                              ",
        "  b                           ",
        "  bs           s    bbb       ",
        "  bbbe    ks  ebb  b          ",
        "         ebbb   bbb           ",
        "                              ",
        "                              ",
        "                              ",
    ],
    [
        "                              ",
        "                              ",
        "                              ",
        "  b      b        b       b   ",
        "  b      b        b       b   ",
        "  b p                     b   ",
        "  b                       b   ",
        "  bbbbb  b  bbbb  b  bbb  b   ",
        "                          b   ",
        "                          b   ",
        "                          b   ",
        "                        ebb   ",
        "                        ebb   ",
        "                      e ebb   ",
        "                   r    e s   ",
        "                          b   ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
    ],
    [
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "b                             ",
        "b p                           ",
        "b                             ",
        "bbbbb                         ",
        "  b                           ",
        "  b   e e e e r        s      ",
        "                b    lbbb     ",
        "                    b         ",
        "                  lb          ",
        "                              ",
        "  b                           ",
        "  b  b                        ",
        "  b  b                        ",
        "  bs b                        ",
        "  bbbb                        ",
    ],
    [
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "   b                          ",
        "   b                          ",
        "   b                          ",
        "   b                          ",
        "   b                          ",
        "   b    k  p                  ",
        "   b   bb       s   bbb       ",
        "   b       bbbbbbb            ",
        "                              ",
        "                              ",
        "       b             b        ",
        "   r      e       e       l   ",
        "   bbbbbbbbbbbbbbbbbbbbbbbb   ",
    ],
    [
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "   b                          ",
        "   b                          ",
        "   b                          ",
        "   b                          ",
        "   b                          ",
        "   b    k  p                  ",
        "   b   bb           bbb       ",
        "   b       bbbbbbb            ",
        "                              ",
        "                              ",
        "       b             b        ",
        "   r      e       e       l   ",
        "   bbbbbbbbbbbbbbbbbbbbbbbb   ",
    ]
]

# starCount = [1, 3, 3, 1, 5]
starCount = []
stageCount = len(levels)

for level in levels:
    cnt = 0
    for y in level:
        for x in y:
            if x == 's':
                cnt += 1
    if cnt == 0:
        cnt = -1
    starCount.append(cnt)