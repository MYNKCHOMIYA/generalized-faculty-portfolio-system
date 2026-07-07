from fpdf import FPDF, XPos, YPos


class FacultyCV(FPDF):
    def header(self):
        # Adding a clean header to every page
        self.set_font("helvetica", "B", 15)
        self.set_text_color(41, 128, 185)  # A nice professional blue
        self.cell(
            0,
            10,
            "Curriculum Vitae",
            border=0,
            align="C",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        self.ln(15)

    def footer(self):
        # Page numbers at the bottom
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def generate_pdf_cv(profile, education, experience, publications, projects) -> bytes:
    """Generates a PDF CV from database records and returns it as raw bytes."""
    pdf = FacultyCV()
    pdf.add_page()

    # --- 1. Personal Information ---
    pdf.set_font("helvetica", "B", 24)
    pdf.set_text_color(44, 62, 80)

    # NEW SYNTAX: Replaced ln=True with new_x and new_y
    pdf.cell(
        0,
        10,
        f"{profile.first_name} {profile.last_name}",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )

    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(127, 140, 141)
    pdf.cell(0, 8, f"{profile.designation}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    if profile.phone_number:
        pdf.cell(
            0, 8, f"Phone: {profile.phone_number}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )
    pdf.ln(5)

    if profile.bio:
        pdf.set_font("helvetica", "", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, profile.bio)
        pdf.ln(10)

    # --- Helper function for section titles ---
    def section_title(title):
        pdf.set_font("helvetica", "B", 16)
        pdf.set_text_color(41, 128, 185)
        pdf.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
        pdf.ln(5)

    # --- 2. Education ---
    if education:
        section_title("Education")
        for edu in education:
            pdf.set_font("helvetica", "B", 12)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(
                0,
                6,
                f"{edu.degree} in {edu.field_of_study}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )

            pdf.set_font("helvetica", "", 11)
            pdf.set_text_color(0, 0, 0)
            date_str = f"{edu.start_date.strftime('%Y')} - {edu.end_date.strftime('%Y') if edu.end_date else 'Present'}"
            pdf.cell(
                0,
                6,
                f"{edu.institution} | {date_str}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.ln(4)

    # --- 3. Experience ---
    if experience:
        section_title("Professional Experience")
        for exp in experience:
            pdf.set_font("helvetica", "B", 12)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(
                0,
                6,
                f"{exp.job_title} at {exp.organization}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )

            pdf.set_font("helvetica", "I", 11)
            pdf.set_text_color(127, 140, 141)
            date_str = f"{exp.start_date.strftime('%b %Y')} - {exp.end_date.strftime('%b %Y') if exp.end_date else 'Present'}"
            pdf.cell(0, 6, date_str, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(4)

    # --- 4. Publications ---
    if publications:
        section_title("Selected Publications")
        for pub in publications:
            pdf.set_font("helvetica", "", 11)
            pdf.set_text_color(0, 0, 0)
            pub_text = f"• {pub.title} ({pub.publication_year}). {pub.publisher or ''} - {pub.publication_type}."
            pdf.multi_cell(0, 6, pub_text)
            pdf.ln(2)

    # Return the PDF as a byte string
    return pdf.output()
