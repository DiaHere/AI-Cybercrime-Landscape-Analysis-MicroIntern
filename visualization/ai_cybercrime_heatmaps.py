
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === CONFIG ===
CSV_PATH = "AI_Cybercrime_Observations.csv"  # update path if needed

# === 1) Read CSV ===
df = pd.read_csv(CSV_PATH)

def _clean(s):
    if isinstance(s, str):
        return s.strip()
    return s

for col in ["tool_name", "source_platform"]:
    if col in df.columns:
        df[col] = df[col].map(_clean)

# crime-type columns
crime_cols = [c for c in df.columns if c.startswith("crime_type_")]

if "crime_type" in df.columns:
    df["crime_type_norm"] = df["crime_type"].str.strip().str.lower().str.replace(" ", "_")
    for ct in df["crime_type_norm"].dropna().unique():
        colname = f"crime_type_{ct}"
        if colname not in df.columns:
            df[colname] = (df["crime_type_norm"] == ct).astype(int)
            crime_cols.append(colname)

crime_cols = sorted(set(crime_cols))

# === Helpers to build matrices ===
def build_tool_crime_matrix(frame, tool_col="tool_name", crime_columns=None):
    crime_columns = crime_columns or []
    records = []
    for _, row in frame.iterrows():
        tool = row.get(tool_col, "Unknown")
        for cc in crime_columns:
            if row.get(cc, 0) == 1:
                crime_name = cc.replace("crime_type_", "")
                records.append((tool, crime_name))
    if not records:
        return pd.DataFrame()
    rc = pd.DataFrame(records, columns=["tool", "crime"])
    matrix = rc.pivot_table(index="tool", columns="crime", values="crime", aggfunc="count", fill_value=0)
    return matrix.sort_index(axis=0).sort_index(axis=1)

def build_platform_crime_matrix(frame, platform_col="source_platform", crime_columns=None):
    crime_columns = crime_columns or []
    records = []
    for _, row in frame.iterrows():
        platform = row.get(platform_col, "Unknown")
        for cc in crime_columns:
            if row.get(cc, 0) == 1:
                crime_name = cc.replace("crime_type_", "")
                records.append((platform, crime_name))
    if not records:
        return pd.DataFrame()
    rc = pd.DataFrame(records, columns=["platform", "crime"])
    matrix = rc.pivot_table(index="platform", columns="crime", values="crime", aggfunc="count", fill_value=0)
    return matrix.sort_index(axis=0).sort_index(axis=1)

def build_platform_tool_matrix(frame, platform_col="source_platform", tool_col="tool_name"):
    frm = frame[[platform_col, tool_col]].dropna()
    if frm.empty:
        return pd.DataFrame()
    matrix = pd.crosstab(frm[platform_col], frm[tool_col])
    return matrix.sort_index(axis=0).sort_index(axis=1)

tool_crime = build_tool_crime_matrix(df, "tool_name", crime_cols)
plat_crime = build_platform_crime_matrix(df, "source_platform", crime_cols)
plat_tool  = build_platform_tool_matrix(df, "source_platform", "tool_name")

# === 3) Plot heatmaps (matplotlib only) ===
def heatmap(matrix, title, xlabel, ylabel):
    if matrix.empty:
        print(f"[WARN] Empty matrix for {title}")
        return
    fig, ax = plt.subplots(figsize=(10, max(4, 0.5 * len(matrix.index))))
    im = ax.imshow(matrix.values, aspect="auto")
    ax.set_xticks(np.arange(matrix.shape[1]))
    ax.set_yticks(np.arange(matrix.shape[0]))
    ax.set_xticklabels(matrix.columns, rotation=45, ha="right")
    ax.set_yticklabels(matrix.index)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, str(matrix.values[i, j]), ha="center", va="center", fontsize=8)
    plt.tight_layout()
    plt.show()

heatmap(tool_crime, "AI Tool vs. Crime Type — Observed Links (count)", "Crime Type", "AI Tool")
heatmap(plat_crime, "Platform vs. Crime Type — Observed Mentions (count)", "Crime Type", "Source Platform")
heatmap(plat_tool, "Platform vs. AI Tool — Mentions (count)", "AI Tool", "Source Platform")

# === 4) Optional risk scatter ===
if {"barrier_delta_0_3", "efficiency_delta_0_3", "tool_name"}.issubset(df.columns):
    agg = (df.groupby("tool_name")[["barrier_delta_0_3","efficiency_delta_0_3"]]
             .mean()
             .join(df["tool_name"].value_counts().rename("count")))
    fig, ax = plt.subplots(figsize=(7,5))
    ax.scatter(agg["efficiency_delta_0_3"], agg["barrier_delta_0_3"], s=agg["count"]*60, alpha=0.7)
    for name, row in agg.iterrows():
        ax.annotate(name, (row["efficiency_delta_0_3"], row["barrier_delta_0_3"]), xytext=(3,3), textcoords="offset points", fontsize=8)
    ax.set_xlabel("Efficiency Gain (0–3)")
    ax.set_ylabel("Barrier Lowering (0–3)")
    ax.set_title("Perceived Risk — Efficiency vs. Barrier Lowering (size = mentions)")
    plt.tight_layout()
    plt.show()
