import marimo

__generated_with = "0.10.9"
app = marimo.App(width="full", app_title="Search Algorithm Visualizer")


@app.cell
def __():
    import marimo as mo
    import time
    import random
    import math
    import statistics
    return mo, time, random, math, statistics


@app.cell
def __(mo):
    mo.Html("""
    <div style="padding:40px 0 24px;border-bottom:1px solid #1e293b;margin-bottom:8px">
        <span style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.12em;color:#475569;text-transform:uppercase">marimo · interactive</span>
        <h1 style="margin:8px 0 6px;font-size:2.4rem;font-weight:700;letter-spacing:-0.03em;color:#f1f5f9;font-family:'JetBrains Mono',monospace">
            Search Algorithm Visualizer
        </h1>
        <p style="margin:0;color:#64748b;font-size:14px;font-family:'JetBrains Mono',monospace">
            Five algorithms · reactive cells · zero re-runs
        </p>
    </div>
    """)
    return


@app.cell
def __(mo):
    algo_choice = mo.ui.dropdown(
        options={
            "Linear Search":           "linear",
            "Binary Search":           "binary",
            "Fibonacci Search":        "fibonacci",
            "BST Search":              "bst",
            "Ant Colony Optimisation": "aco",
        },
        value="Linear Search",
        label="Algorithm",
    )
    array_size = mo.ui.slider(start=8, stop=64, step=4, value=20, label="Array size  n", show_value=True)
    target_pct = mo.ui.slider(start=0, stop=100, step=1, value=60, label="Target position  %", show_value=True)
    mo.hstack([algo_choice, array_size, target_pct], justify="start", gap=3)
    return algo_choice, array_size, target_pct


@app.cell
def __(array_size, target_pct, random):
    _n   = array_size.value
    _arr = sorted(random.sample(range(1, _n * 5), _n))
    _idx = max(0, min(_n - 1, int((_n - 1) * target_pct.value / 100)))
    arr    = _arr
    target = _arr[_idx]
    return arr, target


@app.cell
def __(algo_choice, arr, target):
    def linear_search(arr, target):
        steps = []
        for i, val in enumerate(arr):
            steps.append({"checked": list(range(i + 1)), "current": i, "found": val == target, "label": f"index {i}  →  {val}"})
            if val == target:
                steps[-1]["result"] = i
                break
        return steps

    def binary_search(arr, target):
        steps = []
        lo, hi = 0, len(arr) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            steps.append({"checked": list(range(lo, hi + 1)), "current": mid, "found": arr[mid] == target, "label": f"lo={lo}  mid={mid}  hi={hi}  →  {arr[mid]}"})
            if arr[mid] == target:
                steps[-1]["result"] = mid
                break
            elif arr[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return steps

    def fibonacci_search(arr, target):
        n, steps = len(arr), []
        fibs = [0, 1]
        while fibs[-1] < n:
            fibs.append(fibs[-1] + fibs[-2])
        fib_k, offset = len(fibs) - 1, -1
        while fibs[fib_k] > 1:
            i      = min(offset + fibs[fib_k - 2], n - 1)
            active = list(range(max(0, offset + 1), min(n, offset + fibs[fib_k] + 1)))
            steps.append({"checked": active, "current": i, "found": arr[i] == target, "label": f"window [{max(0,offset+1)}…{min(n-1,offset+fibs[fib_k])}]  probe {i}  →  {arr[i]}"})
            if arr[i] == target:
                steps[-1]["result"] = i
                break
            elif arr[i] < target:
                fib_k -= 1; offset = i
            else:
                fib_k -= 2
        else:
            if fibs[fib_k] and offset + 1 < n and arr[offset + 1] == target:
                steps.append({"checked": [offset + 1], "current": offset + 1, "found": True, "result": offset + 1, "label": f"final probe {offset+1}  →  {arr[offset+1]}"})
        return steps

    def bst_search(arr, target):
        steps = []
        def build_node(lo, hi):
            if lo > hi: return None
            mid = (lo + hi) // 2
            return {"idx": mid, "left": build_node(lo, mid - 1), "right": build_node(mid + 1, hi)}
        def search_node(node, path):
            if node is None: return
            path = path + [node["idx"]]
            steps.append({"checked": path, "current": node["idx"], "found": arr[node["idx"]] == target, "label": f"node {node['idx']}  →  {arr[node['idx']]}"})
            if arr[node["idx"]] == target:
                steps[-1]["result"] = node["idx"]; return
            elif target < arr[node["idx"]]: search_node(node["left"], path)
            else: search_node(node["right"], path)
        search_node(build_node(0, len(arr) - 1), [])
        return steps

    def aco_search(arr, target, n_ants=6, iterations=4):
        import random as _r
        n, pheromone, steps, found_idx = len(arr), [1.0] * len(arr), [], None
        for it in range(iterations):
            ant_positions = []
            for _ in range(n_ants):
                total = sum(pheromone)
                probs = [p / total for p in pheromone]
                r, cumulative, chosen = _r.random(), 0, 0
                for idx, p in enumerate(probs):
                    cumulative += p
                    if r <= cumulative: chosen = idx; break
                ant_positions.append(chosen)
                if arr[chosen] == target: found_idx = chosen
            pheromone = [p * 0.5 for p in pheromone]
            for pos in ant_positions:
                pheromone[pos] += 2 / (1 + abs(arr[pos] - target))
            steps.append({"checked": list(set(ant_positions)), "current": ant_positions[-1], "found": found_idx is not None, "label": f"iter {it+1}  ·  ants at {sorted(set(ant_positions))}", "ants": ant_positions, "pheromone": [round(p, 2) for p in pheromone]})
            if found_idx is not None:
                steps[-1]["result"] = found_idx; break
        return steps

    algo_map = {"linear": linear_search, "binary": binary_search, "fibonacci": fibonacci_search, "bst": bst_search, "aco": aco_search}
    steps = algo_map[algo_choice.value](arr, target)
    return algo_map, steps, linear_search, binary_search, fibonacci_search, bst_search, aco_search


@app.cell
def __(mo, steps, arr, target, algo_choice):
    step_slider = mo.ui.slider(start=0, stop=max(0, len(steps) - 1), step=1, value=len(steps) - 1, label="Step", show_value=True)
    mo.Html(f"""
    <div style="margin-top:32px;margin-bottom:4px;display:flex;align-items:center;justify-content:space-between">
        <div>
            <span style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;color:#e2e8f0">{algo_choice.selected_key}</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#475569;margin-left:16px">
                target <b style="color:#fbbf24">{target}</b> &nbsp;·&nbsp; n={len(arr)} &nbsp;·&nbsp; {len(steps)} steps
            </span>
        </div>
        <div style="display:flex;gap:6px;font-size:11px;font-family:'JetBrains Mono',monospace">
            <span style="padding:2px 10px;border-radius:999px;background:#1e3a5f;color:#60a5fa">checked</span>
            <span style="padding:2px 10px;border-radius:999px;background:#422006;color:#fbbf24">current</span>
            <span style="padding:2px 10px;border-radius:999px;background:#14532d;color:#4ade80">found</span>
        </div>
    </div>
    """)
    return step_slider,


@app.cell
def __(step_slider):
    step_slider
    return


@app.cell
def __(step_slider, steps, arr, target, mo):
    import html as _html
    _s       = steps[step_slider.value]
    _checked = set(_s.get("checked", []))
    _current = _s.get("current", -1)
    _found   = _s.get("found", False)
    _result  = _s.get("result", None)
    _ants    = _s.get("ants", None)

    _cells = []
    for _i, _v in enumerate(arr):
        if _i == _result and _found:
            _bg, _fg, _bd, _gl = "#166534", "#4ade80", "1px solid #16a34a", "✓"
        elif _i == _current:
            _bg, _fg, _bd, _gl = "#422006", "#fbbf24", "1px solid #d97706", "→"
        elif _i in _checked:
            _bg, _fg, _bd, _gl = "#1e3a5f", "#60a5fa", "1px solid #2563eb", ""
        else:
            _bg, _fg, _bd, _gl = "#0f172a", "#334155", "1px solid #1e293b", ""
        _ant = f'<div style="position:absolute;top:-18px;left:50%;transform:translateX(-50%);font-size:11px">🐜</div>' if (_ants and _i in _ants) else ""
        _cells.append(f'<div style="position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;width:46px;height:54px;background:{_bg};border:{_bd};border-radius:8px;font-family:\'JetBrains Mono\',monospace;color:{_fg}">{_ant}<span style="font-size:9px;opacity:0.45;margin-bottom:1px">{_i}</span><span style="font-size:13px;font-weight:700">{_v}</span><span style="font-size:9px;margin-top:1px;opacity:0.8">{_gl}</span></div>')

    _pheromone_html = ""
    if "pheromone" in _s:
        _ph   = _s["pheromone"]
        _mxph = max(_ph) if _ph else 1
        _bars = "".join(f'<div style="width:5px;height:{int(36*p/_mxph)+3}px;background:rgba(251,191,36,{0.2+0.8*p/_mxph});border-radius:2px 2px 0 0" title="{i}:{p}"></div>' for i, p in enumerate(_ph))
        _pheromone_html = f'<div style="margin-top:14px;padding:12px 16px;background:#0f172a;border:1px solid #1e293b;border-radius:8px"><div style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:#475569;margin-bottom:6px;letter-spacing:0.08em;text-transform:uppercase">Pheromone</div><div style="display:flex;align-items:flex-end;gap:2px;height:42px">{_bars}</div></div>'

    _sc = "#4ade80" if _found else "#fbbf24"
    _st = f"Found {target} at index {_result}" if _found else _s.get("label", "")
    mo.Html(f'<div style="background:#0a0f1a;border:1px solid #1e293b;border-radius:12px;padding:20px;overflow-x:auto"><div style="display:flex;flex-wrap:wrap;gap:4px;min-height:72px;align-items:flex-end">{"".join(_cells)}</div>{_pheromone_html}<div style="margin-top:14px;padding:8px 14px;border-left:2px solid {_sc};border-radius:0 6px 6px 0;background:#0f172a;font-family:\'JetBrains Mono\',monospace;font-size:12px;color:{_sc}">{_html.escape(_st)}</div></div>')
    return


@app.cell
def __(mo):
    mo.Html('<div style="margin-top:40px;margin-bottom:4px;font-family:\'JetBrains Mono\',monospace;font-size:13px;font-weight:600;color:#e2e8f0">Benchmark <span style="color:#475569;font-weight:400;font-size:12px">· avg of 30 runs per n</span></div>')
    return


@app.cell
def __(array_size, linear_search, binary_search, fibonacci_search, bst_search, aco_search, time, random, statistics):
    def _bench(fn, n, runs=30):
        a  = sorted(random.sample(range(1, n * 5), n))
        t  = a[random.randint(0, n - 1)]
        ts = []
        for _ in range(runs):
            t0 = time.perf_counter()
            fn(a, t)
            ts.append((time.perf_counter() - t0) * 1e6)
        return round(statistics.mean(ts), 4)

    bench_sizes   = sorted({8, 16, 32, 64, 128, 256, 512, array_size.value})
    bench_results = {
        name: {n: _bench(fn, n) for n in bench_sizes}
        for name, fn in [
            ("Linear", linear_search), ("Binary", binary_search),
            ("Fibonacci", fibonacci_search), ("BST", bst_search), ("ACO", aco_search),
        ]
    }
    return bench_sizes, bench_results


@app.cell
def __(bench_results, bench_sizes, mo, math):
    _colors = {"Linear": "#ef4444", "Binary": "#3b82f6", "Fibonacci": "#a855f7", "BST": "#22c55e", "ACO": "#f59e0b"}
    _W, _H, _pl, _pr, _pt, _pb = 700, 300, 56, 100, 20, 44
    _all  = [t for d in bench_results.values() for t in d.values()]
    _maxt = max(_all) * 1.15
    _maxn, _minn = max(bench_sizes), min(bench_sizes)

    def _xp(n): return _pl + (math.log2(n)-math.log2(_minn))/(math.log2(_maxn)-math.log2(_minn))*(_W-_pl-_pr)
    def _yp(t): return _pt + (1-t/_maxt)*(_H-_pt-_pb)

    _g = ""
    for _t2 in [0, _maxt*0.33, _maxt*0.66, _maxt]:
        _gy = _yp(_t2)
        _g += f'<line x1="{_pl}" y1="{_gy:.1f}" x2="{_W-_pr}" y2="{_gy:.1f}" stroke="#1e293b" stroke-width="1"/>'
        _g += f'<text x="{_pl-8}" y="{_gy+4:.1f}" text-anchor="end" fill="#334155" font-size="10" font-family="JetBrains Mono,monospace">{_t2:.1f}</text>'
    for _n2 in bench_sizes:
        _gx = _xp(_n2)
        _g += f'<line x1="{_gx:.1f}" y1="{_pt}" x2="{_gx:.1f}" y2="{_H-_pb}" stroke="#1e293b" stroke-width="1"/>'
        _g += f'<text x="{_gx:.1f}" y="{_H-_pb+14}" text-anchor="middle" fill="#334155" font-size="10" font-family="JetBrains Mono,monospace">{_n2}</text>'

    _p = ""
    for _nm, _dat in bench_results.items():
        _pts = [((_xp(n)), _yp(t)) for n, t in sorted(_dat.items())]
        _d   = " ".join(f"{'M' if i==0 else 'L'}{px:.1f},{py:.1f}" for i,(px,py) in enumerate(_pts))
        _col = _colors[_nm]
        _p  += f'<path d="{_d}" fill="none" stroke="{_col}" stroke-width="2" stroke-linejoin="round" opacity="0.9"/>'
        for _px, _py in _pts:
            _p += f'<circle cx="{_px:.1f}" cy="{_py:.1f}" r="3.5" fill="{_col}" stroke="#0a0f1a" stroke-width="1.5"/>'

    _leg = ""
    for _li, (_ln, _lc) in enumerate(_colors.items()):
        _ly = _pt + _li * 22
        _leg += f'<rect x="{_W-_pr+12}" y="{_ly}" width="10" height="10" rx="3" fill="{_lc}"/>'
        _leg += f'<text x="{_W-_pr+26}" y="{_ly+9}" fill="{_lc}" font-size="11" font-family="JetBrains Mono,monospace">{_ln}</text>'

    mo.Html(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_W} {_H}" style="background:#0a0f1a;border:1px solid #1e293b;border-radius:12px;width:100%">{_g}{_p}{_leg}<text x="{_pl-44}" y="{_H//2}" text-anchor="middle" fill="#475569" font-size="10" font-family="JetBrains Mono,monospace" transform="rotate(-90,{_pl-44},{_H//2})">μs</text><text x="{_pl+(_W-_pl-_pr)//2}" y="{_H-4}" text-anchor="middle" fill="#475569" font-size="10" font-family="JetBrains Mono,monospace">n (log scale)</text></svg>')
    return


@app.cell
def __(mo):
    mo.Html('<div style="margin-top:40px;margin-bottom:4px;font-family:\'JetBrains Mono\',monospace;font-size:13px;font-weight:600;color:#e2e8f0">Complexity <span style="color:#475569;font-weight:400;font-size:12px">· theoretical growth</span></div>')
    return


@app.cell
def __(mo, math):
    _ns2 = [2**i for i in range(1, 11)]
    _curves = {"O(1)": [(n,1) for n in _ns2], "O(log n)": [(n,math.log2(n)) for n in _ns2], "O(n)": [(n,n) for n in _ns2], "O(n log n)": [(n,n*math.log2(n)) for n in _ns2], "O(n²)": [(n,n*n) for n in _ns2]}
    _cols2  = {"O(1)": "#22c55e", "O(log n)": "#3b82f6", "O(n)": "#f59e0b", "O(n log n)": "#a855f7", "O(n²)": "#ef4444"}
    _W2, _H2, _pl2, _pr2, _pt2, _pb2 = 700, 260, 56, 90, 16, 40
    _maxn2  = max(_ns2)
    _maxy2  = max(n*math.log2(n) for n in _ns2) * 1.08

    def _xp2(n): return _pl2 + (math.log2(n)-1)/(math.log2(_maxn2)-1)*(_W2-_pl2-_pr2)
    def _yp2(y): return _pt2 + (1-y/_maxy2)*(_H2-_pt2-_pb2)

    _g2 = ""
    for _tick2 in [0, _maxy2*0.33, _maxy2*0.66, _maxy2]:
        _gy2 = _yp2(_tick2)
        _g2 += f'<line x1="{_pl2}" y1="{_gy2:.1f}" x2="{_W2-_pr2}" y2="{_gy2:.1f}" stroke="#1e293b" stroke-width="1"/>'
        _g2 += f'<text x="{_pl2-8}" y="{_gy2+4:.1f}" text-anchor="end" fill="#334155" font-size="10" font-family="JetBrains Mono,monospace">{int(_tick2)}</text>'
    for _n3 in _ns2[::2]:
        _gx2 = _xp2(_n3)
        _g2 += f'<text x="{_gx2:.1f}" y="{_H2-_pb2+13}" text-anchor="middle" fill="#334155" font-size="10" font-family="JetBrains Mono,monospace">{_n3}</text>'

    _p2 = ""
    for _cn2, _cpts2 in _curves.items():
        _d2 = " ".join(f"{'M' if i==0 else 'L'}{_xp2(n):.1f},{_yp2(y):.1f}" for i,(n,y) in enumerate(_cpts2))
        _p2 += f'<path d="{_d2}" fill="none" stroke="{_cols2[_cn2]}" stroke-width="2" stroke-linejoin="round"/>'
        _ex2, _ey2 = _xp2(_cpts2[-1][0]), _yp2(_cpts2[-1][1])
        _p2 += f'<text x="{_ex2+4}" y="{_ey2+4:.1f}" fill="{_cols2[_cn2]}" font-size="10" font-family="JetBrains Mono,monospace">{_cn2}</text>'

    mo.Html(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_W2} {_H2}" style="background:#0a0f1a;border:1px solid #1e293b;border-radius:12px;width:100%">{_g2}{_p2}<text x="{_pl2+(_W2-_pl2-_pr2)//2}" y="{_H2-4}" text-anchor="middle" fill="#475569" font-size="10" font-family="JetBrains Mono,monospace">n (log scale)</text></svg>')
    return


@app.cell
def __(mo):
    mo.Html('<div style="margin-top:40px;margin-bottom:4px;font-family:\'JetBrains Mono\',monospace;font-size:13px;font-weight:600;color:#e2e8f0">Comparison</div>')
    return


@app.cell
def __(steps, algo_choice, arr, target, mo):
    _cx = {
        "linear":    ("O(1)",     "O(n)",     "O(n)",     "O(1)", "No preprocessing. Scans left to right."),
        "binary":    ("O(1)",     "O(log n)", "O(log n)", "O(1)", "Requires sorted input. Halves space each step."),
        "fibonacci": ("O(1)",     "O(log n)", "O(log n)", "O(1)", "Fibonacci splits. Cache-friendly memory access."),
        "bst":       ("O(log n)", "O(log n)", "O(n)",     "O(n)", "O(n) worst case on degenerate (unbalanced) tree."),
        "aco":       ("O(k·n)",   "O(k·n)",   "O(k·n)",  "O(n)", "Overkill here. Shines in combinatorial spaces."),
    }
    _lbl = {"linear": "Linear", "binary": "Binary", "fibonacci": "Fibonacci", "bst": "BST", "aco": "ACO"}
    _cur = algo_choice.value
    _rows = []
    for _k, _l in _lbl.items():
        _b, _a, _w, _s, _n = _cx[_k]
        _rows.append({"Algorithm": ("▶  " if _k == _cur else "    ") + _l, "Best": _b, "Avg": _a, "Worst": _w, "Space": _s, f"Steps (n={len(arr)}, t={target})": len(steps) if _k == _cur else "—", "Notes": _n})
    mo.ui.table(_rows, selection=None)
    return


@app.cell
def __(mo, algo_choice):
    _ins = {
        "linear":    "Always correct, no prerequisites. O(n) means every extra element costs linearly — fine for small n.",
        "binary":    "The classic. log₂(n) comparisons means 20 checks suffice for n=1,000,000. Needs sorted input.",
        "fibonacci": "Like binary search but splits by Fibonacci ratios. Avoids division ops — useful on older hardware.",
        "bst":       "Build once, query O(log n) indefinitely. Watch for degenerate inputs — AVL or Red-Black trees fix that.",
        "aco":       "A metaheuristic from swarm intelligence. Overkill for 1D arrays. Beautiful for TSP, routing, and scheduling.",
    }
    mo.callout(mo.md(f"**{algo_choice.selected_key}** — {_ins[algo_choice.value]}"), kind="info")
    return


@app.cell
def __(mo):
    mo.Html("""
    <div style="margin-top:48px;padding:20px 0;border-top:1px solid #1e293b;font-family:'JetBrains Mono',monospace;font-size:11px;color:#334155;display:flex;justify-content:space-between">
        <span>Built with <a href="https://marimo.io" style="color:#475569;text-decoration:underline">marimo</a> · every cell is reactive · no re-runs needed</span>
        <span>marimo run search_visualizer.py</span>
    </div>
    """)
    return


if __name__ == "__main__":
    app.run()