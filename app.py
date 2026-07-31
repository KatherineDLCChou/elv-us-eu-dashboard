import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="US–EU ELV Comparability", page_icon="🚗", layout="wide")

# ================= Verified numbers (Colab session, Jul 30 2026) =================
EU_ELVS, EU_FLEET = 4_264_000, 256_229_781
EU_RATE = EU_ELVS / EU_FLEET
US_FLEET, US_SALES, US_NET = 259_238_294, 15_502_479, 1_497_077
US_RETIRE = US_SALES - US_NET
US_RATE = US_RETIRE / US_FLEET

DISP = pd.DataFrame({
    "Country": ["Ireland", "Norway", "Bulgaria", "Iceland", "Sweden", "Denmark",
                "France", "Finland", "Czechia", "Spain", "Estonia", "Latvia",
                "Italy", "Lithuania", "Portugal", "Poland", "Malta", "Netherlands",
                "Croatia", "Slovakia", "Cyprus", "Belgium", "Greece", "Slovenia",
                "Austria", "Germany", "Hungary", "Luxembourg", "Liechtenstein"],
    "ELVs": [90413, 105444, 105268, 8163, 134177, 74369, 1029932, 91044, 156593,
             601607, 16499, 14309, 737852, 29992, 101315, 375569, 5350, 131896,
             24940, 33597, 7820, 63592, 55097, 7960, 27949, 250749, 15156, 1209, 31],
    "Fleet": [2404140, 2889087, 3006215, 256000, 4976366, 2827864, 39358421,
              3718278, 6512774, 26778142, 865773, 781690, 40915229, 1700524,
              5847610, 21796947, 323852, 9067393, 1910131, 2644361, 625625,
              6047551, 5877759, 1230565, 5185006, 49098685, 4168651, 453659, 30964],
    "EEA": [False, True, False, True, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, True],
})
DISP["Rate"] = DISP["ELVs"] / DISP["Fleet"]
DISP = DISP.sort_values("Rate", ascending=False).reset_index(drop=True)

CW = pd.DataFrame([
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
     "human", "Out of scope; retained for coverage."),
    ("bts_table_1_11", "Truck, combination", "heavy_goods", "human",
     "Out of scope; retained for coverage."),
    ("bts_table_1_11", "Bus", "bus", "human", ""),
    ("bts_table_1_11", "Highway, total (registered vehicles)", "all_vehicles",
     "human", ""),
], columns=["source_system", "native_label", "harmonized_class",
            "mapping_origin", "note"])

BLUE, RED, GREY = "#1a5276", "#922b21", "#8a8a8a"

# ================= Header =================
st.title("🚗 Can the US and EU even be compared on vehicle recycling?")
st.markdown(
    "**Mostly no — and measuring exactly *why* is the finding.** The EU publishes the "
    "world's only audited end-of-life vehicle statistics. The US publishes none: its "
    "famous **'95% recycled'** figure traces to a 2011 infrastructure claim, restated "
    "by industry until it looked like a statistic. This page constructs the closest "
    "defensible US comparison, documents every step where comparability breaks, and "
    "proposes the audit as the team's template for deciding **which markets' data can "
    "support decisions**."
)
st.markdown("**Confidence legend:** ✅ measured · 🔧 derived from measured · "
            "⚠️ estimated (author's construction) · ❌ no audited figure exists")
st.divider()

# ================= 1 · The finding =================
st.header("① The finding — one of these numbers is not like the other")
k1, k2, k3, k4 = st.columns(4)
k1.metric("EU-27 documented rate ✅", f"{EU_RATE:.2%}",
          help="4,264,000 audited ELVs ÷ 256,229,781 cars (Eurostat, 2023)")
k2.metric("US implied rate ⚠️", f"{US_RATE:.2%}",
          help="Author's stock-flow estimate — see § methodology")
k3.metric("Audited US ELV count", "❌ none",
          help="No US agency publishes a measured end-of-life vehicle count")
k4.metric("US classes mapping to EU M1", "0 of 12",
          help="See the crosswalk in section ③")

fig1 = go.Figure()
fig1.add_bar(x=["EU-27 (audited)"], y=[EU_RATE * 100], width=0.45,
             marker_color=BLUE, name="Audited (Eurostat)",
             hovertemplate="EU-27: %{y:.2f}%<br>4.26M ELVs / 256M cars<extra></extra>")
fig1.add_bar(x=["US (constructed)"], y=[US_RATE * 100], width=0.45,
             marker=dict(color="rgba(0,0,0,0)",
                         line=dict(color=RED, width=2),
                         pattern=dict(shape="/", fgcolor=RED)),
             name="Constructed estimate (author)",
             hovertemplate="US: %{y:.2f}% implied<br>sales − fleet growth = 14.0M exits"
                           "<br>includes used exports<extra></extra>")
fig1.update_layout(height=420, yaxis_title="% of registered fleet, 2023",
                   legend=dict(orientation="h", y=1.08), margin=dict(t=30, b=10))
st.plotly_chart(fig1, use_container_width=True)
st.caption(
    "**Claim:** the gap between these bars is a gap in *knowability*, not performance. "
    "The EU bar is an audited count over a measured fleet. The US bar is the author's "
    "arithmetic (sales − net fleet growth) and counts **every** exit including used-car "
    "exports, which the EU number excludes — so even the 5.40% is a different kind of "
    "quantity, drawn hatched for that reason. Higher is not better or worse: it is "
    "*differently constructed*. Scope: EU = cars + vans ≤3.5t (M1+N1, legally "
    "unsplittable); US = cars + light trucks (~8,500 lb), slightly wider."
)
st.divider()

# ================= 2 · Inside the audit =================
st.header("② Inside the audit — the EU's own 7× spread")
st.markdown(
    "Audited ≠ uniform. **Ireland documents 3.8%, Germany 0.5%** — a 7× spread "
    "*inside* the world's only audit regime, consistent with Germany's documented "
    "'whereabouts unknown' phenomenon: deregistered vehicles exported rather than "
    "scrapped at home. The recycling gap this capstone is named for is visible even "
    "where measurement is strongest."
)
show_eea = st.toggle("Include EEA reporters (Norway, Iceland, Liechtenstein — not EU members)",
                     value=True)
d = DISP if show_eea else DISP[~DISP.EEA]
colors = [GREY if r else BLUE for r in d.EEA]
fig2 = go.Figure(go.Bar(
    x=d.Country, y=d.Rate * 100, marker_color=colors,
    hovertemplate="%{x}: %{y:.2f}%<extra></extra>"))
fig2.add_hline(y=EU_RATE * 100, line_dash="dot", line_color=RED,
               annotation_text=f"EU-27 aggregate {EU_RATE:.2%}")
for country, label in [("Ireland", "documents the most"),
                       ("Germany", "0.5% — the export gap")]:
    if country in d.Country.values:
        row = d[d.Country == country].iloc[0]
        fig2.add_annotation(x=country, y=row.Rate * 100 + 0.25, text=label,
                            showarrow=False, font=dict(size=11))
fig2.update_layout(height=430, yaxis_title="Documented scrappage rate, 2023 (%)",
                   margin=dict(t=20, b=10))
st.plotly_chart(fig2, use_container_width=True)
st.caption(
    "**Claim:** even audited national rates disagree 7×, driven by used-vehicle "
    "exports and reporting practice — so 'the EU rate' is an average over very "
    "different measurement realities. Grey bars = EEA reporters, not EU members. "
    "Rates slightly overstated by construction (numerator includes vans; denominator "
    "is cars only — direction known, disclosed)."
)
with st.expander("Full country table"):
    st.dataframe(d[["Country", "ELVs", "Fleet", "Rate", "EEA"]]
                 .style.format({"ELVs": "{:,.0f}", "Fleet": "{:,.0f}",
                                "Rate": "{:.2%}"}),
                 use_container_width=True)
st.divider()

# ================= 3 · The instrument =================
st.header("③ The instrument — a crosswalk that refuses false equivalence")
st.markdown(
    "Every comparison above rests on a documented label reconciliation between "
    "Eurostat and US federal classifications — deterministic lookups first, an LLM "
    "proposing only the irregular residue, **every proposal human-reviewed**. "
    "The decisive row: the model mapped US **'Automobiles'** to the EU passenger-car "
    "class, and review **rejected it** — 'Automobiles' *excludes* SUVs, minivans, and "
    "pickups, which the EU counts as passenger cars. The correction encodes the "
    "central fact: **no US federal vehicle class corresponds to EU M1.** A crosswalk "
    "that maps everything is indistinguishable from one nobody checked; this one "
    "records what cannot map."
)
p1, p2, p3, p4 = st.columns(4)
p1.metric("Labels reconciled", len(CW))
p2.metric("Human-assigned", int((CW.mapping_origin == "human").sum()))
p3.metric("Model-proposed, accepted",
          int((CW.mapping_origin == "model_proposed_accepted").sum()))
p4.metric("Model-proposed, corrected",
          int((CW.mapping_origin == "model_proposed_corrected").sum()),
          help="The evidence review actually happened")
origin = st.multiselect("Filter by mapping origin",
                        CW.mapping_origin.unique().tolist(),
                        default=CW.mapping_origin.unique().tolist())
st.dataframe(CW[CW.mapping_origin.isin(origin)], use_container_width=True)
st.caption("**Claim:** the crosswalk is the adoptable artifact — the same structure "
           "(native label preserved, harmonized class, mapping origin, note, "
           "NO_EQUIVALENT allowed) extends to Japan's kei classes and Singapore's "
           "COE categories.")
st.divider()

# ================= 4 · What it means =================
st.header("④ What this means — a measurement-regime map for the capstone")
st.markdown(
    "Each team market has now been audited by a different member. Read together, "
    "they give the capstone its market-selection criterion: **build decisions on "
    "markets in the order of their measurement regime.**")
regime = pd.DataFrame({
    "Market": ["EU-27", "Japan", "Singapore", "United States"],
    "Regime": ["Audited mass-based reporting (Directive 2000/53/EC)",
               "Law-mandated recycling system (2005 Automobile Recycling Law)",
               "Deregistration-based (COE); disposal split unpublished",
               "None — industry assertion only"],
    "ELV count": ["✅ measured", "✅ measured (system reports)",
                  "🔧 derived (deregistrations)", "⚠️ must be constructed"],
    "Audited by": ["This dashboard", "Teammate build (liability transfer)",
                   "Teammate build (pilot)", "This dashboard"],
})
st.table(regime)
st.caption("**Claim:** the US is the largest vehicle market on this map and the only "
           "one where the ELV count must be constructed by the analyst. Quantifying "
           "that opacity — market by market, with one shared crosswalk — is the "
           "capstone's contribution. (Japan/Singapore rows summarize teammates' "
           "findings; their dashboards are the source.)")
st.divider()

# ================= How to read this =================
st.header("How to read this — measured, derived, estimated, absent")
m1, m2 = st.columns(2)
with m1:
    st.markdown(
        "**✅ Measured (facts)**\n"
        "- EU ELV counts & rates — Eurostat `env_waselvt` (audited under "
        "Directive 2000/53/EC; 2021–23 EU aggregates include Eurostat estimates "
        "for non-reporters, e.g. Romania)\n"
        "- EU & member-state fleets — Eurostat `road_eqs_carpda`\n"
        "- US fleet — BTS NTS Table 1-11 (short-WB + long-WB summed)\n"
        "- US registrations cross-check — FHWA MV-1 (96.9M autos ⊂ 197M short-WB ✓)\n"
        "- US light-vehicle sales — FRED `LTOTALNSA`\n\n"
        "**🔧 Derived from measured**\n"
        "- Both scrappage rates (numerator ÷ denominator, sources above)")
with m2:
    st.markdown(
        "**⚠️ Estimated — author's construction**\n"
        "- US retirements 2023 = sales 15,502,479 − net fleet change 1,497,077 "
        "= **14,005,402**. Counts *all* fleet exits **including used-vehicle "
        "exports**, which the EU figure excludes. Not a measurement.\n\n"
        "**❌ Absent**\n"
        "- Any audited US ELV count. The '95% recycled' figure is a restated "
        "2011 claim that ~95% of scrapped vehicles *enter recycling "
        "infrastructure* — an access rate, not an outcome rate, never audited.")

# ================= Why trust this =================
st.header("Why trust this — and where it stops")
trust = pd.DataFrame({
    "Layer": ["Sources", "EU rate", "US denominator", "US numerator (estimate)",
              "Crosswalk", "Scope construction"],
    "Trust basis": [
        "All counts from the team's approved register (Eurostat, BTS/FHWA); "
        "every figure re-verified against source APIs in the analysis notebook",
        "Reproduces Eurostat's published totals (4.26M ELVs, 2023) exactly",
        "Two independent federal sources coherent (MV-1 autos ⊂ BTS short-WB)",
        "Every input traceable; arithmetic shown on this page",
        "12 labels, full provenance per row; raw model responses retained; "
        "1 corrected row proves review",
        "Threshold (3.5t) anchored to the EU numerator's legal definition; "
        "direction of every mismatch stated"],
    "Where it breaks": [
        "US estimate requires a sales series; the register has none, so FRED "
        "(Federal Reserve) is used — disclosed here",
        "M1+N1 numerator over cars-only denominator → slightly overstated; "
        "EU aggregate partly estimated for non-reporters",
        "US light trucks run to ~8,500 lb — wider than the EU's 3.5t cutoff",
        "Includes used exports the EU excludes; single year; not comparable "
        "to the EU bar as a like measurement — and drawn so",
        "Built for these 3 source systems; Japan/Singapore classes not yet rowed",
        "One year (2023). EU history feasible 2008→; US wheelbase series "
        "breaks at 2007 reclassification"],
})
st.table(trust)
st.caption(
    "Sources: Eurostat env_waselvt & road_eqs_carpda (2023) · BTS NTS Table 1-11 · "
    "FHWA MV-1 (DOT Socrata hwtm-7xmz) · FRED LTOTALNSA · Crosswalk residue: "
    "claude-sonnet-4-5, temperature 0, all proposals human-reviewed. Numbers "
    "verified in the analysis notebook; warehouse-backed pipeline is the next build "
    "phase. Built for *The Global ELV Recycling Gap* capstone, NYU Stern MSBAi.")
