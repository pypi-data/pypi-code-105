"""
Get TaLib Structure Func Doc
"""
__version__ = "0.2"


def get_tadoc(
    use_ta_group: list = [
        "Cycle Indicators",
        "Momentum Indicators",
        "Overlap Studies",
        "Pattern Recognition",
        "Volatility Indicators",
        "Volume Indicators",
    ],
    func_as_key: bool = False,
):
    import ast
    import talib
    import numpy as np

    use_ta_group = [
        g
        for g in talib.get_function_groups().keys()
        if "Indicators" in g or "Pattern" in g or "Overlap" in g
    ]
    talib_group = talib.get_function_groups()
    use_ta = [ta for g in use_ta_group for ta in talib_group[g]]
    ta_docs = {ta: getattr(talib, ta).__doc__ for ta in use_ta}
    if func_as_key:
        ta_parsed = {}
    else:
        ta_parsed = []
    for ta, doc in ta_docs.items():
        doc_lines = [l.strip(" ") for l in doc.split("\n")]
        func_syntax = doc_lines[0]
        input_idx = doc_lines.index("Inputs:") if "Inputs:" in doc_lines else 0
        para_idx = doc_lines.index("Parameters:") if "Parameters:" in doc_lines else 0
        out_idx = doc_lines.index("Outputs:") if "Outputs:" in doc_lines else 0
        input_l = doc_lines[input_idx + 1 : para_idx if para_idx else out_idx]
        para_l = doc_lines[para_idx + 1 : out_idx if para_idx else para_idx + 1]
        output_l = doc_lines[out_idx + 1 if out_idx else out_idx + 1 : -1]
        ninput = []
        for l in input_l:
            lns = l.split(": ")
            t = lns[1]
            if t == "(any ndarray)":
                t = np.ndarray
                i = {lns[0]: t}
                ninput.append(lns[0])
            elif len(t) != 1:
                if lns[0] == "prices":
                    t = ast.literal_eval(t)
                    for c in t:
                        i = {c: np.ndarray}
                        # ninput.append(i)
                        ninput.append(c)
                else:
                    print(lns)
            else:
                pass
        npara = {}
        for l in para_l:
            r = l.split(":")
            npara[r[0]] = int(("").join([c for c in r[1] if c.isdigit()]))
        nout = [
            l.replace("integer (values are -100, 0 or 100)", "cate{-100,0,100}")
            for l in output_l
        ]
        parsed = dict(
            inputs=ninput,
            params=npara,
            outputs=nout,
            func_syntax=func_syntax,
        )
        if func_as_key:
            ta_parsed[ta] = parsed
        else:
            parsed["name"] = ta
            ta_parsed.append(parsed)
    return ta_parsed
