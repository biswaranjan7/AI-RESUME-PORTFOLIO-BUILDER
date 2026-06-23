import streamlit as st
from fpdf import FPDF
import os
import re

# --- Configuration ---
st.set_page_config(page_title="AI Resume Builder", page_icon="📄", layout="wide")

# --- Custom Python Class for PDF Generation ---
class ResumePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Professional Resume', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 7, body)
        self.ln()

    def chapter_link(self, title, url):
        self.set_font('Arial', 'B', 11)
        # Simple text representation of link (FPDF HTML support is limited in basic version)
        self.cell(0, 7, f"{title} (Link: {url})", 0, 1, 'L')
        self.ln(2)

# --- Local "Smart Engine" (Offline AI Simulation) ---

def get_smart_suggestion(mode, input_text):
    """Uses local dictionary mapping and Regex to simulate AI text enhancement."""
    action_verbs = {
        r'\bdid\b': 'Executed',
        r'\bmade\b': 'Developed',
        r'\bhelped\b': 'Facilitated',
        r'\bworked on\b': 'Contributed to',
        r'\bmanaged\b': 'Orchestrated',
        r'\bkept track of\b': 'Monitored',
        r'\btalked to\b': 'Communicated with',
        r'\bwrote\b': 'Authored',
        r'\bfixed\b': 'Resolved',
        r'\bthought of\b': 'Conceptualized',
        r'\bsold\b': 'Market and sold',
        r'\bled\b': 'Directed',
        r'\bcreated\b': 'Engineered',
        r'\bused\b': 'Leveraged',
        r'\bran\b': 'Operated'
    }

    if mode == "polish":
        if not input_text:
            return "Please enter text to polish."
        improved_text = input_text
        for pattern, replacement in action_verbs.items():
            improved_text = re.sub(pattern, replacement, improved_text, flags=re.IGNORECASE)
        improved_text = improved_text[0].upper() + improved_text[1:]
        if improved_text.lower() == input_text.lower():
            return "Your text looks good!"
        return f"✨ **Suggested Polish:**\n{improved_text}"

    elif mode == "summary":
        if not input_text:
            return "Please enter your skills."
        skills_list = [s.strip() for s in input_text.split(',') if s.strip()]
        skills_str = ", ".join(skills_list[:3])
        return f"Highly motivated professional with a strong background in {skills_str}. Proven ability to deliver results in fast-paced environments."
    return "No suggestion available."

def extract_keywords(job_text):
    """Simple keyword extractor using Regex."""
    if not job_text:
        return ""
    words = re.findall(r'\b\w{6,}\b', job_text)
    common = {"experience", "required", "looking", "candidate", "ability", "position", "company", "environment"}
    keywords = list(set([w for w in words if w.lower() not in common]))
    return ", ".join(keywords[:10])

def calculate_match_score(resume_data, keywords):
    """Calculates a score (0.0 to 1.0) based on keyword density."""
    if not keywords:
        return 0.0
    
    keyword_list = [k.strip().lower() for k in keywords.split(',')]
    # Combine all resume text
    all_text = (
        f" {resume_data.get('summary', '')} "
        f" {resume_data.get('skills', '')} "
        f" {' '.join([j['description'] for j in resume_data.get('experience', [])])}"
    ).lower()
    
    matches = sum(1 for k in keyword_list if k in all_text)
    return min(1.0, matches / max(1, len(keyword_list)))

def generate_pdf_resume(data):
    """Generates a PDF file object using FPDF."""
    pdf = ResumePDF()
    pdf.add_page()
    
    # Header
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 10, data.get('name', 'Your Name'), 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    contact_line = f"{data.get('email', '')} | {data.get('phone', '')} | {data.get('linkedin', '')}"
    pdf.cell(0, 10, contact_line, 0, 1, 'C')
    pdf.ln(10)

    # Summary
    if data.get('summary'):
        pdf.chapter_title("Professional Summary")
        pdf.chapter_body(data['summary'])

    # Experience
    if data.get('experience'):
        pdf.chapter_title("Experience")
        for job in data['experience']:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, f"{job['role']} at {job['company']}", 0, 1)
            pdf.set_font('Arial', 'I', 10)
            pdf.cell(0, 6, job['date'], 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(0, 7, job['description'])
            pdf.ln(2)

    # Projects (New Feature)
    if data.get('projects'):
        pdf.chapter_title("Key Projects")
        for proj in data['projects']:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, proj['title'], 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(0, 7, proj['description'])
            if proj['link']:
                pdf.set_font('Arial', 'I', 10)
                pdf.cell(0, 6, f"Link: {proj['link']}", 0, 1)
            pdf.ln(2)

    # Education
    if data.get('education'):
        pdf.chapter_title("Education")
        pdf.chapter_body(data['education'])

    # Skills
    if data.get('skills'):
        pdf.chapter_title("Skills")
        pdf.chapter_body(data['skills'])

    pdf_path = "generated_resume.pdf"
    pdf.output(pdf_path)
    return pdf_path

# --- Main Application Logic ---

def main():
    st.title("🤖 AI Resume & Portfolio Suite")
    st.caption("Build Resumes, Portfolios, and Cover Letters.")

    # --- Sidebar ---
    with st.sidebar:
        st.header("1. Personal Details")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        linkedin = st.text_input("LinkedIn URL")

        st.header("2. Target Job")
        job_desc = st.text_area("Paste Job Description")
        job_title_target = st.text_input("Target Job Title")
        company_target = st.text_input("Target Company Name")
        
        # Extract Keywords
        keywords = ""
        if job_desc:
            keywords = extract_keywords(job_desc)
            st.info(f"🔍 **Keywords:**\n{keywords}")

    # --- Feature: Resume Scorer ---
    with st.expander("📊 Resume Strength Score (AI Analysis)", expanded=False):
        if keywords:
            # Mock resume data for scoring logic
            mock_data = {
                'summary': st.session_state.get('summary', ''), 
                'skills': st.session_state.get('skills', ''),
                'experience': st.session_state.get('experience_list', [])
            }
            # Note: In a real reactive app, we'd pass live values, but here we calculate on button click to avoid lag
            if st.button("Calculate Match Score"):
                score = calculate_match_score(mock_data, keywords)
                st.metric("Match Score", f"{int(score*100)}%")
                st.progress(score)
                
                if score < 0.5:
                    st.warning("Low match! Try using the 'Polish' tools to add more keywords from the JD.")
                else:
                    st.success("Good match! Your resume aligns well with the job description.")
        else:
            st.info("Paste a Job Description to enable scoring.")

    # --- Feature: Smart Tools ---
    with st.expander("✨ Smart Writing Tools", expanded=True):
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.subheader("Polish Bullet")
            txt = st.text_area("Rewrite this:", height=70)
            if st.button("Polish"): st.info(get_smart_suggestion("polish", txt))
        with col_t2:
            st.subheader("Gen. Bio Template")
            sk = st.text_input("Your Skills")
            if st.button("Generate"): st.success(get_smart_suggestion("summary", sk))

    # --- Feature: Cover Letter ---
    with st.expander("✉️ Cover Letter Generator"):
        st.markdown("Generate a cover letter based on your target job.")
        if st.button("Draft Cover Letter"):
            with st.spinner("Drafting..."):
                letter_body = f"""Dear Hiring Manager at {company_target if company_target else '[Company Name]'},

I am writing to express my strong interest in the {job_title_target if job_title_target else '[Job Title]'} position. With my background in skills such as {st.session_state.get('skills', 'various technologies')}, I am confident in my ability to contribute effectively to your team.

My experience includes working on impactful projects, where I honed my ability to collaborate and deliver results. I am particularly drawn to this opportunity at {company_target if company_target else 'your company'} because of your commitment to innovation.

Thank you for considering my application. I look forward to the possibility of discussing how I can contribute to your success.

Sincerely,
{name if name else '[Your Name]'}"""
                st.text_area("Your Draft Cover Letter", letter_body, height=300)

    # --- Main Editor ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Resume & Portfolio Content")
        
        # Summary
        st.session_state['summary'] = st.text_area("Professional Summary", height=80)
        st.session_state['skills'] = st.text_input("Skills (Comma separated)")

        # Experience
        st.subheader("Work Experience")
        if 'experience_list' not in st.session_state:
            st.session_state.experience_list = [{}]
        for i, job in enumerate(st.session_state.experience_list):
            with st.expander(f"Job #{i+1}", expanded=True):
                role = st.text_input("Role", key=f"role_{i}")
                company = st.text_input("Company", key=f"comp_{i}")
                date = st.text_input("Date", key=f"date_{i}")
                desc = st.text_area("Description", key=f"desc_{i}", height=80)
                st.session_state.experience_list[i] = {'role': role, 'company': company, 'date': date, 'description': desc}
        if st.button("Add Job"):
            st.session_state.experience_list.append({})
            st.rerun()

        # Projects (New Feature)
        st.subheader("🚀 Portfolio / Projects")
        if 'project_list' not in st.session_state:
            st.session_state.project_list = [{}]
        for i, proj in enumerate(st.session_state.project_list):
            with st.expander(f"Project #{i+1}", expanded=True):
                title = st.text_input("Project Title", key=f"ptitle_{i}")
                link = st.text_input("Link (GitHub/Live)", key=f"plink_{i}")
                desc = st.text_area("Description", key=f"pdesc_{i}", height=60)
                st.session_state.project_list[i] = {'title': title, 'link': link, 'description': desc}
        if st.button("Add Project"):
            st.session_state.project_list.append({})
            st.rerun()

        # Education
        st.subheader("Education")
        education = st.text_area("Degree, Uni, Year")

    with col2:
        st.header("Preview & Download")
        
        # Gather Data
        resume_data = {
            'name': name, 'email': email, 'phone': phone, 'linkedin': linkedin,
            'summary': st.session_state.get('summary', ''),
            'experience': st.session_state.experience_list,
            'projects': st.session_state.project_list,
            'education': education,
            'skills': st.session_state.get('skills', '')
        }

        # Live Preview
        st.markdown("---")
        st.markdown(f"### {name if name else 'Your Name'}")
        st.caption(f"{email} | {phone} | {linkedin}")
        
        st.markdown("**Projects:**")
        for p in resume_data['projects']:
            if p.get('title'):
                st.markdown(f"- **{p['title']}**")
                if p.get('link'): st.caption(f"🔗 {p['link']}")
                st.caption(p['description'])

        st.markdown("**Experience:**")
        for job in resume_data['experience']:
            if job.get('role'):
                st.markdown(f"- **{job['role']}** at *{job['company']}* ({job['date']})")
        
        st.markdown(f"**Education:** {education}")
        st.markdown(f"**Skills:** {resume_data['skills']}")

        # Download Button
        st.markdown("---")
        if st.button("Generate PDF Resume", type="primary"):
            if not name:
                st.error("Enter Name first.")
            else:
                with st.spinner('Generating PDF...'):
                    try:
                        pdf_file = generate_pdf_resume(resume_data)
                        with open(pdf_file, "rb") as f:
                            st.download_button("Download PDF", f, file_name=f"{name.replace(' ', '_')}_Resume.pdf", mime="application/pdf")
                    except Exception as e:
                        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
