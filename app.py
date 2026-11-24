import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import date, timedelta

st.set_page_config(
    page_title="AGC Recruitment Maker",
    page_icon="🛠️",
    layout="wide"
)

COMPANY = "AMMAR SULEIMAN AL NIMR GENERAL CONTRACTING EST."

CONTACTS = [
    "0591265037",
    "0560427544",
    "0554301956",
    "0537254911",
    "0581378417"
]

OFFICE = "SAUDI AIRLINE, 4th Floor, Flat 3-2"

DEFAULT_TRADES = [
    "Fire Watch", "Steel Fixer", "Mason",
    "Carpenter", "Electrician", "Plumber",
    "Welder", "Pipe Fitter", "Rigger",
    "Scaffolder", "Helper", "Civil Foreman",
    "Mechanical Technician", "Painter",
    "Tile Mason", "HVAC Technician",
    "Safety Officer", "Heavy Driver",
    "Equipment Operator"
]

DOCUMENTS = [
    "Valid Iqama",
    "Updated CV",
    "Valid Ajeer",
    "Valid Authorization",
    "TUV / T-Card",
    "Chamber Authorization"
]


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]

    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass

    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    words = str(text).split()
    lines = []
    current = ""

    for word in words:
        test = (current + " " + word).strip()

        if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def create_poster(data):
    W = 1600
    margin = 85

    title_font = get_font(43, True)
    heading_font = get_font(66, True)
    sub_font = get_font(30, True)
    job_font = get_font(39, True)
    normal_font = get_font(27)
    small_font = get_font(23)
    footer_font = get_font(30, True)

    temp = Image.new("RGB", (W, 100), "white")
    td = ImageDraw.Draw(temp)

    y = 360 + len(data["jobs"]) * 205
    y += 240

    if data["documents"]:
        y += 65 + len(data["documents"]) * 45

    if data["custom_document"]:
        y += 50

    if data["interview"]:
        y += 65

    if data["show_office"]:
        y += 100

    if data["maps"]:
        y += 55

    footer_height = 245
    H = max(1500, y + footer_height + 100)

    img = Image.new("RGB", (W, H), "#F1F4F8")
    d = ImageDraw.Draw(img)

    navy = "#102A43"
    blue = "#1769AA"
    orange = "#F5A742"
    light = "#EAF2F8"

    d.rounded_rectangle(
        (25, 25, W - 25, H - 25),
        radius=35,
        fill="white",
        outline=navy,
        width=7
    )

    d.rounded_rectangle(
        (35, 35, W - 35, 320),
        radius=30,
        fill=navy
    )

    d.text(
        (80, 75),
        COMPANY,
        font=title_font,
        fill="white"
    )

    d.text(
        (80, 145),
        data["heading"].upper(),
        font=heading_font,
        fill=orange
    )

    d.text(
        (80, 245),
        "SAUDI ARABIA | URGENT REQUIREMENT",
        font=sub_font,
        fill="white"
    )

    y = 355

    d.rounded_rectangle(
        (80, y, W - 80, y + 85),
        radius=18,
        fill=light
    )

    d.text(
        (115, y + 19),
        "AVAILABLE VACANCIES",
        font=footer_font,
        fill=navy
    )

    y += 110

    for index, job in enumerate(data["jobs"], 1):

        d.rounded_rectangle(
            (80, y, W - 80, y + 180),
            radius=20,
            fill="#F7FAFC",
            outline="#D5E1EA",
            width=3
        )

        d.ellipse(
            (110, y + 40, 180, y + 110),
            fill=blue
        )

        d.text(
            (133, y + 52),
            str(index),
            font=get_font(34, True),
            fill="white"
        )

        d.text(
            (220, y + 22),
            job["trade"].upper(),
            font=job_font,
            fill=navy
        )

        d.text(
            (220, y + 83),
            f'QUANTITY: {job["quantity"]}    RATE: {job["rate"]} SAR',
            font=normal_font,
            fill=navy
        )

        d.text(
            (220, y + 130),
            "AJEER: " + job["ajeer"],
            font=small_font,
            fill=blue
        )

        y += 200

    y += 10

    d.rounded_rectangle(
        (80, y, W - 80, y + 190),
        radius=20,
        fill=navy
    )

    d.text(
        (115, y + 20),
        "PROJECT DETAILS",
        font=footer_font,
        fill="white"
    )

    d.text(
        (115, y + 75),
        "LOCATION: " + data["location"],
        font=normal_font,
        fill="white"
    )

    d.text(
        (115, y + 125),
        "DURATION: " + data["duration"],
        font=normal_font,
        fill=orange
    )

    y += 220

    if data["documents"] or data["custom_document"]:

        d.text(
            (100, y),
            "REQUIRED DOCUMENTS",
            font=footer_font,
            fill=navy
        )

        y += 55

        for doc in data["documents"]:
            d.text(
                (115, y),
                "• " + doc,
                font=normal_font,
                fill=navy
            )
            y += 45

        if data["custom_document"]:
            for line in wrap_text(
                d, data["custom_document"],
                normal_font, 1300
            ):
                d.text(
                    (115, y),
                    "• " + line,
                    font=normal_font,
                    fill=navy
                )
                y += 45

    if data["interview"]:
        y += 15
        d.text(
            (100, y),
            "TEST / INTERVIEW: " + data["interview"],
            font=normal_font,
            fill=blue
        )
        y += 55

    if data["show_office"]:
        d.text(
            (100, y),
            "OFFICE: " + OFFICE,
            font=normal_font,
            fill=navy
        )
        y += 45

        d.text(
            (100, y),
            "Send WhatsApp message to get office location link.",
            font=small_font,
            fill=blue
        )
        y += 45

    if data["maps"]:
        for line in wrap_text(
            d, "OFFICE MAP: " + data["maps"],
            small_font, 1300
        ):
            d.text(
                (100, y),
                line,
                font=small_font,
                fill=blue
            )
            y += 35

    footer = H - 270

    d.rounded_rectangle(
        (80, footer, W - 80, H - 70),
        radius=22,
        fill=light
    )

    d.text(
        (115, footer + 20),
        "CONTACT / WHATSAPP",
        font=footer_font,
        fill=navy
    )

    contacts = " | ".join(data["contacts"])

    for i, line in enumerate(
        wrap_text(d, contacts, normal_font, 1300)
    ):
        d.text(
            (115, footer + 75 + i * 40),
            line,
            font=normal_font,
            fill=blue
        )

    d.text(
        (115, H - 115),
        "ADVERTISEMENT DATE: " + data["date"],
        font=small_font,
        fill=navy
    )

    return img


st.title("AGC Recruitment Advertisement Maker")
st.caption(COMPANY)

if "trades" not in st.session_state:
    st.session_state.trades = DEFAULT_TRADES.copy()

with st.sidebar:
    st.header("TRADE MANAGEMENT")

    new_trade = st.text_input("Add New Trade")

    if st.button("Add Trade"):
        if new_trade.strip():
            if new_trade.strip() not in st.session_state.trades:
                st.session_state.trades.append(new_trade.strip())
                st.success("Trade added successfully.")

    remove_trade = st.selectbox(
        "Remove Trade",
        ["Select"] + st.session_state.trades
    )

    if st.button("Delete Trade"):
        if remove_trade != "Select":
            st.session_state.trades.remove(remove_trade)
            st.rerun()


left, right = st.columns(2)

with left:

    st.header("ADVERTISEMENT DETAILS")

    heading = st.text_input(
        "Advertisement Heading",
        "URGENT REQUIREMENT"
    )

    location = st.text_input(
        "Project Location",
        "AD DUWAYHI"
    )

    duration = st.text_input(
        "Work Duration",
        "4 MONTHS"
    )

    ad_date = st.date_input(
        "Advertisement Date",
        date.today()
    )

    maps = st.text_input(
        "Google Maps Link (Optional)"
    )

    show_office = st.checkbox(
        "Show Office Address",
        value=True
    )

    st.subheader("Required Documents")

    documents = st.multiselect(
        "Select Documents",
        DOCUMENTS
    )

    custom_document = st.text_input(
        "Additional Document"
    )

    interview_enabled = st.checkbox(
        "Add Test / Interview Details"
    )

    interview = ""

    if interview_enabled:

        interview_date = st.date_input(
            "Interview Date",
            date.today() + timedelta(days=1)
        )

        interview_time = st.time_input(
            "Interview Time"
        )

        interview = (
            interview_date.strftime("%d %b %Y")
            + " at "
            + interview_time.strftime("%I:%M %p")
        )


with right:

    st.header("VACANCY INFORMATION")

    number_jobs = st.number_input(
        "Number of Trades",
        min_value=1,
        max_value=10,
        value=2
    )

    jobs = []

    for i in range(int(number_jobs)):

        with st.expander(
            f"Vacancy {i + 1}",
            expanded=True
        ):

            trade = st.selectbox(
                f"Trade {i + 1}",
                st.session_state.trades,
                key=f"trade_{i}"
            )

            quantity = st.number_input(
                f"Quantity {i + 1}",
                min_value=1,
                value=10,
                key=f"quantity_{i}"
            )

            rate = st.number_input(
                f"Rate in SAR {i + 1}",
                min_value=0.0,
                value=18.0 if i == 0 else 16.0,
                key=f"rate_{i}"
            )

            ajeer = st.selectbox(
                f"Ajeer Requirement {i + 1}",
                [
                    "Must Have Ajeer",
                    "Ajeer Preferred",
                    "Not Required"
                ],
                key=f"ajeer_{i}"
            )

            jobs.append({
                "trade": trade,
                "quantity": quantity,
                "rate": rate,
                "ajeer": ajeer
            })

    st.subheader("CONTACT NUMBERS")

    contacts = st.multiselect(
        "Select Contact Numbers",
        CONTACTS,
        default=[CONTACTS[0]]
    )


if st.button(
    "GENERATE ADVERTISEMENT",
    type="primary",
    use_container_width=True
):

    if not jobs:
        st.error("Please add at least one vacancy.")

    else:

        data = {
            "heading": heading,
            "location": location,
            "duration": duration,
            "date": ad_date.strftime("%d %b %Y"),
            "maps": maps,
            "show_office": show_office,
            "documents": documents,
            "custom_document": custom_document,
            "interview": interview,
            "jobs": jobs,
            "contacts": contacts
        }

        st.session_state.poster = create_poster(data)


if "poster" in st.session_state:

    st.divider()

    st.header("ADVERTISEMENT PREVIEW")

    poster = st.session_state.poster

    st.image(
        poster,
        use_container_width=True
    )

    png_buffer = BytesIO()
    poster.save(png_buffer, format="PNG")

    st.download_button(
        "DOWNLOAD HD PNG",
        data=png_buffer.getvalue(),
        file_name="AGC_Recruitment.png",
        mime="image/png",
        use_container_width=True
    )

    jpg_buffer = BytesIO()
    poster.save(
        jpg_buffer,
        format="JPEG",
        quality=95
    )

    st.download_button(
        "DOWNLOAD JPG",
        data=jpg_buffer.getvalue(),
        file_name="AGC_Recruitment.jpg",
        mime="image/jpeg",
        use_container_width=True
    )

st.divider()

st.caption(
    "AGC Recruitment Advertisement Maker | "
    "Please verify all details before publishing."
)
