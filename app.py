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
REGIONS = ["EU-27","Japan","Singapore","United States"]
RATES = [EU_RATE, JP_RATE, SG_RATE, US_RATE]
AGES = [12.3, 9.5, 10.0, 12.5]   # ACEA · AIRIA · COE certificate term · S&P
AGE_SRC = ["ACEA","AIRIA","COE certificate term (LTA)","S&P Global Mobility"]

st.title("🚗 How the World Measures Vehicle Recycling")
st.markdown(
    "**Four major markets report end-of-life vehicles four different ways — where "
    "one reports them at all.** This page maps each region's measurement regime, "
    "states the scrappage rate each regime's data supports, shows how consumer "
    "replacement behavior drives the numbers, follows the missing flow into the "
    "trade records, documents where the classifications align and where they "
    "cannot, and identifies what a US measurement would require."
)
st.markdown("**Confidence legend:** ✅ measured (audited / system-reported) · "
            "🔧 derived from measured · 📚 literature-cited · "
            "⚠️ estimated (constructed from measured series) · ❌ not published")
st.divider()

# ============ 1 · Regimes ============
st.header("① The barometers — what each region measures, and under what mandate")
st.table(pd.DataFrame({
    "Region": REGIONS,
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

# ============ 2 · Rates ============
st.header("② The rates each regime supports — 2023")
c = st.columns(4)
c[0].metric("EU-27 ✅", f"{EU_RATE:.2%}",
            help="4,264,000 audited ELVs ÷ 256,229,781 cars (Eurostat)")
c[1].metric("Japan ✅*", f"{JP_RATE:.2%}",
            help="2,730,000 ELVs (JARC manifest, FY2023) ÷ 61,950,000 cars "
                 "(e-Stat/AIRIA)")
c[2].metric("Singapore 🔧", f"{SG_RATE:.2%}",
            help="29,089 car deregistrations ÷ 651,302 cars — both LTA")
c[3].metric("United States ⚠️", f"{US_RATE:.2%}",
            help="Constructed — arithmetic below the chart")

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
    "**Claim:** these four bars are four different kinds of number, each drawn to "
    "say so. The US bar is the only constructed one: "
    "**implied exits = 15,502,479 sales − 1,497,077 net fleet growth = "
    "14,005,402**, over a 259.2M light-duty fleet — and it counts every exit "
    "including used-vehicle exports, which the EU and Japan counts exclude. "
    "Scope caveats, direction known: EU numerator includes vans over a cars-only "
    "denominator; Japan's numerator covers all vehicle classes under the law "
    "over a passenger-car denominator — both slightly overstated. Higher is not "
    "better or worse; the quantities are constructed differently."
)
with st.expander("Full numerator / denominator sourcing"):
    st.markdown(f"""
- **EU-27** ✅ — audited ELVs {EU_ELVS:,} (Eurostat env_waselvt) ÷ passenger cars {EU_FLEET:,} (Eurostat road_eqs_carpda)
- **Japan** ✅* — ELVs collected for dismantling {JP_ELVS:,} (JARC manifest system, FY2023) ÷ passenger cars in use {JP_FLEET:,} (e-Stat/AIRIA, Mar 2023)
- **Singapore** 🔧 — permanent car deregistrations {SG_DEREG:,} ÷ cars & station-wagons {SG_FLEET:,} (both LTA Annual Vehicle Statistics)
- **US** ⚠️ — implied exits {US_RETIRE:,} (= FRED LTOTALNSA sales {US_SALES:,} − BTS 1-11 net fleet change {US_NET:,}) ÷ light-duty fleet {US_FLEET:,} (BTS 1-11, short + long wheelbase)
""")

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
           "inside one audit regime. Grey = EEA reporters.")
with st.expander("Full country table"):
    st.dataframe(d.style.format({"ELVs":"{:,.0f}","Fleet":"{:,.0f}","Rate":"{:.2%}"}),
                 use_container_width=True)
st.divider()

# ============ 3 · The consumer layer ============
st.header("③ The consumer layer — replacement behavior drives every number above")
st.markdown(
    "A scrappage rate is the meeting point of two different events: a household's "
    "**decision to replace** a vehicle, and the vehicle's **documented "
    "end-of-life**. Comparing how long consumers actually keep vehicles against "
    "the lifetime each region's scrappage rate implies (at steady state, "
    "**implied lifetime = 1 ÷ rate**) shows how far apart those two events are "
    "in each market."
)
fig3 = go.Figure()
fig3.add_bar(x=REGIONS, y=AGES, name="Average fleet age / holding proxy 📚",
             marker_color="#5d6d7e", width=0.35, offsetgroup=0,
             hovertemplate="%{x}: %{y} yrs<extra></extra>")
fig3.add_bar(x=REGIONS, y=[1/r for r in RATES],
             name="Implied vehicle lifetime = 1 ÷ scrappage rate 🔧",
             marker_color=RED, width=0.35, offsetgroup=1,
             hovertemplate="%{x}: %{y:.0f} yrs implied<extra></extra>")
fig3.update_layout(height=420, yaxis_title="Years", barmode="group",
                   legend=dict(orientation="h", y=1.12), margin=dict(t=30,b=10))
st.plotly_chart(fig3, use_container_width=True)
st.table(pd.DataFrame({
    "Region": REGIONS,
    "Avg fleet age 📚": [f"{a} yrs ({s})" for a, s in zip(AGES, AGE_SRC)],
    "Implied lifetime 🔧": [f"{1/r:.0f} yrs" for r in RATES],
    "Gap": [f"{1/r - a:+.0f} yrs" for r, a in zip(RATES, AGES)],
}))
st.caption(
    "**Claim:** replacement is a spending decision; documented scrappage is a "
    "measurement event — and in every measured market they are decades apart. "
    "EU consumers replace around year 12, yet the documented rate implies cars "
    "live **60 years**: the difference is vehicles leaving the audit as used "
    "exports, not deaths. Japan is sharper — inspection (shaken) costs push "
    "replacement toward year 9–10, and 1.83M used vehicles exported in 2023 "
    "(JAMA 📚) exit the recycling system young. Singapore's COE makes "
    "replacement timing a policy price rather than a consumer choice. The US "
    "is the near-reconciled case — implied 18.5 years against a 12.5-year "
    "average age — precisely because its constructed count includes exports. "
    "**The wedge between replacement and documented end-of-life is the "
    "recycling gap's supply side: consumer upgrade cycles feed the export "
    "flow that measurement loses.** Steady-state assumption stated; slowly "
    "growing fleets understate implied lifetimes modestly — the EU and Japan "
    "impossibilities survive the caveat."
)
st.divider()

# ============ 4 · The export mirror ============
st.header("④ The export mirror — where the wedge goes, and where records disagree")
st.markdown(
    "§3 shows vehicles leaving fleets years before documented end-of-life. Trade "
    "records are where that flow should reappear — and the defining feature of "
    "used-vehicle trade data is that **the two sides of the same shipment "
    "disagree**. Exporter and importer records of identical flows diverge by "
    "multiples, and no major system separates used vehicles from new at the "
    "harmonized 6-digit level (HS 8703)."
)
st.table(pd.DataFrame({
    "Region": REGIONS,
    "Outbound evidence 📚": [
        "Recycling credited to exporting country for ELV parts (Directive "
        "2005/293/EC); Germany: substantial deregistered volumes with "
        "'statistical whereabouts unknown', predominantly used export",
        "1.83M used vehicles exported in 2023, +20.4% y/y (JAMA)",
        "~1,522–2,775 used cars/yr reported exported to its three main "
        "corridors, 2016–2020 (Comtrade)",
        "Used exports occur at scale but are unseparated inside the "
        "14.0M constructed exits (§2)"],
    "Mirror record": [
        "Intra-EU flows partially tracked; extra-EU destination records "
        "not reconciled in the ELV statistics",
        "Destination-side ELV treatment unrecorded — most volume lands in "
        "markets without formal ELV systems (Comtrade × UNEP-derived "
        "classification)",
        "Partner countries record importing only **4–12%** of what "
        "Singapore reports exporting — a 10–25× disagreement, every year, "
        "every corridor (Comtrade mirror)",
        "❌ no mirror computed — Census USA Trade Online (10-digit HTS, "
        "which flags used vehicles) not yet pulled"],
    "What it shows": [
        "The audit measures domestic treatment, not the exported fleet — "
        "the 60-year implied lifetime (§3) is the arithmetic shadow of "
        "this design",
        "A young-replacing market exporting its end-of-life liability to "
        "markets that cannot record receiving it",
        "Even world-class national data cannot make the two sides of its "
        "own trade agree — transshipment/origin re-attribution consistent, "
        "not proven",
        "The single largest unmeasured flow on this page: separating it "
        "is refinement #2 in §6"],
}))
st.caption(
    "**Claim:** the export mirror is broken everywhere it has been tested — "
    "partner records disagree with source records by up to 25×, and HS 8703 "
    "cannot distinguish a used car from a new one. The wedge in §3 therefore "
    "cannot be closed from trade data as published: it can be bounded "
    "(Singapore), estimated at destination (Japan), inferred from audit "
    "arithmetic (EU), or — in the US — not yet seen at all. **All four regimes "
    "lose the same flow at the same point — the border — regardless of how "
    "strong their domestic measurement is.** Mirror-gap magnitudes are as "
    "published in Comtrade-based reconciliations; a US mirror from Census "
    "10-digit HTS is the defined next pull."
)
st.divider()

# ============ 5 · Concordance ============
st.header("⑤ Where the classifications align — and where they cannot")
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

# ============ 6 · The gap and the path ============
st.header("⑥ The US gap — and what a proof-of-concept measurement requires")
st.markdown(
    "For the US to sit on this map as a *measured* market, in order of impact:\n\n"
    "1. **An ELV count** — none is published; the estimate here cannot separate "
    "scrappage from used-vehicle export.\n"
    "2. **A used-export series** — Census USA Trade Online carries 10-digit HTS "
    "detail that UN Comtrade flattens; separating exports from the 14.0M exits "
    "would close the wedge in §3 and give the US its mirror row in §4.\n"
    "3. **A vehicle-class concordance to M1/N1** — absent today (§5).\n"
    "4. **Japan/Singapore concordance rows** — their rates are computed (§2); "
    "aligning their vehicle classes completes the four-market panel.\n\n"
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
        "Mobility, AIRIA); Singapore COE certificate term (LTA); Japan "
        "used-vehicle exports 2023 (JAMA, 1.83M); trade-mirror gap magnitudes "
        "(Comtrade-based reconciliations)")
with m2:
    st.markdown(
        "**⚠️ Estimated** — US fleet exits 2023: 15,502,479 − 1,497,077 = "
        "**14,005,402**. Includes used exports. Not a measurement.\n\n"
        "**❌ Not published / not computed** — any audited US ELV count; "
        "Singapore's export-vs-scrap split; a US trade mirror (Census 10-digit "
        "HTS not yet pulled); Japan/Singapore classes in the concordance")

st.header("Why trust this — and where it stops")
st.table(pd.DataFrame({
    "Layer": ["Sources","EU rate","Japan rate","Singapore rate",
              "US rate (estimate)","Consumer layer (§3)","Export mirror (§4)",
              "Concordance"],
    "Trust basis": [
        "Counts from the project's approved register plus national statistical "
        "systems (Eurostat, BTS/FHWA, JARC, e-Stat/AIRIA, LTA); figures "
        "re-verified against source publications",
        "Reproduces Eurostat's published 2023 totals exactly",
        "System-reported numerator (manifest-tracked) over national fleet series",
        "Numerator and denominator from the same authority (LTA)",
        "Every input a published series; arithmetic stated in full (§2)",
        "Implied lifetimes are pure arithmetic on the rates; ages are "
        "literature-cited from fleet authorities",
        "Evidence assembled from published trade-mirror reconciliations and "
        "national export statistics; each cell tagged to its source",
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
        "Steady state assumed; slowly growing fleets understate implied "
        "lifetimes modestly — the EU/Japan gaps survive the caveat",
        "Mirror-gap magnitudes cited, not recomputed here; no US mirror "
        "exists yet — assembling one is refinement #2 (§6)",
        "Japan/Singapore classes not yet rowed"],
}))
st.caption(
    "Sources: Eurostat env_waselvt & road_eqs_carpda (2023) · BTS NTS 1-11 · "
    "FHWA MV-1 · FRED LTOTALNSA · JARC (FY2023 ELVs) · e-Stat/AIRIA (fleet, "
    "avg age) · JAMA (2023 exports) · Singapore LTA Annual Vehicle Statistics · "
    "ACEA · S&P Global Mobility · UN Comtrade (mirror reconciliations) · "
    "Census USA Trade Online (identified, not yet pulled). Figures verified in "
    "the project analysis notebook; warehouse-backed pipeline is the next build "
    "phase. *The Global ELV Recycling Gap* — NYU Stern MSBAi capstone.")
