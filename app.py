import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="How the World Measures Vehicle Recycling",
                   page_icon="🚗", layout="wide")

# ============ Figures (verified pulls + cited national statistics) ============
EU_ELVS, EU_FLEET = 4_264_000, 256_229_781
US_FLEET, US_SALES, US_NET = 259_238_294, 15_502_479, 1_497_077
US_RETIRE = US_SALES - US_NET
JP_ELVS, JP_FLEET = 2_730_000, 61_950_000          # JARC FY2023; e-Stat/AIRIA Mar-2023
SG_DEREG, SG_FLEET = 29_089, 651_302               # LTA 2023 (cars & station-wagons)
EU_RATE, US_RATE = EU_ELVS/EU_FLEET, US_RETIRE/US_FLEET
JP_RATE, SG_RATE = JP_ELVS/JP_FLEET, SG_DEREG/SG_FLEET
AVG_AGE = {"EU-27": 12.3, "United States": 12.5, "Japan": 9.5}  # ACEA / S&P / AIRIA

DISP = pd.DataFrame({
    "Country": ["Ireland","Norway","Bulgaria","Iceland","Sweden","Denmark","France",
                "Finland","Czechia","Spain","Estonia","Latvia","Italy","Lithuania",
                "Portugal","Poland","Malta","Netherlands","Croatia","Slovakia",
                "Cyprus","Belgium","Greece","Slovenia","Austria","Germany","Hungary",
                "Luxembourg","Liechtenstein"],
    "ELVs": [90413,105444,105268,8163,134177,74369,1029932,91044,156593,601607,
             16499,14309,737852,29992,101315,375569,5350,131896,24940,33597,7820,
             63592,55097,7960,27949,250749,15156,1209,31],
    "Fleet": [2404140,2889087,3006215,256000,4976366,2827864,39358421,3718278,
              6512774,26778142,865773,781690,40915229,1700524,5847610,21796947,
              323852,9067393,1910131,2644361,625625,6047551,5877759,1230565,
              5185006,49098685,4168651,453659,30964],
    "EEA": [False,True,False,True,False,False,False,False,False,False,False,False,
            False,False,False,False,False,False,False,False,False,False,False,
            False,False,False,False,False,True],
})
DISP["Rate"] = DISP.ELVs / DISP.Fleet
DISP = DISP.sort_values("Rate", ascending=False).reset_index(drop=True)

CW = pd.DataFrame([
    ("Eurostat (env_waselvt)","End-of-life vehicles (M1+N1)","light_duty_combined",""),
    ("Eurostat (road_eqs)","Passenger cars","passenger_car_M1",""),
    ("US FHWA (MV-1)","Automobiles","NO_EQUIVALENT",
     "Excludes SUVs, minivans, pickups — M1 vehicles in the EU. No US federal "
     "class corresponds to EU M1."),
    ("US FHWA (MV-1)","Buses","bus",""),
    ("US FHWA (MV-1)","Trucks","NO_EQUIVALENT",
     "Light and heavy trucks in one undifferentiated column."),
    ("US FHWA (MV-1)","Motorcycles","motorcycle","Outside passenger scope."),
    ("US BTS (NTS 1-11)","Light duty vehicle, short wheel base","light_duty_combined",
     "Meaningful only summed with long-wheel-base line."),
    ("US BTS (NTS 1-11)","Light duty vehicle, long wheel base","light_duty_combined",
     "Meaningful only summed with short-wheel-base line."),
    ("US BTS (NTS 1-11)","Truck, single-unit 2-axle 6-tire+","heavy_goods",
     "Outside passenger scope."),
    ("US BTS (NTS 1-11)","Truck, combination","heavy_goods","Outside passenger scope."),
    ("US BTS (NTS 1-11)","Bus","bus",""),
    ("US BTS (NTS 1-11)","Highway, total (registered)","all_vehicles",""),
], columns=["Source system","Native class label","Harmonized class","Note"])

BLUE, TEAL, AMBER, RED, GREY = "#1a5276","#117864","#b9770e","#922b21","#8a8a8a"

st.title("🚗 How the World Measures Vehicle Recycling")
st.markdown(
    "**Four major markets report end-of-life vehicles four different ways — where "
    "one reports them at all.** This page maps each region's measurement regime, "
    "computes the scrappage rate each regime's data supports with the arithmetic "
    "written out, tests every rate against fleet-age behavior, documents where the "
    "classifications align and where they cannot, and identifies what a US "
    "measurement would require."
)
st.markdown("**Confidence legend:** ✅ measured (audited / system-reported) · "
            "🔧 derived from measured · 📚 literature-cited · "
            "⚠️ estimated (constructed from measured series) · ❌ not published")
st.divider()

# ============ 1 · Regimes ============
st.header("① The barometers — what each region measures, and under what mandate")
st.table(pd.DataFrame({
    "Region": ["EU-27 (+EEA)","Japan","Singapore","United States"],
    "Mandate": ["Directive 2000/53/EC — mandatory annual reporting",
                "Automobile Recycling Law (2005) — owner-funded, manifest-tracked",
                "COE system (LTA) — deregistration with proof of disposal",
                "None"],
    "What is reported": [
        "ELV counts + reuse/recycling/recovery rates, by weight, per country",
        "ELVs collected for dismantling under the manifest system "
        "(2.73M in FY2023 — JARC)",
        "Permanent deregistrations (29,089 cars in 2023 — LTA); "
        "export-vs-scrap split not published",
        "No ELV count. The circulating '95% recycled' figure restates a 2011 "
        "claim that ~95% of scrapped vehicles enter recycling infrastructure — "
        "an access rate, never audited"],
    "ELV count status": ["✅ measured","✅ measured (system reports)",
                         "🔧 derived (deregistrations)","❌ not published"],
}))
st.caption(
    "**Claim:** outcomes are measured in one region, system-reported in a second, "
    "derivable in a third, and absent in the fourth — the largest vehicle market "
    "of the four. Vehicles exported used carry their end-of-life with them; a "
    "market's regime determines whether its recycling gap can be seen at all."
)
st.divider()

# ============ 2 · Rates, with the math ============
st.header("② The rates each regime supports — with the arithmetic written out")
c = st.columns(4)
c[0].metric("EU-27 ✅", f"{EU_RATE:.2%}")
c[1].metric("Japan ✅*", f"{JP_RATE:.2%}")
c[2].metric("Singapore 🔧", f"{SG_RATE:.2%}")
c[3].metric("United States ⚠️", f"{US_RATE:.2%}")

st.markdown(f"""
| Region | Numerator (vehicles leaving the fleet) | Denominator (registered fleet) | Rate |
|---|---|---|---|
| **EU-27** ✅ | audited ELVs = **{EU_ELVS:,}** (Eurostat) | passenger cars = **{EU_FLEET:,}** (Eurostat) | {EU_ELVS:,} ÷ {EU_FLEET:,} = **{EU_RATE:.2%}** |
| **Japan** ✅* | ELVs collected for dismantling = **{JP_ELVS:,}** (JARC, FY2023) | passenger cars in use = **{JP_FLEET:,}** (e-Stat/AIRIA) | {JP_ELVS:,} ÷ {JP_FLEET:,} = **{JP_RATE:.2%}** |
| **Singapore** 🔧 | car deregistrations = **{SG_DEREG:,}** (LTA) | cars & station-wagons = **{SG_FLEET:,}** (LTA) | {SG_DEREG:,} ÷ {SG_FLEET:,} = **{SG_RATE:.2%}** |
| **US** ⚠️ | implied exits = sales **{US_SALES:,}** − net fleet change **{US_NET:,}** = **{US_RETIRE:,}** (FRED − BTS) | light-duty vehicles = **{US_FLEET:,}** (BTS 1-11) | {US_RETIRE:,} ÷ {US_FLEET:,} = **{US_RATE:.2%}** |
""")

fig1 = go.Figure()
fig1.add_bar(x=["EU-27"], y=[EU_RATE*100], marker_color=BLUE, width=0.5,
             name="Measured (audited)")
fig1.add_bar(x=["Japan"], y=[JP_RATE*100], marker_color=TEAL, width=0.5,
             name="Measured (system reports)")
fig1.add_bar(x=["Singapore"], y=[SG_RATE*100], marker_color=AMBER, width=0.5,
             name="Derived (deregistrations)")
fig1.add_bar(x=["United States"], y=[US_RATE*100], width=0.5,
             marker=dict(color="rgba(0,0,0,0)", line=dict(color=RED, width=2),
                         pattern=dict(shape="/", fgcolor=RED)),
             name="Constructed estimate")
fig1.update_layout(height=400, yaxis_title="Vehicles leaving fleet, % of fleet (2023)",
                   legend=dict(orientation="h", y=1.12), margin=dict(t=30,b=10))
st.plotly_chart(fig1, use_container_width=True)
st.caption(
    "**Claim:** these four bars are four different kinds of number, and each is "
    "drawn to say so. Scope caveats, direction known and disclosed: EU numerator "
    "includes vans over a cars-only denominator (overstated); *Japan's numerator "
    "covers all vehicle classes under the law over a passenger-car denominator "
    "(overstated); Singapore's deregistrations and the US estimate both include "
    "exported vehicles, which the EU and Japan counts exclude. Higher is not "
    "better or worse — the quantities are constructed differently."
)

st.subheader("The check: implied vehicle lifetime vs. how long fleets actually live")
lifetimes = pd.DataFrame({
    "Region": ["EU-27","Japan","Singapore","United States"],
    "Rate": [f"{EU_RATE:.2%}", f"{JP_RATE:.2%}", f"{SG_RATE:.2%}", f"{US_RATE:.2%}"],
    "Implied lifetime = 1 ÷ rate 🔧": [f"{1/EU_RATE:.0f} years", f"{1/JP_RATE:.0f} years",
                                       f"{1/SG_RATE:.0f} years", f"{1/US_RATE:.1f} years"],
    "Average fleet age 📚": ["≈12.3 yrs (ACEA)","≈9.5 yrs (AIRIA)",
                             "COE structure, ~10-yr certificates (LTA)",
                             "≈12.5 yrs (S&P Global Mobility)"],
})
st.table(lifetimes)
st.caption(
    "**Claim:** at steady state, a scrappage rate implies an average vehicle "
    "lifetime of 1 ÷ rate. The EU's documented rate implies a **60-year** vehicle "
    "life against an actual average fleet age of ~12 years — an impossibility "
    "that quantifies how much of the fleet's real exit flow the documented ELV "
    "count does not capture, predominantly used-vehicle export. Japan's implied "
    "23 years against a 9.5-year average age shows the same structure (1.83M "
    "used vehicles exported in 2023 leave the recycling system uncounted). The "
    "US implied 18.5 years is closest to plausible precisely because the "
    "constructed estimate counts every exit, exports included. The gap between "
    "implied and actual lifetime is the recycling gap, expressed in years."
)

st.subheader("Within the EU audit: a 7× spread")
show_eea = st.toggle("Include EEA reporters (Norway, Iceland, Liechtenstein)", True)
d = DISP if show_eea else DISP[~DISP.EEA]
fig2 = go.Figure(go.Bar(x=d.Country, y=d.Rate*100,
                        marker_color=[GREY if r else BLUE for r in d.EEA],
                        hovertemplate="%{x}: %{y:.2f}%<extra></extra>"))
fig2.add_hline(y=EU_RATE*100, line_dash="dot", line_color=RED,
               annotation_text=f"EU-27 aggregate {EU_RATE:.2%}")
fig2.update_layout(height=400, yaxis_title="Documented scrappage rate, 2023 (%)",
                   margin=dict(t=20,b=10))
st.plotly_chart(fig2, use_container_width=True)
st.caption("**Claim:** documented rates span 3.8% (Ireland) to 0.5% (Germany) "
           "inside one audit regime — Germany's implied lifetime is ~196 years, "
           "the export gap at its widest. Grey = EEA reporters.")
with st.expander("Full country table"):
    st.dataframe(d.style.format({"ELVs":"{:,.0f}","Fleet":"{:,.0f}","Rate":"{:.2%}"}),
                 use_container_width=True)
st.divider()

# ============ 3 · Concordance ============
st.header("③ Where the classifications align — and where they cannot")
st.markdown(
    "Cross-region comparison requires reconciling classification systems never "
    "designed to align. The concordance preserves each source's native label and "
    "assigns a harmonized class where one defensibly exists — **NO_EQUIVALENT** "
    "recorded where none does. Decisive entries: no US federal class corresponds "
    "to EU M1, and US 'Trucks' merges light and heavy vehicles the EU separates "
    "at 3.5t."
)
st.dataframe(CW, use_container_width=True)
st.caption("**Claim:** comparison is only possible at the combined light-duty "
           "level because that is the only scope both systems can approximately "
           "express. The same structure extends to Japan's registration classes "
           "(incl. kei vehicles) and Singapore's COE categories — not yet rowed.")
st.divider()

# ============ 4 · The gap and the path ============
st.header("④ The US gap — and what a proof-of-concept measurement requires")
st.markdown(
    "For the US to sit on this map as a *measured* market, in order of impact:\n\n"
    "1. **An ELV count** — none is published; the estimate here cannot separate "
    "scrappage from used-vehicle export.\n"
    "2. **A used-export series** — Census USA Trade Online carries 10-digit HTS "
    "detail that UN Comtrade flattens; separating exports from the 14.0M exits "
    "is the single largest refinement available, and would let the implied-"
    "lifetime check above close.\n"
    "3. **A vehicle-class concordance to M1/N1** — absent today (§3).\n"
    "4. **Japan/Singapore concordance rows** — their rates are computed above; "
    "aligning their vehicle classes to the shared concordance completes the "
    "four-market panel.\n\n"
    "The EU series supports history to 2008; the US fleet series breaks at the "
    "2007 federal reclassification. A multi-year, four-market panel is feasible "
    "within those bounds."
)
st.divider()

# ============ Read / trust ============
st.header("How to read this")
m1, m2 = st.columns(2)
with m1:
    st.markdown(
        "**✅ Measured** — EU ELVs & rates (Eurostat env_waselvt); EU & member "
        "fleets (road_eqs_carpda); US fleet (BTS 1-11); US registrations "
        "cross-check (FHWA MV-1); US sales (FRED LTOTALNSA); Japan ELVs (JARC "
        "manifest system, FY2023); Japan fleet (e-Stat/AIRIA); Singapore "
        "deregistrations & fleet (LTA)\n\n"
        "**🔧 Derived** — all four rates; implied lifetimes (1 ÷ rate, "
        "steady-state assumption)\n\n"
        "**📚 Literature-cited** — average fleet ages (ACEA, S&P Global "
        "Mobility, AIRIA); Japan used-vehicle exports 2023 (JAMA, 1.83M)")
with m2:
    st.markdown(
        "**⚠️ Estimated** — US fleet exits 2023: 15,502,479 − 1,497,077 = "
        "**14,005,402**. Includes used exports. Not a measurement.\n\n"
        "**❌ Not published** — any audited US ELV count; Singapore's "
        "export-vs-scrap split; Japan/Singapore classes in the concordance")

st.header("Why trust this — and where it stops")
st.table(pd.DataFrame({
    "Layer": ["Sources","EU rate","Japan rate","Singapore rate",
              "US rate (estimate)","Implied lifetimes","Concordance"],
    "Trust basis": [
        "Counts from the project's approved register plus national statistical "
        "systems (Eurostat, BTS/FHWA, JARC, e-Stat/AIRIA, LTA); figures "
        "re-verified against source publications",
        "Reproduces Eurostat's published 2023 totals exactly",
        "System-reported numerator (manifest-tracked) over national fleet series",
        "Numerator and denominator from the same authority (LTA)",
        "Every input a published series; arithmetic in full above",
        "Pure arithmetic on the rates; steady-state assumption stated",
        "12 labels, native classifications preserved, NO_EQUIVALENT permitted"],
    "Where it breaks": [
        "US estimate requires a sales series outside the register; FRED "
        "supplies it — disclosed",
        "M1+N1 numerator over cars-only denominator → slightly overstated; "
        "EU aggregate partly estimated for non-reporters",
        "Numerator covers all vehicle classes under the law; denominator is "
        "passenger cars → overstated, direction known",
        "Deregistrations include exports; export-vs-scrap split unpublished",
        "Cannot separate scrappage from export; single year; not a like "
        "measurement to the measured bars — and drawn so",
        "Steady state assumed; fleets are growing slowly, so lifetimes are "
        "modestly understated — the EU/Japan impossibilities survive the caveat",
        "Japan/Singapore classes not yet rowed"],
}))
st.caption(
    "Sources: Eurostat env_waselvt & road_eqs_carpda (2023) · BTS NTS 1-11 · "
    "FHWA MV-1 · FRED LTOTALNSA · JARC (FY2023 ELVs) · e-Stat/AIRIA (fleet, "
    "avg age) · JAMA (2023 exports) · Singapore LTA Annual Vehicle Statistics · "
    "ACEA · S&P Global Mobility. Figures verified in the project analysis "
    "notebook; warehouse-backed pipeline is the next build phase. "
    "*The Global ELV Recycling Gap* — NYU Stern MSBAi capstone.")
