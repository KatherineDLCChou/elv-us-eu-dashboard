import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="How the World Measures Vehicle Recycling",
                   page_icon="🚗", layout="wide")

# ============ Verified figures (analysis notebook, Jul 2026) ============
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
    ("Eurostat (env_waselvt)", "End-of-life vehicles (M1+N1)", "light_duty_combined", ""),
    ("Eurostat (road_eqs)", "Passenger cars", "passenger_car_M1", ""),
    ("US FHWA (MV-1)", "Automobiles", "NO_EQUIVALENT",
     "Excludes SUVs, minivans, pickups — vehicles classified M1 in the EU. "
     "No US federal class corresponds to EU M1."),
    ("US FHWA (MV-1)", "Buses", "bus", ""),
    ("US FHWA (MV-1)", "Trucks", "NO_EQUIVALENT",
     "Light and heavy trucks reported in one undifferentiated column."),
    ("US FHWA (MV-1)", "Motorcycles", "motorcycle", "Outside passenger scope."),
    ("US BTS (NTS 1-11)", "Light duty vehicle, short wheel base",
     "light_duty_combined", "Meaningful only summed with long-wheel-base line."),
    ("US BTS (NTS 1-11)", "Light duty vehicle, long wheel base",
     "light_duty_combined", "Meaningful only summed with short-wheel-base line."),
    ("US BTS (NTS 1-11)", "Truck, single-unit 2-axle 6-tire+", "heavy_goods",
     "Outside passenger scope."),
    ("US BTS (NTS 1-11)", "Truck, combination", "heavy_goods",
     "Outside passenger scope."),
    ("US BTS (NTS 1-11)", "Bus", "bus", ""),
    ("US BTS (NTS 1-11)", "Highway, total (registered)", "all_vehicles", ""),
], columns=["Source system", "Native class label", "Harmonized class", "Note"])

BLUE, RED, GREY = "#1a5276", "#922b21", "#8a8a8a"

# ============ Header ============
st.title("🚗 How the World Measures Vehicle Recycling")
st.markdown(
    "**Four major markets report end-of-life vehicles four different ways — where "
    "one reports them at all.** This page maps each region's measurement regime, "
    "states the recycling rates the data can support, documents where the "
    "classifications do and do not align, and identifies what a US measurement "
    "would require."
)
st.markdown("**Confidence legend:** ✅ measured (audited/system-reported) · "
            "🔧 derived from measured · ⚠️ estimated (constructed from measured "
            "series) · ❌ not published")
st.divider()

# ============ 1 · Measurement regimes ============
st.header("① The barometers — what each region measures, and under what mandate")
regimes = pd.DataFrame({
    "Region": ["EU-27 (+EEA)", "Japan", "Singapore", "United States"],
    "Mandate": ["Directive 2000/53/EC — mandatory annual reporting",
                "Automobile Recycling Law (2005) — owner-funded, manifest-tracked",
                "COE system (LTA) — deregistration with proof of disposal",
                "None"],
    "What is reported": [
        "ELV counts + reuse/recycling/recovery rates, by weight, per country",
        "Vehicles processed through the recycling system; ~95% of materials "
        "captured for domestic ELVs (system reports / literature)",
        "Permanent deregistrations (49,550 cars in 2025; 36,137 in 2024; "
        "29,089 in 2023 — LTA); export-vs-scrap split not published",
        "No ELV count. The circulating '95% recycled' figure restates a 2011 "
        "claim that ~95% of scrapped vehicles enter recycling infrastructure — "
        "an access rate, never audited"],
    "ELV count status": ["✅ measured", "✅ measured (system reports)",
                         "🔧 derived (deregistrations)", "❌ not published"],
})
st.table(regimes)
st.caption(
    "**Claim:** outcomes are measured in one region, system-reported in a second, "
    "derivable in a third, and absent in the fourth — and the fourth is the largest "
    "vehicle market of the four. Vehicles exported used carry their end-of-life "
    "with them, so a market's regime determines whether its recycling gap can be "
    "seen at all. Singapore's trade data cannot isolate used-vehicle flows from "
    "new-car re-exports; Japan's exported used vehicles leave its recycling system "
    "entirely — both markets' own published reconciliations show these limits."
)
st.divider()

# ============ 2 · The rates the data supports ============
st.header("② The rates the data supports — documented vs. constructed, 2023")
k1, k2, k3, k4 = st.columns(4)
k1.metric("EU-27 documented rate ✅", f"{EU_RATE:.2%}",
          help="4,264,000 audited ELVs ÷ 256,229,781 registered cars (Eurostat)")
k2.metric("US implied rate ⚠️", f"{US_RATE:.2%}",
          help="Constructed: sales − net fleet change, ÷ fleet — see methodology")
k3.metric("Japan / Singapore rates", "not computed",
          help="Requires fleet denominators verified to the same standard; "
               "defined expansion in § 4")
k4.metric("US classes mapping to EU M1", "0 of 12", help="See concordance, § 3")

fig1 = go.Figure()
fig1.add_bar(x=["EU-27 (documented)"], y=[EU_RATE * 100], width=0.45,
             marker_color=BLUE, name="Documented (Eurostat, audited)",
             hovertemplate="EU-27: %{y:.2f}%<br>4.26M ELVs / 256M cars<extra></extra>")
fig1.add_bar(x=["US (constructed)"], y=[US_RATE * 100], width=0.45,
             marker=dict(color="rgba(0,0,0,0)", line=dict(color=RED, width=2),
                         pattern=dict(shape="/", fgcolor=RED)),
             name="Constructed estimate",
             hovertemplate="US: %{y:.2f}% implied<br>15.5M sales − 1.5M fleet growth"
                           "<br>= 14.0M exits incl. used exports<extra></extra>")
fig1.update_layout(height=400, yaxis_title="% of registered fleet, 2023",
                   legend=dict(orientation="h", y=1.1), margin=dict(t=30, b=10))
st.plotly_chart(fig1, use_container_width=True)
st.caption(
    "**Claim:** these bars are different kinds of numbers, and the difference is "
    "drawn. The EU figure is an audited count over a measured fleet. The US figure "
    "is arithmetic on measured series — sales (15,502,479) minus net fleet change "
    "(1,497,077) = 14,005,402 fleet exits — and counts **all** exits including "
    "used-vehicle exports, which the EU figure excludes. Higher is not better or "
    "worse; the quantities are constructed differently. Scope: EU = cars + vans "
    "≤3.5t (M1+N1, reported combined and not splittable); US = cars + light trucks "
    "(~8,500 lb cutoff), slightly wider than 3.5t."
)

st.subheader("Within the EU audit: a 7× spread")
show_eea = st.toggle("Include EEA reporters (Norway, Iceland, Liechtenstein — "
                     "report under the Directive, not EU members)", value=True)
d = DISP if show_eea else DISP[~DISP.EEA]
fig2 = go.Figure(go.Bar(x=d.Country, y=d.Rate * 100,
                        marker_color=[GREY if r else BLUE for r in d.EEA],
                        hovertemplate="%{x}: %{y:.2f}%<extra></extra>"))
fig2.add_hline(y=EU_RATE * 100, line_dash="dot", line_color=RED,
               annotation_text=f"EU-27 aggregate {EU_RATE:.2%}")
fig2.update_layout(height=420, yaxis_title="Documented scrappage rate, 2023 (%)",
                   margin=dict(t=20, b=10))
st.plotly_chart(fig2, use_container_width=True)
st.caption(
    "**Claim:** documented national rates span 3.8% (Ireland) to 0.5% (Germany) — "
    "a 7× spread inside a single audit regime, consistent with Germany's "
    "documented volume of deregistered vehicles whose statistical whereabouts are "
    "unknown, predominantly used-vehicle exports. The recycling gap is visible "
    "even where measurement is strongest. Grey = EEA reporters. Rates slightly "
    "overstated by construction (numerator includes vans; denominator is cars "
    "only — direction known)."
)
with st.expander("Full country table"):
    st.dataframe(d[["Country", "ELVs", "Fleet", "Rate", "EEA"]]
                 .style.format({"ELVs": "{:,.0f}", "Fleet": "{:,.0f}",
                                "Rate": "{:.2%}"}), use_container_width=True)
st.divider()

# ============ 3 · The concordance ============
st.header("③ Where the classifications align — and where they cannot")
st.markdown(
    "Cross-region comparison requires reconciling classification systems that "
    "were never designed to align. The concordance below preserves each source's "
    "native label and assigns a harmonized class where one defensibly exists — "
    "with **NO_EQUIVALENT** recorded where none does. The decisive entries: no US "
    "federal class corresponds to EU M1 (US 'Automobiles' excludes SUVs, minivans, "
    "and pickups, which the EU classifies as passenger cars), and US 'Trucks' "
    "merges light and heavy vehicles the EU separates at 3.5t."
)
st.dataframe(CW, use_container_width=True)
st.caption(
    "**Claim:** the comparison in § 2 is only possible at the combined light-duty "
    "level — cars + light trucks against cars + vans — because that is the only "
    "scope both systems can approximately express. The same concordance structure "
    "(native label preserved, harmonized class, NO_EQUIVALENT permitted) extends "
    "to Japan's registration classes (incl. kei vehicles) and Singapore's COE "
    "categories."
)
st.divider()

# ============ 4 · The gap and the expansion path ============
st.header("④ The US gap — and what a proof-of-concept measurement requires")
st.markdown(
    "For the US to sit on this map as a *measured* market rather than a "
    "constructed one, the data would need, in order of impact:\n\n"
    "1. **An ELV count** — none is published by any US agency; the estimate here "
    "is built from sales and fleet-change series and cannot separate scrappage "
    "from used-vehicle export.\n"
    "2. **A used-export series** — Census USA Trade Online carries 10-digit HTS "
    "detail that UN Comtrade flattens; separating exports from the 14.0M exits "
    "is the single largest refinement available.\n"
    "3. **A vehicle-class concordance to M1/N1** — absent today (§ 3); any US "
    "measurement inherits the ~8,500 lb vs 3.5t scope mismatch until resolved.\n"
    "4. **Extension of the same audit to Japan and Singapore rates** — both "
    "regions report counts (§ 1); computing comparable rates requires fleet "
    "denominators verified to the standard used for the EU and US figures here.\n\n"
    "The EU series supports history to 2008; the US fleet series breaks at the "
    "2007 federal reclassification. A multi-year panel on both sides is feasible "
    "within those bounds."
)
st.divider()

# ============ How to read this ============
st.header("How to read this — measured, derived, estimated, absent")
m1, m2 = st.columns(2)
with m1:
    st.markdown(
        "**✅ Measured**\n"
        "- EU ELV counts & rates — Eurostat `env_waselvt` (audited under "
        "Directive 2000/53/EC; 2021–23 EU aggregates include Eurostat estimates "
        "for non-reporters)\n"
        "- EU & member-state fleets — Eurostat `road_eqs_carpda`\n"
        "- US fleet — BTS NTS Table 1-11 (short + long wheelbase summed)\n"
        "- US registrations cross-check — FHWA MV-1 (96.9M autos ⊂ 197M short-WB)\n"
        "- US light-vehicle sales — FRED `LTOTALNSA`\n"
        "- Singapore deregistrations — LTA (published annual statistics)\n\n"
        "**🔧 Derived from measured**\n"
        "- EU and US scrappage rates (§ 2)")
with m2:
    st.markdown(
        "**⚠️ Estimated (constructed from measured series)**\n"
        "- US fleet exits 2023: 15,502,479 sales − 1,497,077 net fleet change "
        "= **14,005,402**. Includes used-vehicle exports, which the EU figure "
        "excludes. Not a measurement.\n\n"
        "**❌ Not published**\n"
        "- Any audited US ELV count\n"
        "- Singapore's export-vs-domestic-scrap split\n"
        "- Japan/Singapore fleet denominators verified here (expansion, § 4)")

# ============ Why trust this ============
st.header("Why trust this — and where it stops")
trust = pd.DataFrame({
    "Layer": ["Sources", "EU rate", "US denominator", "US numerator (estimate)",
              "Concordance", "Regime map (JP/SG)"],
    "Trust basis": [
        "Counts drawn from the project's approved source register (Eurostat, "
        "BTS/FHWA, LTA); each figure re-verified against the source API or "
        "publication",
        "Reproduces Eurostat's published 2023 totals (4.26M ELVs) exactly",
        "Two independent federal sources coherent (MV-1 autos ⊂ BTS short-WB)",
        "Every input a published series; arithmetic stated in full on this page",
        "12 labels, native classifications preserved, NO_EQUIVALENT permitted",
        "Regimes and counts as published by national systems (LTA statistics; "
        "recycling-law system reports)"],
    "Where it breaks": [
        "The US estimate requires a sales series outside the register; FRED "
        "(Federal Reserve) supplies it — disclosed",
        "M1+N1 numerator over cars-only denominator → slightly overstated; EU "
        "aggregate partly estimated for non-reporters",
        "US light trucks extend to ~8,500 lb — wider than the EU 3.5t cutoff",
        "Cannot separate scrappage from used export; single year (2023); not a "
        "like measurement to the EU bar — and drawn so",
        "Covers Eurostat and US federal systems; Japan/Singapore classes not "
        "yet rowed",
        "Japan/Singapore rates not computed pending verified fleet denominators"],
})
st.table(trust)
st.caption(
    "Sources: Eurostat env_waselvt & road_eqs_carpda (2023) · BTS NTS Table 1-11 · "
    "FHWA MV-1 (DOT Socrata) · FRED LTOTALNSA · Singapore LTA annual statistics · "
    "Directive 2000/53/EC · Japan Automobile Recycling Law (2005). Figures verified "
    "in the project analysis notebook; warehouse-backed pipeline is the next build "
    "phase. *The Global ELV Recycling Gap* — NYU Stern MSBAi capstone.")
