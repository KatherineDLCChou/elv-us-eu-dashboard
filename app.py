import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="US–EU ELV Comparison", page_icon="🚗", layout="wide")

# ---------------- Verified numbers (Colab session, Jul 30 2026) ----------------
EU_ELVS, EU_FLEET = 4_264_000, 256_229_781
EU_RATE = EU_ELVS / EU_FLEET
US_FLEET, US_SALES = 259_238_294, 15_502_479
US_NET_CHANGE = 1_497_077
US_RETIREMENTS = US_SALES - US_NET_CHANGE
US_RATE = US_RETIREMENTS / US_FLEET

DISPERSION = pd.DataFrame({
    "Country": ["Ireland", "Norway*", "Bulgaria", "Iceland*", "Sweden", "Denmark",
                "France", "Finland", "Czechia", "Spain", "Estonia", "Latvia",
                "Italy", "Lithuania", "Portugal", "Poland", "EU-27 aggregate",
                "Malta", "Netherlands", "Croatia", "Slovakia", "Cyprus", "Belgium",
                "Greece", "Slovenia", "Austria", "Germany", "Hungary",
                "Luxembourg", "Liechtenstein*"],
    "ELVs (2023)": [90413, 105444, 105268, 8163, 134177, 74369, 1029932, 91044,
                    156593, 601607, 16499, 14309, 737852, 29992, 101315, 375569,
                    4264000, 5350, 131896, 24940, 33597, 7820, 63592, 55097,
                    7960, 27949, 250749, 15156, 1209, 31],
    "Passenger-car fleet": [2404140, 2889087, 3006215, 256000, 4976366, 2827864,
                            39358421, 3718278, 6512774, 26778142, 865773, 781690,
                            40915229, 1700524, 5847610, 21796947, 256229781,
                            323852, 9067393, 1910131, 2644361, 625625, 6047551,
                            5877759, 1230565, 5185006, 49098685, 4168651,
                            453659, 30964],
})
DISPERSION["Documented scrappage rate"] = (
    DISPERSION["ELVs (2023)"] / DISPERSION["Passenger-car fleet"])

CROSSWALK = pd.DataFrame([
    ("eurostat_env_waselvt", "End-of-life vehicles (M1+N1, Directive 2000/53/EC scope)",
     "light_duty_combined", "model_proposed_accepted", ""),
    ("eurostat_road_eqs", "Passenger cars", "passenger_car_M1", "human", ""),
    ("fhwa_mv1", "Automobiles", "NO_EQUIVALENT", "model_proposed_corrected",
     "Proper subset of EU M1 — excludes SUVs, minivans, pickups (M1 in EU terms). "
     "No US federal class corresponds to M1. Within-US use only."),
    ("fhwa_mv1", "Buses", "bus", "human", ""),
    ("fhwa_mv1", "Trucks", "NO_EQUIVALENT", "model_proposed_accepted",
     "Mixes light and heavy trucks in one undifferentiated column."),
    ("fhwa_mv1", "Motorcycles", "motorcycle", "human",
     "Out of analysis scope (passenger focus); retained for coverage."),
    ("bts_table_1_11", "Light duty vehicle, short wheel base", "light_duty_combined",
     "model_proposed_accepted", "Only meaningful summed with long-WB counterpart."),
    ("bts_table_1_11", "Light duty vehicle, long wheel base", "light_duty_combined",
     "model_proposed_accepted", "Only meaningful summed with short-WB counterpart."),
    ("bts_table_1_11", "Truck, single-unit 2-axle 6-tire or more", "heavy_goods",
     "human", "Out of analysis scope; retained for coverage."),
    ("bts_table_1_11", "Truck, combination", "heavy_goods", "human",
     "Out of analysis scope; retained for coverage."),
    ("bts_table_1_11", "Bus", "bus", "human",
     "Out of analysis scope; retained for coverage."),
    ("bts_table_1_11", "Highway, total (registered vehicles)", "all_vehicles",
     "human", ""),
], columns=["source_system", "native_label", "harmonized_class",
            "mapping_origin", "note"])

# ---------------- Page ----------------
st.title("🚗 The Global ELV Recycling Gap — US data, made comparable")
st.markdown(
    "The EU publishes the world's only **audited** end-of-life vehicle statistics. "
    "The US publishes **none** — its famous '95% recycled' figure is an industry "
    "restatement of a 2011 infrastructure claim. This page constructs the closest "
    "defensible US comparison and shows exactly where comparability ends."
)
st.markdown(
    "**Confidence legend:** ✅ measured · 🔧 derived from measured · "
    "⚠️ estimated (author's construction) · ❌ no audited figure exists"
)

# ---------------- 1 · The comparison ----------------
st.header("1 · Documented vs. constructed: light-vehicle scrappage, 2023")
c1, c2, c3 = st.columns(3)
c1.metric("EU-27 rate ✅", f"{EU_RATE:.2%}", help="4.26M audited ELVs ÷ 256M cars (Eurostat)")
c2.metric("US implied rate ⚠️", f"{US_RATE:.2%}",
          help="Author's stock-flow estimate: sales − net fleet change, ÷ fleet")
c3.metric("Audited US figure", "❌ none exists")

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(0, EU_RATE * 100, width=0.55, color="#1a5276", zorder=3)
ax.bar(1, US_RATE * 100, width=0.55, facecolor="none", edgecolor="#922b21",
       hatch="///", linewidth=1.5, linestyle="--", zorder=3)
ax.set_xticks([0, 1])
ax.set_xticklabels(["EU-27 2023\n(audited)", "US 2023\n(constructed estimate)"])
ax.set_ylabel("% of registered fleet")
ax.text(0, EU_RATE * 100 + 0.15, f"{EU_RATE:.2%}\nEurostat, audited",
        ha="center", fontsize=9)
ax.text(1, US_RATE * 100 + 0.15,
        f"{US_RATE:.2%} (implied)\nsales − fleet growth\nincludes used exports",
        ha="center", fontsize=9)
ax.set_ylim(0, 7)
ax.spines[["top", "right"]].set_visible(False)
st.pyplot(fig)

st.caption(
    "Scope: EU = cars + vans ≤3.5t (M1+N1, as legally reported — the data cannot "
    "be split to passenger cars only); US = cars + light trucks (~8,500 lb cutoff), "
    "approximating that scope but slightly wider. US value is the author's "
    "stock-flow estimate and counts all fleet exits including used-vehicle "
    "exports, which the EU figure excludes. The bars are different kinds of "
    "numbers; the gap in knowability is the finding."
)

# ---------------- 2 · Dispersion ----------------
st.header("2 · Inside the audit: the EU's 7× spread")
st.markdown(
    "Even audited numbers vary enormously. **Ireland documents 3.8%; Germany 0.5%** "
    "— consistent with Germany's documented 'whereabouts unknown' phenomenon: "
    "vehicles deregistered and exported rather than scrapped domestically. "
    "The recycling gap exists *inside* the audit regime."
)
st.dataframe(
    DISPERSION.style.format({"ELVs (2023)": "{:,.0f}",
                             "Passenger-car fleet": "{:,.0f}",
                             "Documented scrappage rate": "{:.2%}"}),
    use_container_width=True, height=400)
st.caption("*Norway, Iceland, Liechtenstein are EEA reporters, not EU members. "
           "EU-27 aggregate includes Eurostat estimates for non-reporters "
           "(e.g. Romania). Rates slightly overstated: numerator includes vans, "
           "denominator is cars only — disclosed, direction known.")

# ---------------- 3 · Crosswalk ----------------
st.header("3 · The crosswalk: why US and EU classes don't map")
st.markdown(
    "Every comparison above rests on a documented label reconciliation. Built "
    "deterministic-first with an LLM proposing only the irregular residue — every "
    "proposal human-reviewed. **The corrected row is the point:** the model mapped "
    "US 'Automobiles' to the EU passenger-car class; review rejected it, because "
    "'Automobiles' *excludes* SUVs, minivans, and pickups — vehicles the EU counts "
    "as passenger cars. **No US federal class corresponds to EU M1.**"
)
st.dataframe(CROSSWALK, use_container_width=True)
n = len(CROSSWALK)
h = (CROSSWALK.mapping_origin == "human").sum()
a = (CROSSWALK.mapping_origin == "model_proposed_accepted").sum()
c = (CROSSWALK.mapping_origin == "model_proposed_corrected").sum()
st.markdown(f"**Provenance arithmetic:** {n} labels reconciled — "
            f"{h} human · {a} model-proposed-accepted · {c} model-proposed-corrected")

st.divider()
st.caption(
    "Sources: Eurostat env_waselvt & road_eqs_carpda (2023) · FHWA MV-1 via DOT "
    "Socrata · BTS NTS Table 1-11 · FRED LTOTALNSA. Built for The Global ELV "
    "Recycling Gap capstone, NYU Stern MSBAi. US estimate is the author's; "
    "methodology in repo notebook.")
