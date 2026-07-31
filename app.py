import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="How the World Measures Vehicle Recycling",
                   layout="wide")

# ================= Design system =================
INK, SLATE, MIST = "#1A1F2B", "#3D4451", "#E5E8EC"
NAVY, STEEL, SAND, BURGUNDY, GREY = "#16324F", "#4F6D8F", "#8C7A4F", "#7A1F1F", "#9AA5B1"

st.markdown("""
<style>
html, body, [class*="css"] { font-family: "Segoe UI","Helvetica Neue",Arial,sans-serif; }
.block-container { max-width: 1180px; padding-top: 2.2rem; }
h1 { font-size: 2.05rem !important; font-weight: 700; letter-spacing: -.01em;
     color: #1A1F2B; border-bottom: 3px solid #16324F; padding-bottom: .55rem; }
h2 { font-size: 1.35rem !important; font-weight: 650; color: #16324F;
     margin-top: .6rem; letter-spacing: .01em; }
h3 { font-size: 1.05rem !important; font-weight: 650; color: #3D4451; }
p, li { color: #3D4451; font-size: .95rem; line-height: 1.55; }
[data-testid="stTable"] td, [data-testid="stTable"] th { font-size: .88rem; color: #1A1F2B; }
[data-testid="stTable"] th { background: #F4F6F8; font-weight: 650; }
[data-testid="stMetricLabel"] { color: #3D4451 !important; font-size: .82rem !important;
     text-transform: uppercase; letter-spacing: .06em; }
[data-testid="stMetricValue"] { color: #1A1F2B !important; font-weight: 700; }
.claim { border-left: 3px solid #16324F; background: #F4F6F8;
     padding: .8rem 1.1rem; margin: .4rem 0 1.2rem 0;
     font-size: .92rem; line-height: 1.55; color: #1A1F2B; }
.claim b { color: #16324F; }
.finding { border: 1px solid #16324F; border-left: 6px solid #7A1F1F;
     padding: .9rem 1.2rem; margin: .8rem 0 1.1rem 0;
     font-size: .95rem; line-height: 1.6; color: #1A1F2B; background: #FFFFFF; }
.badge { font-size: .74rem; font-weight: 700; letter-spacing: .07em;
     text-transform: uppercase; padding: .1rem .45rem; border-radius: 2px; }
.b-meas { background:#E8EEF4; color:#16324F; }
.b-der  { background:#EDEAE0; color:#5C4F2E; }
.b-lit  { background:#ECECEC; color:#3D4451; }
.b-est  { background:#F5E9E9; color:#7A1F1F; }
.b-abs  { background:#7A1F1F; color:#FFFFFF; }
[data-testid="stSidebar"] { background: #F4F6F8; }
[data-testid="stSidebar"] a { color: #16324F; text-decoration: none;
     font-size: .9rem; line-height: 2; }
</style>""", unsafe_allow_html=True)

def claim(html):
    st.markdown(f'<div class="claim"><b>Claim.</b> {html}</div>',
                unsafe_allow_html=True)

PLOT = dict(
    font=dict(family='"Segoe UI","Helvetica Neue",Arial,sans-serif',
              color=INK, size=13),
    paper_bgcolor="white", plot_bgcolor="white",
    xaxis=dict(gridcolor=MIST, linecolor=SLATE, tickcolor=SLATE),
    yaxis=dict(gridcolor=MIST, linecolor=SLATE, tickcolor=SLATE),
    legend=dict(orientation="h", y=1.12, font=dict(size=12)),
    margin=dict(t=30, b=10, l=10, r=10),
)

# ================= Data =================
EU_ELVS, EU_FLEET = 4_264_000, 256_229_781
US_FLEET, US_SALES, US_NET = 259_238_294, 15_502_479, 1_497_077
US_RETIRE = US_SALES - US_NET
JP_ELVS, JP_FLEET = 2_730_000, 61_950_000
SG_DEREG, SG_FLEET = 29_089, 651_302
EU_RATE, US_RATE = EU_ELVS/EU_FLEET, US_RETIRE/US_FLEET
JP_RATE, SG_RATE = JP_ELVS/JP_FLEET, SG_DEREG/SG_FLEET
REGIONS = ["EU-27","Japan","Singapore","United States"]
RATES = [EU_RATE, JP_RATE, SG_RATE, US_RATE]
AGES = [12.3, 9.5, 10.0, 12.5]
AGE_SRC = ["ACEA","AIRIA","COE certificate term (LTA)","S&P Global Mobility"]
SG_MIRROR = pd.DataFrame({
    "Year": [2016, 2017, 2018, 2019, 2020],
    "SG-reported exports": [1924, 2351, 2775, 1522, 1960],
    "Partner-recorded imports": [80, 145, 173, 177, 176],
})

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
DISP = DISP.sort_values("Rate", ascending=True).reset_index(drop=True)

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
     "Split from light trucks here — the split MV-1 cannot make."),
    ("US BTS (NTS 1-11)","Truck, combination","heavy_goods","Outside passenger scope."),
    ("US BTS (NTS 1-11)","Bus","bus",""),
    ("US BTS (NTS 1-11)","Highway, total (registered)","all_vehicles",""),
], columns=["Source system","Native class label","Harmonized class","Note"])

# ================= Sidebar navigation =================
with st.sidebar:
    st.markdown("### Contents")
    st.markdown(
        "[1 · The barometers](#sec1)  \n"
        "[2 · The rates — 2023](#sec2)  \n"
        "[3 · The consumer layer](#sec3)  \n"
        "[4 · The export mirror](#sec4)  \n"
        "[5 · The concordance](#sec5)  \n"
        "[6 · The US gap](#sec6)  \n"
        "[How to read this](#read)  \n"
        "[Why trust this](#trust)")
    st.markdown("---")
    st.markdown(
        '<p style="font-size:.8rem;color:#3D4451;">Analysis of end-of-life '
        'vehicle measurement across four markets. Every figure carries a '
        'confidence tier; burgundy marks constructed or absent data '
        'throughout.</p>', unsafe_allow_html=True)

# ================= Header =================
st.title("How the World Measures Vehicle Recycling")
st.markdown(
    "**Four major markets report end-of-life vehicles four different ways — where "
    "one reports them at all.** This page maps each region's measurement regime, "
    "states the scrappage rate each regime's data supports, shows how consumer "
    "replacement behavior drives the numbers, follows the missing flow into the "
    "trade records, documents where the classifications align and where they "
    "cannot, and identifies what a US measurement would require."
)
st.markdown(
    'Confidence levels used throughout &nbsp; '
    '<span class="badge b-meas">Measured</span> audited or system-reported &nbsp;·&nbsp; '
    '<span class="badge b-der">Derived</span> arithmetic on measured series &nbsp;·&nbsp; '
    '<span class="badge b-lit">Literature</span> cited from authorities &nbsp;·&nbsp; '
    '<span class="badge b-est">Estimated</span> constructed by the analysis &nbsp;·&nbsp; '
    '<span class="badge b-abs">Not published</span> no figure exists',
    unsafe_allow_html=True)
st.divider()

# ================= 1 =================
st.markdown('<div id="sec1"></div>', unsafe_allow_html=True)
st.header("1 · The barometers — what each region measures, and under what mandate")
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
    "ELV count status": ["Measured","Measured (system reports)",
                         "Derived (deregistrations)","Not published"],
}))
claim("Outcomes are measured in one region, system-reported in a second, "
      "derivable in a third, and absent in the fourth — the largest vehicle "
      "market of the four. Vehicles exported used carry their end-of-life with "
      "them; a market's regime determines whether its recycling gap can be "
      "seen at all.")
st.divider()

# ================= 2 =================
st.markdown('<div id="sec2"></div>', unsafe_allow_html=True)
st.header("2 · The rates each regime supports — 2023")
c = st.columns(4)
c[0].metric("EU-27 · Measured", f"{EU_RATE:.2%}",
            help="4,264,000 audited ELVs ÷ 256,229,781 cars (Eurostat)")
c[1].metric("Japan · Measured*", f"{JP_RATE:.2%}",
            help="2,730,000 ELVs (JARC manifest, FY2023) ÷ 61,950,000 cars (e-Stat/AIRIA)")
c[2].metric("Singapore · Derived", f"{SG_RATE:.2%}",
            help="29,089 car deregistrations ÷ 651,302 cars — both LTA")
c[3].metric("United States · Estimated", f"{US_RATE:.2%}",
            help="Constructed — arithmetic in the note below the chart")

tier = ["MEASURED · AUDITED", "MEASURED · SYSTEM", "DERIVED", "ESTIMATED"]
fig1 = go.Figure()
for i, (reg, rate, col) in enumerate(zip(REGIONS, RATES, [NAVY, STEEL, SAND, None])):
    if col:
        fig1.add_bar(x=[reg], y=[rate*100], marker_color=col, width=0.5,
                     showlegend=False)
    else:
        fig1.add_bar(x=[reg], y=[rate*100], width=0.5, showlegend=False,
                     marker=dict(color="rgba(0,0,0,0)",
                                 line=dict(color=BURGUNDY, width=2),
                                 pattern=dict(shape="/", fgcolor=BURGUNDY)))
    fig1.add_annotation(x=reg, y=rate*100, text=f"<b>{rate:.2%}</b>",
                        showarrow=False, yshift=14, font=dict(size=15, color=INK))
    fig1.add_annotation(x=reg, y=0, text=tier[i], showarrow=False, yshift=-34,
                        font=dict(size=10, color=SLATE))
fig1.update_layout(height=420, yaxis_title="Vehicles leaving fleet, % of fleet (2023)",
                   yaxis_range=[0, 6.3], **PLOT)
fig1.update_xaxes(showticklabels=True, ticklabelstandoff=24)
st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
claim("These four bars are four different kinds of number, each drawn to say "
      "so — solid fills are measured or derived; the outlined hatch is "
      "constructed. The US figure: <b>implied exits = 15,502,479 sales − "
      "1,497,077 net fleet growth = 14,005,402</b>, over a 259.2M light-duty "
      "fleet — counting every exit including used-vehicle exports, which the "
      "EU and Japan counts exclude. Scope caveats, direction known: EU "
      "numerator includes vans over a cars-only denominator; Japan's numerator "
      "covers all vehicle classes under the law over a passenger-car "
      "denominator — both slightly overstated. Higher is not better or worse; "
      "the quantities are constructed differently.")
with st.expander("Full numerator / denominator sourcing"):
    st.markdown(f"""
- **EU-27** (Measured) — audited ELVs {EU_ELVS:,} (Eurostat env_waselvt) ÷ passenger cars {EU_FLEET:,} (Eurostat road_eqs_carpda)
- **Japan** (Measured*) — ELVs collected for dismantling {JP_ELVS:,} (JARC manifest system, FY2023) ÷ passenger cars in use {JP_FLEET:,} (e-Stat/AIRIA, Mar 2023)
- **Singapore** (Derived) — permanent car deregistrations {SG_DEREG:,} ÷ cars & station-wagons {SG_FLEET:,} (both LTA Annual Vehicle Statistics)
- **US** (Estimated) — implied exits {US_RETIRE:,} (= FRED LTOTALNSA sales {US_SALES:,} − BTS 1-11 net fleet change {US_NET:,}) ÷ light-duty fleet {US_FLEET:,} (BTS 1-11, short + long wheelbase)
""")

st.subheader("Within the EU audit: a sevenfold spread")
show_eea = st.toggle("Include EEA reporters (Norway, Iceland, Liechtenstein)", True)
d = DISP if show_eea else DISP[~DISP.EEA]
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=d.Rate*100, y=d.Country, mode="markers",
    marker=dict(size=9,
                color=["white" if r else NAVY for r in d.EEA],
                line=dict(color=[GREY if r else NAVY for r in d.EEA], width=2)),
    hovertemplate="%{y}: %{x:.2f}%<extra></extra>", showlegend=False))
for _, row in d.iterrows():
    fig2.add_shape(type="line", x0=0, x1=row.Rate*100, y0=row.Country,
                   y1=row.Country, line=dict(color=MIST, width=2), layer="below")
fig2.add_vline(x=EU_RATE*100, line_dash="dot", line_color=BURGUNDY,
               annotation_text=f"EU-27 aggregate {EU_RATE:.2%}",
               annotation_position="top")
for country, label, shift in [("Ireland", "documents the most", 8),
                              ("Germany", "0.51% — the export gap", 8)]:
    if country in d.Country.values:
        r = d[d.Country == country].iloc[0]
        fig2.add_annotation(x=r.Rate*100, y=country, text=f"<b>{label}</b>",
                            showarrow=False, xshift=10, xanchor="left",
                            font=dict(size=11, color=INK))
fig2.update_layout(height=640, xaxis_title="Documented scrappage rate, 2023 (%)",
                   **PLOT)
st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
claim("Documented rates span 3.8% (Ireland) to 0.5% (Germany) inside one audit "
      "regime. Hollow markers are EEA reporters — they file under the "
      "Directive but are not EU members.")
with st.expander("Full country table"):
    st.dataframe(d.sort_values("Rate", ascending=False)
                 .style.format({"ELVs":"{:,.0f}","Fleet":"{:,.0f}","Rate":"{:.2%}"}),
                 use_container_width=True)
st.divider()

# ================= 3 =================
st.markdown('<div id="sec3"></div>', unsafe_allow_html=True)
st.header("3 · The consumer layer — replacement behavior drives every number above")
st.markdown(
    "A scrappage rate is the meeting point of two different events: a household's "
    "**decision to replace** a vehicle, and the vehicle's **documented "
    "end-of-life**. Comparing how long consumers actually keep vehicles against "
    "the lifetime each region's scrappage rate implies (at steady state, "
    "**implied lifetime = 1 ÷ rate**) shows how far apart those two events are "
    "in each market."
)
fig3 = go.Figure()
order = REGIONS[::-1]
ages_o = AGES[::-1]
lives_o = [1/r for r in RATES][::-1]
for reg, a, l in zip(order, ages_o, lives_o):
    fig3.add_shape(type="line", x0=a, x1=l, y0=reg, y1=reg,
                   line=dict(color=SLATE, width=3))
    fig3.add_annotation(x=(a+l)/2, y=reg, text=f"<b>+{l-a:.0f} yrs</b>",
                        showarrow=False, yshift=14, font=dict(size=11, color=BURGUNDY))
fig3.add_trace(go.Scatter(x=ages_o, y=order, mode="markers",
                          name="Average fleet age (literature)",
                          marker=dict(size=13, color=SLATE),
                          hovertemplate="%{y}: held ~%{x} yrs<extra></extra>"))
fig3.add_trace(go.Scatter(x=lives_o, y=order, mode="markers",
                          name="Implied lifetime = 1 ÷ rate (derived)",
                          marker=dict(size=13, color=BURGUNDY),
                          hovertemplate="%{y}: %{x:.0f} yrs implied<extra></extra>"))
fig3.update_layout(height=420, xaxis_title="Years", **PLOT)
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
st.table(pd.DataFrame({
    "Region": REGIONS,
    "Avg fleet age (literature)": [f"{a} yrs ({s})" for a, s in zip(AGES, AGE_SRC)],
    "Implied lifetime (derived)": [f"{1/r:.0f} yrs" for r in RATES],
    "Gap": [f"{1/r - a:+.0f} yrs" for r, a in zip(RATES, AGES)],
}))
claim("Replacement is a spending decision; documented scrappage is a "
      "measurement event — and in every measured market they are decades "
      "apart. The line between each pair of dots <b>is</b> the gap: EU "
      "consumers replace around year 12, yet the documented rate implies cars "
      "live <b>60 years</b> — the stretch is vehicles leaving the audit as "
      "used exports, not deaths. Japan is sharper — inspection (shaken) costs "
      "push replacement toward year 9–10, and 1.83M used vehicles exported in "
      "2023 (JAMA) exit the recycling system young. Singapore's COE makes "
      "replacement timing a policy price rather than a consumer choice. The "
      "US is the near-reconciled case — implied 18.5 years against a "
      "12.5-year average age — precisely because its constructed count "
      "includes exports. <b>The wedge between replacement and documented "
      "end-of-life is the recycling gap's supply side: consumer upgrade "
      "cycles feed the export flow that measurement loses.</b> Steady-state "
      "assumption stated; slowly growing fleets understate implied lifetimes "
      "modestly — the EU and Japan impossibilities survive the caveat.")
st.divider()

# ================= 4 =================
st.markdown('<div id="sec4"></div>', unsafe_allow_html=True)
st.header("4 · The export mirror — where the wedge goes, and where records disagree")
st.markdown(
    "Section 3 shows vehicles leaving fleets years before documented "
    "end-of-life. Trade records are where that flow should reappear — and the "
    "defining feature of used-vehicle trade data is that **the two sides of "
    "the same shipment disagree**. The one corridor with published numbers on "
    "both sides makes the disagreement visible:"
)
fig4 = go.Figure()
fig4.add_bar(x=SG_MIRROR.Year, y=SG_MIRROR["SG-reported exports"],
             name="Singapore reports exporting", marker_color=NAVY, width=0.35,
             offsetgroup=0)
fig4.add_bar(x=SG_MIRROR.Year, y=SG_MIRROR["Partner-recorded imports"],
             name="Partners record importing", marker_color=BURGUNDY, width=0.35,
             offsetgroup=1)
fig4.update_layout(height=380, barmode="group",
                   yaxis_title="Used passenger cars (SG → ID/TH/AU)",
                   **PLOT)
st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
claim("The burgundy bars are barely visible next to the navy — <b>that is the "
      "finding</b>. Partner countries record importing only 4–12% of what "
      "Singapore reports exporting: a 10–25× disagreement, every year, every "
      "corridor (Comtrade mirror, 2016–2020, as published in the pilot "
      "reconciliation). The same mirror cannot even be attempted for the US.")
st.table(pd.DataFrame({
    "Region": REGIONS,
    "Outbound evidence (literature)": [
        "Recycling credited to exporting country for ELV parts (Directive "
        "2005/293/EC); Germany: substantial deregistered volumes with "
        "'statistical whereabouts unknown', predominantly used export",
        "1.83M used vehicles exported in 2023, +20.4% y/y (JAMA)",
        "~1,522–2,775 used cars/yr reported exported to its three main "
        "corridors, 2016–2020 (Comtrade)",
        "Used exports occur at scale but are unseparated inside the "
        "14.0M constructed exits (Sec. 2)"],
    "Mirror record": [
        "Intra-EU flows partially tracked; extra-EU destination records "
        "not reconciled in the ELV statistics",
        "Destination-side ELV treatment unrecorded — most volume lands in "
        "markets without formal ELV systems (Comtrade × UNEP-derived "
        "classification)",
        "Partner countries record importing only 4–12% of what Singapore "
        "reports exporting (chart above)",
        "No mirror computed — Census USA Trade Online (10-digit HTS, "
        "which flags used vehicles) not yet pulled"],
    "What it shows": [
        "The audit measures domestic treatment, not the exported fleet — "
        "the 60-year implied lifetime (Sec. 3) is the arithmetic shadow of "
        "this design",
        "A young-replacing market exporting its end-of-life liability to "
        "markets that cannot record receiving it",
        "Even world-class national data cannot make the two sides of its "
        "own trade agree — transshipment/origin re-attribution consistent, "
        "not proven",
        "The single largest unmeasured flow on this page: separating it "
        "is refinement 2 in Sec. 6"],
}))
claim("The export mirror is broken everywhere it has been tested — and HS "
      "8703 cannot distinguish a used car from a new one. The wedge in "
      "Section 3 therefore cannot be closed from trade data as published: it "
      "can be bounded (Singapore), estimated at destination (Japan), inferred "
      "from audit arithmetic (EU), or — in the US — not yet seen at all. "
      "<b>All four regimes lose the same flow at the same point — the border "
      "— regardless of how strong their domestic measurement is.</b>")
st.divider()

# ================= 5 =================
st.markdown('<div id="sec5"></div>', unsafe_allow_html=True)
st.header("5 · Where the classifications align — and where they cannot")
st.markdown(
    "Cross-region comparison requires reconciling classification systems never "
    "designed to align. The concordance preserves each source's native label "
    "and assigns a harmonized class where one defensibly exists — "
    "**NO_EQUIVALENT** recorded where none does. Decisive entries: no US "
    "federal class corresponds to EU M1, and US 'Trucks' merges light and "
    "heavy vehicles the EU separates at 3.5t."
)
st.markdown(
    '<div class="finding"><b>Finding — the classification disagreement is '
    'itself a data point.</b> The two US federal sources on this page disagree '
    'with each other: FHWA MV-1 reports all trucks in one undifferentiated '
    'column, while BTS Table 1-11 splits light-duty from heavy. The US '
    'therefore lacks not just an ELV count but a <b>single consistent vehicle '
    'classification</b> — any future US measurement must first choose which '
    'federal taxonomy to measure in. No comparable internal disagreement '
    'exists in the EU, Japan, or Singapore systems, each of which classifies '
    'under one authority.</div>', unsafe_allow_html=True)
st.dataframe(CW, use_container_width=True)
claim("Comparison is only possible at the combined light-duty level because "
      "that is the only scope both systems can approximately express. "
      "Non-passenger classes are rowed deliberately: the concordance maps the "
      "full classification terrain so that exclusions are visible decisions "
      "rather than omissions; so that Japan's numerator — which spans all "
      "vehicle classes under its law — can be described at all; and because "
      "the US sources' internal disagreement (finding above) is only "
      "demonstrable with the non-passenger rows present. Scope is enforced in "
      "the analysis (Sec. 2), not by deleting rows. The same structure extends "
      "to Japan's registration classes (incl. kei vehicles) and Singapore's "
      "COE categories — not yet rowed.")
st.divider()

# ================= 6 =================
st.markdown('<div id="sec6"></div>', unsafe_allow_html=True)
st.header("6 · The US gap — and what a proof-of-concept measurement requires")
st.markdown(
    "For the US to sit on this map as a *measured* market, in order of impact:\n\n"
    "1. **An ELV count** — none is published; the estimate here cannot separate "
    "scrappage from used-vehicle export.\n"
    "2. **A used-export series** — Census USA Trade Online carries 10-digit HTS "
    "detail that UN Comtrade flattens; separating exports from the 14.0M exits "
    "would close the wedge in Sec. 3 and give the US its mirror row in Sec. 4.\n"
    "3. **A vehicle-class concordance to M1/N1** — absent today, and "
    "complicated by the US sources' internal disagreement (Sec. 5).\n"
    "4. **Japan/Singapore concordance rows** — their rates are computed "
    "(Sec. 2); aligning their vehicle classes completes the four-market panel.\n\n"
    "The EU series supports history to 2008; the US fleet series breaks at the "
    "2007 federal reclassification. A multi-year, four-market panel is feasible "
    "within those bounds."
)
st.divider()

# ================= Read / trust =================
st.markdown('<div id="read"></div>', unsafe_allow_html=True)
st.header("How to read this")
m1, m2 = st.columns(2)
with m1:
    st.markdown(
        '<span class="badge b-meas">Measured</span> — EU ELVs & rates '
        '(Eurostat env_waselvt); EU & member fleets (road_eqs_carpda); US '
        'fleet (BTS 1-11); US registrations cross-check (FHWA MV-1); US sales '
        '(FRED LTOTALNSA); Japan ELVs (JARC manifest, FY2023); Japan fleet '
        '(e-Stat/AIRIA); Singapore deregistrations & fleet (LTA)<br><br>'
        '<span class="badge b-der">Derived</span> — all four rates; implied '
        'lifetimes (1 ÷ rate, steady-state assumption)<br><br>'
        '<span class="badge b-lit">Literature</span> — average fleet ages '
        '(ACEA, S&P Global Mobility, AIRIA); Singapore COE certificate term '
        '(LTA); Japan used exports 2023 (JAMA, 1.83M); trade-mirror gap '
        'magnitudes (Comtrade-based reconciliations)',
        unsafe_allow_html=True)
with m2:
    st.markdown(
        '<span class="badge b-est">Estimated</span> — US fleet exits 2023: '
        '15,502,479 − 1,497,077 = <b>14,005,402</b>. Includes used exports. '
        'Not a measurement.<br><br>'
        '<span class="badge b-abs">Not published</span> — any audited US ELV '
        'count; Singapore\'s export-vs-scrap split; a US trade mirror (Census '
        '10-digit HTS not yet pulled); Japan/Singapore classes in the '
        'concordance', unsafe_allow_html=True)

st.markdown('<div id="trust"></div>', unsafe_allow_html=True)
st.header("Why trust this — and where it stops")
st.table(pd.DataFrame({
    "Layer": ["Sources","EU rate","Japan rate","Singapore rate",
              "US rate (estimate)","Consumer layer (Sec. 3)",
              "Export mirror (Sec. 4)","Concordance (Sec. 5)"],
    "Trust basis": [
        "Counts from the project's approved source register plus national "
        "statistical systems (Eurostat, BTS/FHWA, JARC, e-Stat/AIRIA, LTA); "
        "figures re-verified against source publications",
        "Reproduces Eurostat's published 2023 totals exactly",
        "System-reported numerator (manifest-tracked) over national fleet series",
        "Numerator and denominator from the same authority (LTA)",
        "Every input a published series; arithmetic stated in full (Sec. 2)",
        "Implied lifetimes are pure arithmetic on the rates; ages are "
        "literature-cited from fleet authorities",
        "Singapore mirror charted from published reconciliation figures; "
        "other cells tagged to their sources",
        "12 labels, native classifications preserved, NO_EQUIVALENT permitted; "
        "the US internal disagreement is visible in the rows themselves"],
    "Where it breaks": [
        "US estimate requires a sales series outside the register; FRED "
        "supplies it — disclosed",
        "M1+N1 numerator over cars-only denominator, slightly overstated; "
        "EU aggregate partly estimated for non-reporters",
        "Numerator covers all vehicle classes under the law; denominator is "
        "passenger cars — overstated, direction known",
        "Deregistrations include exports; export-vs-scrap split unpublished",
        "Cannot separate scrappage from export; single year; not a like "
        "measurement to the measured bars — and drawn so",
        "Steady state assumed; slowly growing fleets understate implied "
        "lifetimes modestly — the EU/Japan gaps survive the caveat",
        "Mirror-gap magnitudes cited, not recomputed here; no US mirror "
        "exists yet — assembling one is refinement 2 (Sec. 6)",
        "Japan/Singapore classes not yet rowed"],
}))
st.markdown(
    '<p style="font-size:.82rem;color:#3D4451;margin-top:1rem;">Sources: '
    'Eurostat env_waselvt & road_eqs_carpda (2023) · BTS NTS 1-11 · FHWA MV-1 '
    '· FRED LTOTALNSA · JARC (FY2023 ELVs) · e-Stat/AIRIA (fleet, avg age) · '
    'JAMA (2023 exports) · Singapore LTA Annual Vehicle Statistics · ACEA · '
    'S&P Global Mobility · UN Comtrade (mirror reconciliations) · Census USA '
    'Trade Online (identified, not yet pulled). Figures verified in the '
    'project analysis notebook; warehouse-backed pipeline is the next build '
    'phase. <i>The Global ELV Recycling Gap</i> — NYU Stern MSBAi capstone.</p>',
    unsafe_allow_html=True)
