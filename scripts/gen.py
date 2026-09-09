import random, re
from pathlib import Path


W, H, ND = 160, 40, 400
README = Path("README.md")
START = "<!-- TOTD:BEGIN -->"
END = "<!-- TOTD:END -->"
DIR = [(0, -1, 1, 4), (1, 0, 2, 8), (0, 1, 4, 1), (-1, 0, 8, 2)]
BOX = " ╵╶└╷│┌├╴┘─┴┐┤┬┼"


def gt():
    grid = [[0] * W for _ in range(H)]
    root = (W // 2, H // 2)
    occ, vis = [root], {root}
    for _ in range(ND):
        random.shuffle(occ)
        for x, y in occ:
            add = 0
            dirs = DIR[:]
            random.shuffle(dirs)
            for dx, dy, cb, nb in dirs:
                nx, ny = x + dx, y + dy
                npos = (nx, ny)
                if not (0 < nx < W - 1 and 0 < ny < H - 1):
                    continue
                if npos in vis:
                    continue
                grid[y][x] |= cb
                grid[ny][nx] |= nb
                vis.add(npos)
                occ.append(npos)
                add = 1
                break
            ## try other occ node
            if not add:
                continue
            ## added node, go next
            break

    ## rm ws
    xs = [x for x, _ in vis]
    ys = [y for _, y in vis]
    mnx, mxx = min(xs), max(xs)
    mny, mxy = min(ys), max(ys)
    lns = []

    ## add left margin
    for y in range(mny, mxy + 1):
        ln = " "
        for x in range(mnx, mxx + 1):
            if (x, y) == root:
                ln += "●"
            else:
                ln += BOX[grid[y][x]]
        lns.append(ln.rstrip())
    return "\n".join(lns)


def upd(tree):
    txt = README.read_text()
    replacement = f"{START}\n```text\n{tree}\n```\n{END}"
    utxt = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        replacement, txt, flags = re.DOTALL,
    )
    README.write_text(utxt)


if __name__ == "__main__":
    upd(gt())