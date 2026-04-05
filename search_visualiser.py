import marimo

__generated_with = "0.10.9"
app = marimo.App(width="full", app_title="Search Algorithm Visualizer")


@app.cell
def __():
    import marimo as mo
    import time
    import random
    import math
    import json
    return mo, time, random, math, json


@app.cell
def __(mo):
    mo.md(
        r"""
        # 🔍 Search Algorithm Visualizer

        > *A marimo notebook that makes searching algorithms feel alive.*
        > Adjust the controls below — every cell reacts instantly. No re-runs needed.

        ---
        """
    )
    return


@app.cell
def __(mo):
    algo_choice = mo.ui.dropdown(
        options={
            "Linear Search": "linear",
            "Binary Search": "binary",
            "Fibonacci Search": "fibonacci",
            "BST Search": "bst",
            "Ant Colony Optimisation (ACO)": "aco",
        },
        value="Linear Search",
        label="**Algorithm**",
    )

    array_size = mo.ui.slider(
        start=8,
        stop=64,
        step=4,
        value=20,
        label="**Array Size (n)**",
        show_value=True,
    )

    target_pct = mo.ui.slider(
        start=0,
        stop=100,
        step=1,
        value=60,
        label="**Target Position (% through array)**",
        show_value=True,
    )

    speed = mo.ui.slider(
        start=1,
        stop=10,
        step=1,
        value=5,
        label="**Animation Speed**",
        show_value=True,
    )

    mo.hstack(
        [algo_choice, array_size, target_pct, speed],
        justify="start",
        gap=2,
    )
    return algo_choice, array_size, target_pct, speed


@app.cell
def __(array_size, target_pct, random):
    # Generate sorted array and target
    _n = array_size.value
    _arr = sorted(random.sample(range(1, _n * 5), _n))
    _target_idx = max(0, min(_n - 1, int((_n - 1) * target_pct.value / 100)))
    arr = _arr
    target = _arr[_target_idx]
    return arr, target


@app.cell
def __(algo_choice, arr, target, math):
    # ── Algorithm implementations ──────────────────────────────────────────────
    def linear_search(arr, target):
        steps = []
        for i, val in enumerate(arr):
            steps.append({
                "checked": list(range(i + 1)),
                "current": i,
                "found": val == target,
                "label": f"Checking index {i} → value {val}",
            })
            if val == target:
                steps[-1]["result"] = i
                break
        return steps

    def binary_search(arr, target):
        steps = []
        lo, hi = 0, len(arr) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            steps.append({
                "lo": lo, "hi": hi, "mid": mid,
                "checked": list(range(lo, hi + 1)),
                "current": mid,
                "found": arr[mid] == target,
                "label": f"lo={lo} hi={hi} mid={mid} → value {arr[mid]}",
            })
            if arr[mid] == target:
                steps[-1]["result"] = mid
                break
            elif arr[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return steps

    def fibonacci_search(arr, target):
        n = len(arr)
        steps = []
        # Build fibonacci numbers up to n
        fibs = [0, 1]
        while fibs[-1] < n:
            fibs.append(fibs[-1] + fibs[-2])
        fib_k = len(fibs) - 1
        offset = -1
        while fibs[fib_k] > 1:
            i = min(offset + fibs[fib_k - 2], n - 1)
            active = list(range(max(0, offset + 1), min(n, offset + fibs[fib_k] + 1)))
            steps.append({
                "checked": active,
                "current": i,
                "found": arr[i] == target,
                "label": f"Fib window [{max(0,offset+1)}…{min(n-1, offset+fibs[fib_k])}], checking index {i} → {arr[i]}",
            })
            if arr[i] == target:
                steps[-1]["result"] = i
                break
            elif arr[i] < target:
                fib_k -= 1
                offset = i
            else:
                fib_k -= 2
        else:
            if fibs[fib_k] and offset + 1 < n and arr[offset + 1] == target:
                steps.append({
                    "checked": [offset + 1],
                    "current": offset + 1,
                    "found": True,
                    "result": offset + 1,
                    "label": f"Last check index {offset+1} → {arr[offset+1]}",
                })
        return steps

    def bst_search(arr, target):
        # Simulate BST built from sorted array (like a balanced BST)
        steps = []
        def build_node(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            return {"idx": mid, "left": build_node(lo, mid - 1), "right": build_node(mid + 1, hi)}

        root = build_node(0, len(arr) - 1)

        def search_node(node, path):
            if node is None:
                return
            path = path + [node["idx"]]
            steps.append({
                "checked": path,
                "current": node["idx"],
                "found": arr[node["idx"]] == target,
                "label": f"BST node index {node['idx']} → value {arr[node['idx']]}",
            })
            if arr[node["idx"]] == target:
                steps[-1]["result"] = node["idx"]
                return
            elif target < arr[node["idx"]]:
                search_node(node["left"], path)
            else:
                search_node(node["right"], path)

        search_node(root, [])
        return steps

    def aco_search(arr, target, n_ants=6, iterations=4):
        """
        Simplified ACO for search: ants probabilistically select indices
        guided by pheromone. Pheromone is deposited more near the found index.
        Educational approximation — shows the flavour of ACO.
        """
        import random as _r
        n = len(arr)
        pheromone = [1.0] * n
        steps = []
        found_idx = None

        for it in range(iterations):
            ant_positions = []
            for ant in range(n_ants):
                total = sum(pheromone)
                probs = [p / total for p in pheromone]
                # Weighted random choice
                r = _r.random()
                cumulative = 0
                chosen = 0
                for idx, p in enumerate(probs):
                    cumulative += p
                    if r <= cumulative:
                        chosen = idx
                        break
                ant_positions.append(chosen)
                if arr[chosen] == target:
                    found_idx = chosen

            # Update pheromone
            evap = 0.5
            pheromone = [p * (1 - evap) for p in pheromone]
            for pos in ant_positions:
                closeness = 1 / (1 + abs(arr[pos] - target))
                pheromone[pos] += closeness * 2

            steps.append({
                "checked": list(set(ant_positions)),
                "current": ant_positions[-1],
                "found": found_idx is not None,
                "label": f"Iteration {it+1}: {n_ants} ants explored {sorted(set(ant_positions))}",
                "ants": ant_positions,
                "pheromone": [round(p, 2) for p in pheromone],
            })
            if found_idx is not None:
                steps[-1]["result"] = found_idx
                break

        return steps

    algo_map = {
        "linear": linear_search,
        "binary": binary_search,
        "fibonacci": fibonacci_search,
        "bst": bst_search,
        "aco": aco_search,
    }

    algo_key = algo_choice.value
    steps = algo_map[algo_key](arr, target)
    return algo_map, algo_key, steps, linear_search, binary_search, fibonacci_search, bst_search, aco_search


@app.cell
def __(mo, steps, arr, target, algo_choice, speed):
    # ── Step navigator ─────────────────────────────────────────────────────────
    step_slider = mo.ui.slider(
        start=0,
        stop=max(0, len(steps) - 1),
        step=1,
        value=len(steps) - 1,
        label=f"**Step** (of {len(steps)})",
        show_value=True,
    )

    mo.md(f"""
    ---
    ## 🎬 Step-by-step: {algo_choice.selected_key}

    Searching for **{target}** in array of {len(arr)} elements · {len(steps)} steps taken

    Use the slider to walk through each comparison:
    """)
    return step_slider,


@app.cell
def __(step_slider):
    step_slider
    return


@app.cell
def __(step_slider, steps, arr, target, mo):
    import html as _html

    current_step = steps[step_slider.value]
    checked_set = set(current_step.get("checked", []))
    current_idx = current_step.get("current", -1)
    found = current_step.get("found", False)
    result_idx = current_step.get("result", None)
    ants = current_step.get("ants", None)

    # Build array visualization as HTML
    cells_html = []
    for _i, _val in enumerate(arr):
        if _i == result_idx and found:
            bg = "#22c55e"
            color = "#fff"
            border = "3px solid #16a34a"
            glyph = "✓"
        elif _i == current_idx:
            bg = "#f59e0b"
            color = "#1c1917"
            border = "3px solid #d97706"
            glyph = "👁"
        elif _i in checked_set:
            bg = "#3b82f6"
            color = "#fff"
            border = "2px solid #2563eb"
            glyph = ""
        else:
            bg = "#1e293b"
            color = "#94a3b8"
            border = "2px solid #334155"
            glyph = ""

        ant_marker = ""
        if ants and _i in ants:
            ant_marker = f'<div style="font-size:10px;position:absolute;top:-16px;left:50%;transform:translateX(-50%)">🐜</div>'

        cells_html.append(f"""
        <div style="
            position:relative;
            display:inline-flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            width:44px; height:52px;
            background:{bg};
            border:{border};
            border-radius:6px;
            margin:2px;
            font-family:'JetBrains Mono',monospace;
            font-size:12px;
            font-weight:600;
            color:{color};
            transition:all 0.2s;
        ">
            {ant_marker}
            <span style="font-size:10px;opacity:0.6">{_i}</span>
            <span>{_val}</span>
            <span style="font-size:10px">{glyph}</span>
        </div>
        """)

    array_html = f"""
    <div style="
        background:#0f172a;
        border:1px solid #1e293b;
        border-radius:12px;
        padding:20px 16px;
        overflow-x:auto;
        font-family:'JetBrains Mono',monospace;
    ">
        <div style="display:flex;flex-wrap:wrap;gap:2px;align-items:flex-end;min-height:80px">
            {''.join(cells_html)}
        </div>
        <div style="margin-top:14px;display:flex;gap:16px;font-size:12px;color:#64748b">
            <span>🟦 Checked</span>
            <span>🟨 Current</span>
            <span>🟩 Found</span>
            <span>⬛ Unsearched</span>
        </div>
    </div>
    """

    pheromone_bar = ""
    if "pheromone" in current_step:
        ph = current_step["pheromone"]
        max_ph = max(ph) if ph else 1
        bars = "".join([
            f'<div style="width:6px;height:{int(40*p/max_ph)+4}px;background:rgba(251,191,36,{0.3+0.7*p/max_ph});border-radius:2px 2px 0 0;margin:0 1px" title="idx {i}: {p}"></div>'
            for i, p in enumerate(ph)
        ])
        pheromone_bar = f"""
        <div style="margin-top:12px;color:#94a3b8;font-size:11px;font-family:'JetBrains Mono',monospace">
            Pheromone intensity ↓
            <div style="display:flex;align-items:flex-end;margin-top:4px;height:48px">{bars}</div>
        </div>
        """

    status_color = "#22c55e" if found else "#f59e0b"
    status_text = f"✅ Found {target} at index {result_idx}!" if found else f"🔍 {current_step.get('label', '')}"

    mo.Html(f"""
    {array_html}
    {pheromone_bar}
    <div style="
        margin-top:12px;
        padding:10px 16px;
        background:#0f172a;
        border-left:3px solid {status_color};
        border-radius:0 8px 8px 0;
        color:{status_color};
        font-family:'JetBrains Mono',monospace;
        font-size:13px;
    ">
        {_html.escape(status_text)}
    </div>
    """)
    return (
        array_html,
        ant_marker,
        ants,
        cells_html,
        checked_set,
        current_idx,
        current_step,
        found,
        pheromone_bar,
        result_idx,
        status_color,
        status_text,
    )


@app.cell
def __(mo):
    mo.md("""
    ---
    ## 📊 Live Benchmark: Actual Time vs Input Size

    Runs each algorithm 30 times per n, averages the result. Drag the array size slider above to see this update instantly.
    """)
    return


@app.cell
def __(array_size, linear_search, binary_search, fibonacci_search, bst_search, aco_search, time, random):
    import statistics as _stats

    def _bench(fn, n, runs=30):
        arr_b = sorted(random.sample(range(1, n * 5), n))
        target_b = arr_b[random.randint(0, n - 1)]
        times = []
        for _ in range(runs):
            t0 = time.perf_counter()
            fn(arr_b, target_b)
            times.append((time.perf_counter() - t0) * 1e6)  # microseconds
        return round(_stats.mean(times), 4)

    bench_sizes = [8, 16, 32, 64, 128, 256, 512, array_size.value]
    bench_sizes = sorted(set(bench_sizes))

    bench_results = {}
    for _algo_name, _fn in [
        ("Linear", linear_search),
        ("Binary", binary_search),
        ("Fibonacci", fibonacci_search),
        ("BST", bst_search),
        ("ACO", aco_search),
    ]:
        bench_results[_algo_name] = {n: _bench(_fn, n) for n in bench_sizes}
    return bench_results, bench_sizes, _bench, _stats


@app.cell
def __(bench_results, bench_sizes, mo, math):
    # Build SVG chart
    colors = {
        "Linear": "#ef4444",
        "Binary": "#3b82f6",
        "Fibonacci": "#a855f7",
        "BST": "#22c55e",
        "ACO": "#f59e0b",
    }

    W, H = 680, 320
    pad_l, pad_r, pad_t, pad_b = 60, 24, 24, 48

    all_times = [t for algo in bench_results.values() for t in algo.values()]
    max_t = max(all_times) * 1.1
    min_t = 0
    max_n = max(bench_sizes)
    min_n = min(bench_sizes)

    def x_pos(n):
        return pad_l + (math.log2(n) - math.log2(min_n)) / (math.log2(max_n) - math.log2(min_n)) * (W - pad_l - pad_r)

    def y_pos(t):
        return pad_t + (1 - (t - min_t) / (max_t - min_t)) * (H - pad_t - pad_b)

    # Grid lines
    grid = ""
    for _t_tick in [0, max_t * 0.25, max_t * 0.5, max_t * 0.75, max_t]:
        _y = y_pos(_t_tick)
        grid += f'<line x1="{pad_l}" y1="{_y:.1f}" x2="{W - pad_r}" y2="{_y:.1f}" stroke="#1e293b" stroke-width="1"/>'
        grid += f'<text x="{pad_l - 6}" y="{_y + 4:.1f}" text-anchor="end" fill="#475569" font-size="10" font-family="JetBrains Mono,monospace">{_t_tick:.1f}</text>'

    for _n in bench_sizes:
        _x = x_pos(_n)
        grid += f'<line x1="{_x:.1f}" y1="{pad_t}" x2="{_x:.1f}" y2="{H - pad_b}" stroke="#1e293b" stroke-width="1"/>'
        grid += f'<text x="{_x:.1f}" y="{H - pad_b + 16}" text-anchor="middle" fill="#475569" font-size="10" font-family="JetBrains Mono,monospace">{_n}</text>'

    # Lines + dots
    lines_svg = ""
    for _name, _data in bench_results.items():
        _pts = [(x_pos(n), y_pos(t)) for n, t in sorted(_data.items())]
        _path = " ".join([f"{'M' if i == 0 else 'L'}{px:.1f},{py:.1f}" for i, (px, py) in enumerate(_pts)])
        lines_svg += f'<path d="{_path}" fill="none" stroke="{colors[_name]}" stroke-width="2.5" stroke-linejoin="round"/>'
        for _px, _py in _pts:
            lines_svg += f'<circle cx="{_px:.1f}" cy="{_py:.1f}" r="4" fill="{colors[_name]}" stroke="#0f172a" stroke-width="2"/>'

    # Legend
    legend = ""
    for _i, (_name, _col) in enumerate(colors.items()):
        _lx = pad_l + _i * 128
        legend += f'<rect x="{_lx}" y="{H - 14}" width="14" height="6" rx="3" fill="{_col}"/>'
        legend += f'<text x="{_lx + 18}" y="{H - 8}" fill="{_col}" font-size="11" font-family="JetBrains Mono,monospace">{_name}</text>'

    chart_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" style="background:#0f172a;border-radius:12px;border:1px solid #1e293b;width:100%">
        {grid}
        {lines_svg}
        {legend}
        <text x="{pad_l - 40}" y="{H // 2}" text-anchor="middle" fill="#64748b" font-size="11" font-family="JetBrains Mono,monospace" transform="rotate(-90,{pad_l-40},{H//2})">Time (μs)</text>
        <text x="{W // 2}" y="{H - 2}" text-anchor="middle" fill="#64748b" font-size="11" font-family="JetBrains Mono,monospace">Array Size n (log scale)</text>
    </svg>"""

    mo.Html(chart_svg)
    return (
        H,
        W,
        all_times,
        chart_svg,
        colors,
        grid,
        legend,
        lines_svg,
        max_n,
        max_t,
        min_n,
        min_t,
        pad_b,
        pad_l,
        pad_r,
        pad_t,
        x_pos,
        y_pos,
    )


@app.cell
def __(mo):
    mo.md("""
    ---
    ## 🗂 Comparison Table: All Algorithms Side by Side
    """)
    return


@app.cell
def __(bench_results, bench_sizes, steps, algo_choice, arr, target, mo):
    algo_key_current = algo_choice.value

    complexity_map = {
        "linear": ("O(1)", "O(n)", "O(n)", "O(1)", "Sequential scan, no preprocessing needed"),
        "binary": ("O(1)", "O(log n)", "O(log n)", "O(1)", "Requires sorted array, halves search space each step"),
        "fibonacci": ("O(1)", "O(log n)", "O(log n)", "O(1)", "Uses Fibonacci numbers to divide; cache-friendly access pattern"),
        "bst": ("O(log n)", "O(log n)", "O(n)", "O(n)", "Tree built once; worst case O(n) on unbalanced tree"),
        "aco": ("O(k·n)", "O(k·n)", "O(k·n)", "O(n)", "Probabilistic; good for combinatorial spaces, overkill for arrays"),
    }

    algo_display = {
        "linear": "Linear Search",
        "binary": "Binary Search",
        "fibonacci": "Fibonacci Search",
        "bst": "BST Search",
        "aco": "Ant Colony Opt.",
    }

    rows = []
    for _key, _label in algo_display.items():
        _best, _avg, _worst, _space, _note = complexity_map[_key]
        _steps_count = len(steps) if _key == algo_key_current else "—"
        _highlight = "🎯 " if _key == algo_key_current else ""
        rows.append({
            "Algorithm": f"{_highlight}{_label}",
            "Best": _best,
            "Average": _avg,
            "Worst": _worst,
            "Space": _space,
            f"Steps (n={len(arr)}, t={target})": _steps_count,
            "Notes": _note,
        })

    mo.ui.table(rows, selection=None)
    return algo_display, algo_key_current, complexity_map, rows


@app.cell
def __(mo):
    mo.md("""
    ---
    ## 🧠 Theoretical Complexity Overlay

    How do O(1), O(log n), O(n), O(n log n) scale? Plotted against realistic n values.
    """)
    return


@app.cell
def __(mo, math):
    _ns = [2**i for i in range(1, 11)]  # 2 to 1024
    _curves = {
        "O(1)": [(n, 1) for n in _ns],
        "O(log n)": [(n, math.log2(n)) for n in _ns],
        "O(n)": [(n, n) for n in _ns],
        "O(n log n)": [(n, n * math.log2(n)) for n in _ns],
        "O(n²)": [(n, n * n) for n in _ns],
    }
    _colors2 = {
        "O(1)": "#22c55e",
        "O(log n)": "#3b82f6",
        "O(n)": "#f59e0b",
        "O(n log n)": "#a855f7",
        "O(n²)": "#ef4444",
    }

    _W, _H = 680, 300
    _pl, _pr, _pt, _pb = 60, 24, 20, 48
    _max_n = max(_ns)
    _max_y = max(n * math.log2(n) for n in _ns) * 1.05

    def _xp(n): return _pl + (math.log2(n) - 1) / (math.log2(_max_n) - 1) * (_W - _pl - _pr)
    def _yp(y): return _pt + (1 - y / _max_y) * (_H - _pt - _pb)

    _grid2 = ""
    for _tick in [0, _max_y * 0.25, _max_y * 0.5, _max_y * 0.75, _max_y]:
        _gy = _yp(_tick)
        _grid2 += f'<line x1="{_pl}" y1="{_gy:.1f}" x2="{_W-_pr}" y2="{_gy:.1f}" stroke="#1e293b" stroke-width="1"/>'
        _grid2 += f'<text x="{_pl-6}" y="{_gy+4:.1f}" text-anchor="end" fill="#475569" font-size="10" font-family="JetBrains Mono,monospace">{int(_tick)}</text>'

    for _n2 in _ns[::2]:
        _gx = _xp(_n2)
        _grid2 += f'<text x="{_gx:.1f}" y="{_H-_pb+16}" text-anchor="middle" fill="#475569" font-size="10" font-family="JetBrains Mono,monospace">{_n2}</text>'

    _paths2 = ""
    for _cname, _pts2 in _curves.items():
        _d = " ".join([f"{'M' if i==0 else 'L'}{_xp(n):.1f},{_yp(y):.1f}" for i,(n,y) in enumerate(_pts2)])
        _paths2 += f'<path d="{_d}" fill="none" stroke="{_colors2[_cname]}" stroke-width="2" stroke-linejoin="round"/>'
        _ex, _ey = _xp(_pts2[-1][0]), _yp(_pts2[-1][1])
        _paths2 += f'<text x="{_ex+5}" y="{_ey+4:.1f}" fill="{_colors2[_cname]}" font-size="11" font-family="JetBrains Mono,monospace">{_cname}</text>'

    _chart2 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_W} {_H}" style="background:#0f172a;border-radius:12px;border:1px solid #1e293b;width:100%">
        {_grid2}{_paths2}
        <text x="{_pl-40}" y="{_H//2}" text-anchor="middle" fill="#64748b" font-size="11" font-family="JetBrains Mono,monospace" transform="rotate(-90,{_pl-40},{_H//2})">Operations</text>
        <text x="{_W//2}" y="{_H-2}" text-anchor="middle" fill="#64748b" font-size="11" font-family="JetBrains Mono,monospace">n (log scale)</text>
    </svg>"""

    mo.Html(_chart2)
    return


@app.cell
def __(mo, algo_choice):
    _insights = {
        "linear": ("🔴 Linear", "This is your baseline. Simple and always correct, but O(n) means doubling n doubles the work. No preprocessing, no prerequisites."),
        "binary": ("🔵 Binary", "The classic divide-and-conquer. Requires sorted input, but slashes comparisons from n to log₂(n). At n=1M, that's 1M vs 20 comparisons."),
        "fibonacci": ("🟣 Fibonacci", "Like binary search but uses Fibonacci splits instead of halves. Avoids division, making it cache-friendly on certain hardware. Rarely used in practice but elegant in theory."),
        "bst": ("🟢 BST", "Build a tree once, search it O(log n) forever — until it degenerates into a linked list. Self-balancing variants (AVL, Red-Black) fix this."),
        "aco": ("🟡 ACO (Ant Colony)", "A metaheuristic from nature. Completely overkill for 1D array search. Its power emerges in combinatorial spaces — TSP, routing, scheduling — where no closed-form solution exists."),
    }
    _name, _text = _insights[algo_choice.value]
    mo.callout(mo.md(f"**{_name} Search** — {_text}"), kind="info")
    return


@app.cell
def __(mo):
    mo.md("""
    ---
    > **Why marimo?** Every cell above is reactive. Change the algorithm dropdown or drag the array size slider —
    > the step visualizer, benchmark chart, comparison table, and callout all update *simultaneously* without a single re-run.
    > In Colab, you'd be hitting `Runtime → Run All` right now.
    >
    > Built with [marimo](https://marimo.io) · Deploy with `marimo run search_visualizer.py`
    """)
    return


if __name__ == "__main__":
    app.run()