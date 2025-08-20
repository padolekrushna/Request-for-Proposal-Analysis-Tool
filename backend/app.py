

import streamlit as st
import pandas as pd
import time
import json
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from gemini_client import GeminiClient

from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
from streamlit_lottie import st_lottie
from fpdf import FPDF

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    st.error("Google API key not found. Please set it in your .env file.")
    st.stop()

gemini = GeminiClient()

def load_css(css_file):
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None
def main():
    st.set_page_config(
        page_title="RFP Proposal Analyzer",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("🚀 RFP Proposal Analyzer")
    st.markdown("### Comprehensive AI-Powered Proposal Analysis System")
    
    # Initialize session state for step navigation
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'proposal_text' not in st.session_state:
        st.session_state.proposal_text = None
    if 'new_feature' not in st.session_state:
        st.session_state.new_feature = ""
    if 'gemini_client' not in st.session_state:
        st.session_state.gemini_client = GeminiClient()
    
    # Sidebar for step navigation
    st.sidebar.title("📋 Navigation")
    st.sidebar.markdown(f"**Current Step: {st.session_state.current_step}/2**")
    
    # Progress bar
    progress = st.session_state.current_step / 2
    st.sidebar.progress(progress)
    
    # Step indicators
    if st.session_state.current_step == 1:
        st.sidebar.markdown("🔵 **Step 1: Document Upload** ← Current")
        st.sidebar.markdown("⚪ Step 2: Analysis & Results")
    else:
        st.sidebar.markdown("✅ Step 1: Document Upload")
        st.sidebar.markdown("🔵 **Step 2: Analysis & Results** ← Current")
    
    # Back button (only show in step 2)
    if st.session_state.current_step == 2:
        if st.sidebar.button("⬅️ Back to Step 1", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    
    # Main content based on current step
    if st.session_state.current_step == 1:
        show_step_1()
    elif st.session_state.current_step == 2:
        show_step_2()

def show_step_1():
    """Step 1: Document Upload and Initial Setup"""
    st.header("📤 Step 1: Document Upload & Setup")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Proposal Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF or DOCX file",
            type=['pdf', 'docx'],
            help="Upload the RFP proposal document you want to analyze"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Show file details
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.1f} KB",
                "File type": uploaded_file.type
            }
            st.json(file_details)
            
            # Extract text from uploaded file
            with st.spinner("🔄 Extracting text from document..."):
                try:
                    if uploaded_file.type == "application/pdf":
                        proposal_text = st.session_state.gemini_client.extract_text_from_uploaded_pdf_proposal(uploaded_file)
                    else:  # DOCX
                        proposal_text = st.session_state.gemini_client.extract_text_from_docx_proposal(uploaded_file)
                    
                    if proposal_text:
                        st.session_state.proposal_text = proposal_text
                        st.success("✅ Text extraction completed!")
                        
                        # Show preview of extracted text
                        with st.expander("📋 Preview Extracted Text"):
                            st.markdown(
                                "Extracted Content (Preview)",
                                value=proposal_text[:1000] + "..." if len(proposal_text) > 1000 else proposal_text,
                                height=200,
                                disabled=True
                            )
                    else:
                        st.error("❌ Failed to extract text from the document")
                        
                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")
    
    with col2:
        st.subheader("📊 Upload Statistics")
        if uploaded_file is not None and st.session_state.proposal_text:
            # Calculate some basic statistics
            word_count = len(st.session_state.proposal_text.split())
            char_count = len(st.session_state.proposal_text)
            
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.metric("Words", f"{word_count:,}")
            with metrics_col2:
                st.metric("Characters", f"{char_count:,}")
    
    # Additional Features Section
    st.subheader("🔧 Additional Analysis Features")
    
    new_feature = st.markdown(
        "Specify Additional Components to Analyze",
        value=st.session_state.new_feature,
        placeholder="Enter any specific components or sections you want to analyze (optional)...",
        help="You can specify additional components to check for in the proposal analysis",
        height=100
    )
    
    # Update session state
    st.session_state.new_feature = new_feature
    
    # Proceed to Step 2 Button
    st.markdown("---")
    
    # Check if we can proceed
    can_proceed = st.session_state.proposal_text is not None
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:  # Center the button
        if can_proceed:
            if st.button("🚀 Proceed to Analysis", 
                        type="primary", 
                        use_container_width=True,
                        help="Click to proceed to the analysis step"):
                st.session_state.current_step = 2
                st.success("✅ Moving to Step 2...")
                st.rerun()
        else:
            st.button("🚀 Proceed to Analysis", 
                     type="primary", 
                     use_container_width=True,
                     disabled=True,
                     help="Please upload and process a document first")
    
    # Show requirements if can't proceed
    if not can_proceed:
        st.warning("📋 **Requirements to proceed:**")
        requirements = []
        if not st.session_state.proposal_text:
            requirements.append("❌ Upload and process a proposal document")
        else:
            requirements.append("✅ Document uploaded and processed")
            
        for req in requirements:
            st.markdown(f"- {req}")

def show_step_2():
    """Step 2: Analysis and Results"""
    st.header("📊 Step 2: Analysis & Results")
    
    if not st.session_state.proposal_text:
        st.error("❌ No document data found. Please go back to Step 1 and upload a document.")
        return
    
    # Analysis options
    st.subheader("🔍 Select Analysis Types")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        run_component_analysis = st.checkbox("📋 Component Analysis", value=True)
        run_price_analysis = st.checkbox("💰 Pricing Analysis")
    
    with col2:
        run_cost_realism = st.checkbox("🔍 Cost Realism Analysis")
        run_technical_analysis = st.checkbox("⚙️ Technical Analysis")
    
    with col3:
        run_compliance = st.checkbox("✅ Compliance Assessment")
        generate_summary = st.checkbox("📄 Executive Summary", value=True)
    
    # Run Analysis Button
    if st.button("🎯 Run Selected Analyses", type="primary", use_container_width=True):
        run_analyses(
            run_component_analysis, run_price_analysis, run_cost_realism,
            run_technical_analysis, run_compliance, generate_summary
        )

def run_analyses(run_component_analysis, run_price_analysis, run_cost_realism,
                run_technical_analysis, run_compliance, generate_summary):
    """Execute the selected analyses"""
    
    results = {}
    
    # Component Analysis
    if run_component_analysis:
        with st.spinner("🔄 Running Component Analysis..."):
            try:
                extra_components = st.session_state.new_feature if st.session_state.new_feature.strip() else None
                results['component_analysis'] = st.session_state.gemini_client.analysis_proposal(
                    st.session_state.proposal_text, 
                    extra_components
                )
                st.success("✅ Component Analysis completed!")
            except Exception as e:
                st.error(f"❌ Component Analysis failed: {str(e)}")
    
    # Price Analysis
    if run_price_analysis and 'component_analysis' in results:
        with st.spinner("🔄 Running Pricing Analysis..."):
            try:
                results['price_analysis'] = st.session_state.gemini_client.analyze_pricing(
                    st.session_state.proposal_text,
                    results['component_analysis']
                )
                st.success("✅ Pricing Analysis completed!")
            except Exception as e:
                st.error(f"❌ Pricing Analysis failed: {str(e)}")
    
    # Cost Realism Analysis
    if run_cost_realism and 'component_analysis' in results:
        with st.spinner("🔄 Running Cost Realism Analysis..."):
            try:
                results['cost_realism'] = st.session_state.gemini_client.analyze_cost_realism(
                    st.session_state.proposal_text,
                    results['component_analysis']
                )
                st.success("✅ Cost Realism Analysis completed!")
            except Exception as e:
                st.error(f"❌ Cost Realism Analysis failed: {str(e)}")
    
    # Technical Analysis
    if run_technical_analysis:
        with st.spinner("🔄 Running Technical Analysis..."):
            try:
                results['technical_analysis'] = st.session_state.gemini_client.technical_analysis_review(
                    st.session_state.proposal_text
                )
                st.success("✅ Technical Analysis completed!")
            except Exception as e:
                st.error(f"❌ Technical Analysis failed: {str(e)}")
    
    # Compliance Assessment
    if run_compliance:
        with st.spinner("🔄 Running Compliance Assessment..."):
            try:
                results['compliance_assessment'] = st.session_state.gemini_client.compliance_assessment(
                    st.session_state.proposal_text
                )
                st.success("✅ Compliance Assessment completed!")
            except Exception as e:
                st.error(f"❌ Compliance Assessment failed: {str(e)}")
    
    # Display Results
    display_results(results, generate_summary)

def display_results(results, generate_summary):
    """Display analysis results"""
    
    st.markdown("---")
    st.header("📊 Analysis Results")
    
    # Component Analysis Results
    if 'component_analysis' in results:
        with st.expander("📋 Component Analysis Results", expanded=True):
            st.markdown(results['component_analysis'])
    
    # Price Analysis Results
    if 'price_analysis' in results:
        with st.expander("💰 Pricing Analysis Results"):
            st.markdown(results['price_analysis'])
    
    # Cost Realism Results
    if 'cost_realism' in results:
        with st.expander("🔍 Cost Realism Analysis Results"):
            st.markdown(results['cost_realism'])
    
    # Technical Analysis Results
    if 'technical_analysis' in results:
        with st.expander("⚙️ Technical Analysis Results"):
            st.markdown(results['technical_analysis'])
    
    # Compliance Assessment Results
    if 'compliance_assessment' in results:
        with st.expander("✅ Compliance Assessment Results"):
            st.markdown(results['compliance_assessment'])
    
    # Executive Summary
    if generate_summary and results:
        with st.spinner("🔄 Generating Executive Summary..."):
            try:
                summary = st.session_state.gemini_client.analysis_proposal_summary(
                    st.session_state.proposal_text,
                    results.get('component_analysis', ''),
                    results.get('price_analysis'),
                    results.get('cost_realism'),
                    results.get('technical_analysis'),
                    results.get('compliance_assessment')
                )
                
                with st.expander("📄 Executive Summary", expanded=True):
                    st.markdown(summary)
                    
                    # Download button for summary
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"proposal_analysis_summary_{timestamp}.md"
                    
                    st.download_button(
                        label="📥 Download Summary",
                        data=summary,
                        file_name=filename,
                        mime="text/markdown"
                    )
                    
            except Exception as e:
                st.error(f"❌ Executive Summary generation failed: {str(e)}")
    
    # Download All Results
    if results:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("📥 Download All Results", use_container_width=True):
                download_all_results(results)

def download_all_results(results):
    """Create downloadable file with all results"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"complete_proposal_analysis_{timestamp}.md"
    
    # Combine all results into one document
    combined_results = f"# Complete Proposal Analysis Report\n\n"
    combined_results += f"**Generated on:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}\n\n"
    combined_results += "---\n\n"
    
    for analysis_type, result in results.items():
        title = analysis_type.replace('_', ' ').title()
        combined_results += f"## {title}\n\n{result}\n\n---\n\n"
    
    st.download_button(
        label="📥 Download Complete Report",
        data=combined_results,
        file_name=filename,
        mime="text/markdown",
        use_container_width=True
    )


def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.type
        file_name = uploaded_file.name
        
        with st.status(f"Processing {file_name}...", expanded=True) as status:
            if file_type == "text/plain":
                st.write("📄 Reading text file...")
                content = uploaded_file.getvalue().decode("utf-8")
                status.update(label=f"✅ {file_name} processed successfully!", state="complete")
                return content
                
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                st.write("📄 Converting DOCX to PDF...")
                st.write("🔍 Extracting text using Gemini...")
                content = gemini.extract_text_from_docx(uploaded_file)
                if content:
                    status.update(label=f"✅ {file_name} processed successfully!", state="complete")
                    return content
                else:
                    status.update(label=f"❌ Failed to process {file_name}", state="error")
                    return None
                    
            elif file_type == "application/pdf":
                st.write("📄 Processing PDF file...")
                st.write("🔍 Extracting text using Gemini...")
                content = gemini.extract_text_from_uploaded_pdf(uploaded_file)
                if content:
                    status.update(label=f"✅ {file_name} processed successfully!", state="complete")
                    return content
                else:
                    status.update(label=f"❌ Failed to process {file_name}", state="error")
                    return None
            else:
                st.error(f"Unsupported file type: {file_type}")
                return None
    return None

def process_uploaded_file_Proposal(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.type
        file_name = uploaded_file.name
        
        with st.status(f"Processing {file_name}...", expanded=True) as status:
            if file_type == "text/plain":
                st.write("📄 Reading text file...")
                content = uploaded_file.getvalue().decode("utf-8")
                status.update(label=f"✅ {file_name} processed successfully!", state="complete")
                return content
                
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                st.write("📄 Converting DOCX to PDF...")
                st.write("🔍 Extracting text using Gemini...")
                content = gemini.extract_text_from_docx_proposal(uploaded_file)
                if content:
                    status.update(label=f"✅ {file_name} processed successfully!", state="complete")
                    return content
                else:
                    status.update(label=f"❌ Failed to process {file_name}", state="error")
                    return None
                    
            elif file_type == "application/pdf":
                st.write("📄 Processing PDF file...")
                st.write("🔍 Extracting text using Gemini...")
                content = gemini.extract_text_from_uploaded_pdf_proposal(uploaded_file)
                if content:
                    status.update(label=f"✅ {file_name} processed successfully!", state="complete")
                    return content
                else:
                    status.update(label=f"❌ Failed to process {file_name}", state="error")
                    return None
            else:
                st.error(f"Unsupported file type: {file_type}")
                return None
    return None
 
def generate_pdf_report(content, filename="report.pdf"):
    try:
        from fpdf import FPDF
        import re

        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 15)
                self.cell(0, 10, 'Proposal Analysis Report', 0, 1, 'C')
                self.ln(10)

            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font('Arial', '', 12)

        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                pdf.ln(5)
                continue

            if line.startswith('# '):
                pdf.set_font('Arial', 'B', 16)
                pdf.multi_cell(0, 10, line[2:], 0, 1)
                pdf.ln(5)
                pdf.set_font('Arial', '', 12)
            elif line.startswith('## '):
                pdf.set_font('Arial', 'B', 14)
                pdf.multi_cell(0, 8, line[3:], 0, 1)
                pdf.ln(3)
                pdf.set_font('Arial', '', 12)
            elif line.startswith('### '):
                pdf.set_font('Arial', 'B', 12)
                pdf.multi_cell(0, 6, line[4:], 0, 1)
                pdf.ln(2)
                pdf.set_font('Arial', '', 12)
            else:
                line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
                line = re.sub(r'\*(.*?)\*', r'\1', line)
                line = re.sub(r'`(.*?)`', r'\1', line)

                try:
                    pdf.multi_cell(0, 6, line.encode('latin-1', 'replace').decode('latin-1'), 0, 1)
                except:
                    clean_line = ''.join(char if ord(char) < 128 else '?' for char in line)
                    pdf.multi_cell(0, 6, clean_line, 0, 1)
                pdf.ln(2)

        return pdf.output(dest='S').encode('latin-1')

    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None
    
def analyze_proposal_components(proposal_text, extra_component):
    try:
        with st.spinner("Analyzing proposal with AI"):
            ai_analysis = gemini.analysis_proposal(proposal_text, extra_component)
        
        components = {
            "Executive Summary": "✅",
            "Scope of Work": "✅",
            "Out of Scope": "✅",
            "Prerequisites": "✅",
            "Deliverables": "✅",
            "Timeline": "✅",
            "Technology Stack": "✅",
            "Budget": "✅",
            "Team Structure": "✅",
            "Risk Assessment": "✅",
            "Success Criteria": "✅",
        }
        
        return components, ai_analysis
        
    except Exception as e:
        st.error(f"Error analyzing proposal: {str(e)}")
        return None, None

st.set_page_config(
    page_title="Project Management Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

def next_step():
    st.session_state.step += 1
    st.session_state.processing = False

def reset_process_proposal():
    keys_to_reset = [
        'step',
        'proposal_text',
        'proposal_analysis',
        'ai_analysis_details',
        'proposal_summary',
        'extra_component',
        'current_filename',
        'price_analysis',
        'cost_realism',
        'unbalanced_pricing',
        'technical_analysis',
        'compliance_assessment',
        'processing'
    ]
    
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    
    st.session_state.step = 1
    st.session_state.proposal_text = ""
    st.session_state.proposal_analysis = None
    st.session_state.ai_analysis_details = None
    st.session_state.proposal_summary = None
    st.session_state.extra_component = ""
    st.session_state.current_filename = None
    st.session_state.price_analysis = None
    st.session_state.cost_realism = None
    st.session_state.unbalanced_pricing = None
    st.session_state.technical_analysis = None
    st.session_state.compliance_assessment = None
    st.session_state.processing = False

try:
    load_css("assets/style.css")
except:
    pass

if 'mode' not in st.session_state:
    st.session_state.mode = "with_proposal" 
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'proposal_text' not in st.session_state:
    st.session_state.proposal_text = ""
if 'proposal_analysis' not in st.session_state:
    st.session_state.proposal_analysis = None
if 'ai_analysis_details' not in st.session_state:
    st.session_state.ai_analysis_details = None
if 'proposal_summary' not in st.session_state:
    st.session_state.proposal_summary = None
if 'extra_component' not in st.session_state:
    st.session_state.extra_component = ""
if 'current_filename' not in st.session_state:  
    st.session_state.current_filename = None 
if 'price_analysis' not in st.session_state:
    st.session_state.price_analysis = None
if 'cost_realism' not in st.session_state:
    st.session_state.cost_realism = None
if 'unbalanced_pricing' not in st.session_state:
    st.session_state.unbalanced_pricing = None
if 'technical_analysis' not in st.session_state:
    st.session_state.technical_analysis = None
if 'compliance_assessment' not in st.session_state:
    st.session_state.compliance_assessment = None
if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
if 'proposal_text' not in st.session_state:
        st.session_state.proposal_text = None
if 'new_feature' not in st.session_state:
        st.session_state.new_feature = ""
if 'gemini_client' not in st.session_state:
        st.session_state.gemini_client = GeminiClient()


st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 1rem 0;
    background: linear-gradient(90deg, #1f77b4, #17becf);
    color: white;
    border-radius: 10px;
    margin-bottom: 2rem;
}

.component-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #28a745;
    margin: 0.5rem 0;
}

.component-card.missing {
    border-left-color: #dc3545;
}

.progress-step {
    padding: 0.5rem;
    margin: 0.25rem 0;
    border-radius: 5px;
    background: #f1f3f4;
}

.progress-step.completed {
    background: #d4edda;
    border-left: 3px solid #28a745;
}

.progress-step.current {
    background: #fff3cd;
    border-left: 3px solid #ffc107;
}

.create-proposal-btn {
    position: fixed;
    top: 100px;
    right: 20px;
    z-index: 1000;
}

.analysis-section {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    border: 1px solid #dee2e6;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1> Project Management Tool</h1><p>Intelligent Proposal Analysis & RFP Management</p></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([4, 1, 1])
with col3:
    if st.session_state.mode == "with_proposal":
        if st.button("Create Proposal", key="create_proposal_btn", help="Switch to proposal creation mode"):
            st.session_state.mode = "create_proposal"
            st.session_state.create_proposal_initialized = True
            reset_process_proposal()
            st.rerun()
    else:
        if st.button("Go To Main Page", key="analysis_btn", help="Switch to proposal analysis mode"):
            st.session_state.mode = "with_proposal"
            reset_process_proposal()
            st.rerun()

if st.session_state.mode == "with_proposal":
    with st.sidebar:
        st.image("./images/yashphoto.PNG", width=200)  
        st.title("Proposal Analysis Progress")
        
        analysis_steps = [
            "Flight Check",
            "Price Analysis",  
            "Cost Realism Check",             
            "Technical Analysis Review",      
            "Compliance Assessment",         
            "Generate Summary Report",
        ]
        
        total_steps = len(analysis_steps)
        current_step = 1
        
        if st.session_state.proposal_text and st.session_state.proposal_analysis:
            current_step = 2
        if st.session_state.price_analysis:
            current_step = 3
        if st.session_state.cost_realism:
            current_step = 4
        if st.session_state.technical_analysis:
            current_step = 5
        if st.session_state.compliance_assessment:
            current_step = 6
        if st.session_state.proposal_summary:
            current_step = 7

        completion = int((current_step - 1) / total_steps * 100)
        st.progress(completion / 100)
        st.write(f"**{completion}%** completed")
        
        add_vertical_space(1)
        
        for i, step_name in enumerate(analysis_steps, 1):
            status_class = "completed" if i < current_step else "current" if i == current_step else ""
            icon = "✅" if i < current_step else "🔄" if i == current_step else "⏳"
            
            st.markdown(f'<div class="progress-step {status_class}"><strong>{icon} Step {i}: {step_name}</strong></div>', unsafe_allow_html=True)
        
        add_vertical_space(2)
        
        if st.button("🔄 Reset Analysis", use_container_width=True):
            reset_process_proposal()
            st.rerun()
        
        with st.expander("ℹ️ Help & Tips"):
            st.write("""
            **Enhanced AI Analysis Features:**
            - 🤖 AI-powered component detection
            - ✅ 15+ component completeness check
            - 📊 Quality assessment scoring
            - 🎯 Compliance verification
            - 💡 Detailed improvement recommendations
            - 📋 Executive summary generation
            
            **Supported Formats:**
            - PDF documents
            - Word documents (.docx)
            - Text files (.txt)
            """)

    colored_header(
        label="AI-Powered Proposal Analysis Dashboard",
        description="Upload and analyze your proposal document with advanced AI analysis",
        color_name="blue-green-70"
    )
    
    if st.session_state.step == 1:
        with st.container():
            st.subheader("Step 1: Flight Check")
            st.write("Upload your proposal document and get instant AI-powered component analysis")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                uploaded_file = st.file_uploader(
                    "Choose a file",
                    type=["pdf", "docx", "txt"],
                    accept_multiple_files=False,
                    key="file_uploader_step1"
                )
            
                if uploaded_file is not None:
                    st.session_state.current_filename = uploaded_file.name
                    with st.spinner("Processing and analyzing document..."):
                        extracted_text = process_uploaded_file_Proposal(uploaded_file)
                        if extracted_text:  
                            st.session_state.proposal_text = extracted_text
                            components, ai_details = analyze_proposal_components(
                                st.session_state.proposal_text, 
                                st.session_state.extra_component
                            )
                            st.session_state.proposal_analysis = components
                            st.session_state.ai_analysis_details = ai_details
            
            with col2:
                st.subheader("Additional Features")
                extra_component = st.text_area(
    "Additional components to analyze:",
    placeholder="Enter any additional features you want to analyze",
    height=100
)
                
                if extra_component:
                    st.session_state.extra_component = extra_component
            
            if st.session_state.current_filename:
                st.info(f"📄 Document: **{st.session_state.current_filename}** | Length: **{len(st.session_state.proposal_text):,} characters**")
            
            if st.session_state.proposal_analysis:
                st.success("✅ Document processed and analyzed successfully!")
                
                st.markdown("### 📋 Proposal Component Analysis")
                components = st.session_state.proposal_analysis
                component_list = list(components.items())
                
                for i in range(0, len(component_list), 2):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if i < len(component_list):
                            component_name, present = component_list[i]
                            card_class = "component-card" 
                            st.markdown(f'<div class="{card_class}"><strong>{present} {component_name}</strong></div>', 
                                        unsafe_allow_html=True)
                    
                    with col2:
                        if i + 1 < len(component_list):
                            component_name, present = component_list[i + 1]
                            st.markdown(f'<div class="{card_class}"><strong>{present} {component_name}</strong></div>', 
                                        unsafe_allow_html=True)
                
                if st.session_state.ai_analysis_details:
                    with st.expander("🔍 View Detailed Component Analysis"):
                        st.markdown(st.session_state.ai_analysis_details)
                
                if st.button("Proceed to Price Analysis ➡️", type="primary", use_container_width=True):
                    st.session_state.step = 2
                    st.rerun()
            
            elif st.session_state.proposal_text:
                if st.button("🔍 Analyze Proposal Components", type="primary", use_container_width=True):
                    with st.spinner("Analyzing proposal components..."):
                        components, ai_details = analyze_proposal_components(
                            st.session_state.proposal_text, 
                            st.session_state.extra_component
                        )
                        st.session_state.proposal_analysis = components
                        st.session_state.ai_analysis_details = ai_details
                        st.rerun()

    elif st.session_state.step == 2:
        with st.container():
            st.subheader("Step 2: Price Analysis")
            st.write("Analyzing pricing fairness using federal acquisition standards...")
            
            if not st.session_state.price_analysis:
                with st.spinner("Performing price analysis per FAR 15.404-1(b)"):
                    st.session_state.price_analysis = gemini.analyze_pricing(st.session_state.proposal_text, st.session_state.ai_analysis_details)
            
            if st.session_state.price_analysis:
                with st.expander("💰 Price Analysis Results", expanded=True):
                    st.markdown(st.session_state.price_analysis)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("⬅️ Back to Component Analysis"):
                        st.session_state.step = 1
                        st.rerun()
                with col2:
                    if st.button("Proceed to Cost Realism ➡️"):
                        st.session_state.step = 3
                        st.rerun()

    elif st.session_state.step == 3:
        with st.container():
            st.subheader("Step 3: Cost Realism Analysis")
            st.write("Evaluating if proposed costs are realistic for the work scope...")
            
            if not st.session_state.cost_realism:
                with st.spinner("Analyzing cost realism per FAR 15.404-1(d)"):
                    st.session_state.cost_realism = gemini.analyze_cost_realism(
                        st.session_state.proposal_text, 
                        st.session_state.ai_analysis_details
                    )
            
            if st.session_state.cost_realism:
                with st.expander("💰 Cost Realism Analysis", expanded=True):
                    st.markdown(st.session_state.cost_realism)
                    
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("⬅️ Back to Price Analysis"):
                        st.session_state.step = 2
                        st.rerun()
                with col2:
                    if st.button("Proceed to Technical Analysis ➡️"):
                        st.session_state.step = 4
                        st.rerun()

    elif st.session_state.step == 4:
        with st.container():
            st.subheader("Step 4: Technical Analysis Review")
            st.write("Reviewing technical aspects and feasibility...")
            
            if not st.session_state.technical_analysis:
                with st.spinner("Performing technical analysis review..."):
                    st.session_state.technical_analysis = gemini.technical_analysis_review(st.session_state.proposal_text)
            
            if st.session_state.technical_analysis:
                with st.expander("🔧 Technical Analysis", expanded=True):
                    st.markdown(st.session_state.technical_analysis)
                    
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("⬅️ Back to Cost Realism"):
                        st.session_state.step = 3
                        st.rerun()
                with col2:
                    if st.button("Proceed to Compliance Assessment ➡️"):
                        st.session_state.step = 5
                        st.rerun()

    elif st.session_state.step == 5:
        with st.container():
            st.subheader("Step 5: Compliance Assessment")
            st.write("Assessing compliance with requirements and regulations...")
            
            if not st.session_state.compliance_assessment:
                with st.spinner("Performing compliance assessment..."):
                    st.session_state.compliance_assessment = gemini.compliance_assessment(st.session_state.proposal_text)
            
            if st.session_state.compliance_assessment:
                with st.expander("⚖️ Compliance Assessment", expanded=True):
                    st.markdown(st.session_state.compliance_assessment)
                    
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("⬅️ Back to Technical Analysis"):
                        st.session_state.step = 4
                        st.rerun()
                with col2:
                    if st.button("Generate Summary Report ➡️"):
                        st.session_state.step = 6
                        st.rerun()

    elif st.session_state.step == 6:
        with st.container():
            st.subheader("Step 6: Executive Summary Report")
            if not st.session_state.proposal_summary:
                with st.spinner("Generating comprehensive summary report..."):
                    summary = gemini.analysis_proposal_summary(
                        st.session_state.proposal_text, 
                        st.session_state.ai_analysis_details,
                        st.session_state.price_analysis,
                        st.session_state.cost_realism,
                        st.session_state.technical_analysis,
                        st.session_state.compliance_assessment
                    )
                    st.session_state.proposal_summary = summary
            
            if st.session_state.proposal_summary:
                st.success("✅ Summary report generated successfully!")
                st.markdown('<div class="analysis-content">', unsafe_allow_html=True)
                st.markdown(st.session_state.proposal_summary)
                st.markdown('</div>', unsafe_allow_html=True)
                
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download Summary Report (MD)",
                    data=st.session_state.proposal_summary,
                    file_name=f"proposal_summary_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
            with col2:
                pdf_data = generate_pdf_report(
                    st.session_state.proposal_summary, 
                    f"proposal_summary_{datetime.now().strftime('%Y%m%d')}.pdf"
                )
                if pdf_data:
                    st.download_button(
                        label="📥 Download Summary Report (PDF)",
                        data=pdf_data,
                        file_name=f"proposal_summary_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.warning("PDF generation failed")

elif st.session_state.mode == "create_proposal":
    
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'rfp_text' not in st.session_state:
        st.session_state.rfp_text = ""
    if 'company_profile' not in st.session_state:
        try:
            with open('D:/rfp_analysis_tool/company_profile.txt', 'r') as file:
                st.session_state.company_profile = file.read()
        except:
            st.session_state.company_profile = ""
    if 'rfp_breakdown' not in st.session_state:
        st.session_state.rfp_breakdown = None
    if 'eligibility_analysis' not in st.session_state:
        st.session_state.eligibility_analysis = None
    if 'requirements' not in st.session_state:
        st.session_state.requirements = None
    if 'tasks' not in st.session_state:
        st.session_state.tasks = None
    if 'proposal' not in st.session_state:
        st.session_state.proposal = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'current_filename' not in st.session_state:
        st.session_state.current_filename = None

    def next_step():
        st.session_state.step += 1
        st.session_state.processing = False

    def reset_process():
        company_profile_backup = st.session_state.company_profile
        for key in list(st.session_state.keys()):
            if key != 'company_profile':
                del st.session_state[key]
        st.session_state.step = 1
        st.session_state.company_profile = company_profile_backup
        st.session_state.processing = False

    with st.sidebar:
        st.title("Project Management Tool")
        
        colored_header(
            label="Progress Tracker",
            description="Follow your proposal generation progress",
            color_name="green-70"
        )
        
        total_steps = 9
        
        completion = int((st.session_state.step - 1) / total_steps * 100)
        st.progress(completion / 100)
        st.write(f"**{completion}%** completed")
        add_vertical_space(1)
        
        for i, step_name in enumerate([
            "Input RFP",
            "RFP Breakdown", 
            "Eligibility Analysis",
            "Requirements Extraction",
            "Task Generation",
            "Competitive Analysis",
            "Innovation Assessment",
            "Executive Briefing",
            "Proposal Generation"
        ], 1):
            if i < st.session_state.step:
                step_status = "✅ "
            elif i == st.session_state.step:
                step_status = "🔄 "
            else:
                step_status = "⏳ "
            
            with stylable_container(
                key=f"step_{i}",
                css_styles="""
                    {
                        background-color: #f0f2f6;
                        border-radius: 10px;
                        padding: 10px;
                        margin-bottom: 10px;
                    }
                    """
            ):
                st.write(f"**{step_status} Step {i}: {step_name}**")
        
        add_vertical_space(2)
        
        if st.button("🔄 Start Over", use_container_width=True):
            reset_process()
            st.rerun()
        
        with st.expander("ℹ️ Help"):
            st.write("""
            **How to use this tool:**
            1. Upload or paste your RFP text
            2. Review the automatic analysis results
            3. Follow the process through eligibility check
            4. Examine requirements and tasks
            5. Generate and download your full proposal
            
            **Supported file formats:**
            - Text files (.txt)
            - PDF files (.pdf)
            - Word documents (.docx)
            
            All steps are processed automatically once you provide the RFP text.
            """)
        
        add_vertical_space(2)
        st.caption("© 2025 DataNova Solutions | Powered by Gemini API")

    if st.session_state.step == 1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            colored_header(
                label="Input RFP Document",
                description="Provide the Request for Proposal text to analyze",
                color_name="blue-green-70"
            )
            
            input_method = st.radio(
                "Choose input method:",
                ["Upload RFP File", "Paste RFP Text"],
                horizontal=True
            )

            if input_method == "Upload RFP File":
                uploaded_file = st.file_uploader(
                    "Upload RFP document",
                    type=["txt", "pdf", "docx"],
                    help="Supports text files (.txt), PDF files (.pdf), and Word documents (.docx)"
                )
                
                if uploaded_file is not None:
                    st.session_state.current_filename = uploaded_file.name
                    
                    extracted_text = process_uploaded_file(uploaded_file)
                    
                    if extracted_text:
                        st.session_state.rfp_text = extracted_text
                        st.success(f"✅ File '{uploaded_file.name}' processed successfully!")
                        
                        with st.expander("📄 Preview extracted text", expanded=False):
                            st.markdown(
                                "Extracted content:",
                                value=extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text,
                                height=200,
                                disabled=True
                            )
                    else:
                        st.error("❌ Failed to extract text from the uploaded file. Please try a different file or paste the content manually.")
                        
            else:
                sample_placeholder = """Paste your RFP text here, or use our sample by clicking 'Load Sample RFP'"""
                
                rfp_text_input = st.markdown(
                    "RFP Content:",
                    height=400,
                    placeholder=sample_placeholder,
                    value=st.session_state.rfp_text
                )
                
                if rfp_text_input:
                    st.session_state.rfp_text = rfp_text_input
                
                col1a, col1b = st.columns([1, 1])
                with col1a:
                    if st.button("📄 Load Sample RFP", use_container_width=True):
                        try:
                            with open('D:/rfp_analysis_tool/sample_rfp.txt', 'r') as file:
                                st.session_state.rfp_text = file.read()
                                st.session_state.current_filename = "sample_rfp.txt"
                                st.rerun()
                        except Exception as e:
                            st.error(f"Could not load sample RFP: {e}")
        
        with col2:
            st.subheader("Company Profile")
            st.info("This profile will be used to analyze if your company meets the RFP requirements.")
            
            company_profile = st.text_area(
                       "Company profile:",
                       height=400,
                       value=st.session_state.company_profile
                       )
            
            if company_profile:
                st.session_state.company_profile = company_profile
        
        if st.session_state.rfp_text and st.session_state.company_profile:
            st.success("✅ All information provided! Click below to start the analysis process.")
            
            if st.session_state.current_filename:
                st.info(f"📄 Document: **{st.session_state.current_filename}** | Length: **{len(st.session_state.rfp_text):,} characters**")
            
            if st.button("▶️ Start Analysis Process", type="primary", use_container_width=True):
                st.session_state.processing = True
                st.session_state.step = 2
                st.rerun()
        else:
            st.warning("Please provide both RFP text and company profile to proceed.")

    elif st.session_state.step == 2:
        colored_header(
            label="RFP Breakdown Analysis",
            description="Comprehensive analysis of the RFP document",
            color_name="blue-green-70"
        )
        
        if st.session_state.current_filename:
            st.info(f"Analyzing RFP document: **{st.session_state.current_filename}**", icon="📄")
        
        if not st.session_state.rfp_breakdown:
            with st.status("Analyzing RFP...", expanded=True) as status:
                st.write("Extracting key information from the RFP...")
                st.session_state.rfp_breakdown = gemini.analyze_rfp(st.session_state.rfp_text)
                time.sleep(1)
                st.write("Analysis complete! ✅")
                status.update(label="Analysis completed!", state="complete", expanded=False)
        
        with st.expander("RFP Breakdown Analysis", expanded=True):
            st.markdown('<div class="markdown-content">', unsafe_allow_html=True)
            st.markdown(st.session_state.rfp_breakdown)
            st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(
                    label="📥 Download RFP Breakdown",
                    data=st.session_state.rfp_breakdown,
                    file_name="rfp_breakdown.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        
        st.success("RFP breakdown completed successfully!")
        if st.button("Proceed to eligibility analysis"):
            next_step()
            st.rerun()

    elif st.session_state.step == 3:
        colored_header(
            label="Eligibility Analysis",
            description="Determining if your company meets the RFP requirements",
            color_name="blue-green-70"
        )
        
        if not st.session_state.eligibility_analysis:
            with st.status("Analyzing eligibility...", expanded=True) as status:
                st.write("Extracting requirements from the RFP...")
                time.sleep(1)
                st.write("Comparing against company capabilities...")
                st.session_state.eligibility_analysis = gemini.analyze_eligibility(
                    st.session_state.rfp_text, st.session_state.company_profile
                )
                time.sleep(1)
                st.write("Analysis complete! ✅")
                status.update(label="Eligibility analysis completed!", state="complete", expanded=False)
        
        with st.expander("Eligibility Analysis Results", expanded=True):
            st.markdown('<div class="markdown-content">', unsafe_allow_html=True)
            st.markdown(st.session_state.eligibility_analysis)
            st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(
                    label="📥 Download Eligibility Analysis",
                    data=st.session_state.eligibility_analysis,
                    file_name="eligibility_analysis.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        
        st.write("### Decision Point")
        st.write("Based on the eligibility analysis, would you like to proceed with the proposal?")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✅ Yes, proceed with analysis", type="primary", use_container_width=True):
                next_step()
                st.rerun()
        with col2:
            if st.button("❌ No, start over with a different RFP", use_container_width=True):
                reset_process()
                st.rerun()

    elif st.session_state.step == 4:
        colored_header(
            label="Requirements Extraction",
            description="Identifying and categorizing all requirements in the RFP",
            color_name="blue-green-70"
        )
        
        if not st.session_state.requirements:
            with st.status("Extracting requirements...", expanded=True) as status:
                st.write("Analyzing RFP for specific requirements...")
                time.sleep(1)
                st.write("Categorizing and prioritizing requirements...")
                st.session_state.requirements = gemini.extract_requirements(st.session_state.rfp_text)
                time.sleep(1)
                st.write("Extraction complete! ✅")
                status.update(label="Requirements extraction completed!", state="complete", expanded=False)
        
        with st.expander("Extracted Requirements", expanded=True):
            st.markdown('<div class="markdown-content">', unsafe_allow_html=True)
            st.markdown(st.session_state.requirements)
            st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(
                    label="📥 Download Requirements",
                    data=st.session_state.requirements,
                    file_name="rfp_requirements.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        
        st.success("Requirements extraction completed successfully!")
        if st.button("Proceed to task generation"):
            next_step()
            st.rerun()

    elif st.session_state.step == 5:
        colored_header(
            label="Task Generation",
            description="Creating actionable Jira-style tasks based on the requirements",
            color_name="blue-green-70"
        )
        
        if not st.session_state.tasks:
            with st.status("Generating tasks...", expanded=True) as status:
                st.write("Converting requirements to actionable tasks...")
                time.sleep(1)
                st.write("Estimating effort and assigning task types...")
                st.session_state.tasks = gemini.generate_tasks(st.session_state.requirements)
                time.sleep(1)
                st.write("Task generation complete! ✅")
                status.update(label="Task generation completed!", state="complete", expanded=False)
        
        with st.expander("Generated Tasks", expanded=True):
            st.markdown('<div class="markdown-content">', unsafe_allow_html=True)
            st.markdown(st.session_state.tasks)
            st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(
                    label="📥 Download Tasks",
                    data=st.session_state.tasks,
                    file_name="rfp_tasks.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        
        st.success("Task generation completed successfully!")
        if st.button("Proceed to competitive analysis"):
            next_step()
            st.rerun()

    elif st.session_state.step == 6:
        colored_header(
            label="Competitive Analysis",
            description="Analyzing competitive landscape and positioning strategy",
            color_name="blue-green-70"
        )
        
        if 'competitive_analysis' not in st.session_state:
            st.session_state.competitive_analysis = None
        
        if not st.session_state.competitive_analysis:
            with st.status("Analyzing competitive landscape...", expanded=True) as status:
                st.write("Identifying likely competitors...")
                st.write("Analyzing competitive advantages...")
                st.session_state.competitive_analysis = gemini.analyze_competitive_landscape(
                    st.session_state.rfp_text, st.session_state.company_profile
                )
                status.update(label="Competitive analysis completed!", state="complete", expanded=False)
        
        with st.expander("Competitive Analysis Results", expanded=True):
            st.markdown(st.session_state.competitive_analysis)
            st.download_button(
                label="📥 Download Competitive Analysis",
                data=st.session_state.competitive_analysis,
                file_name="competitive_analysis.md",
                mime="text/markdown"
            )
        
        if st.button("Proceed to innovation assessment"):
            next_step()
            st.rerun()

    elif st.session_state.step == 7:
        colored_header(
            label="Innovation Assessment",
            description="Identifying opportunities for emerging technology integration",
            color_name="blue-green-70"
        )
        
        if 'innovation_assessment' not in st.session_state:
            st.session_state.innovation_assessment = None
        
        if not st.session_state.innovation_assessment:
            with st.status("Assessing innovation opportunities...", expanded=True) as status:
                st.write("Analyzing AI/ML integration potential...")
                st.write("Identifying automation opportunities...")
                st.session_state.innovation_assessment = gemini.assess_innovation_opportunities(
                    st.session_state.rfp_text
                )
                status.update(label="Innovation assessment completed!", state="complete", expanded=False)
        
        with st.expander("Innovation Assessment Results", expanded=True):
            st.markdown(st.session_state.innovation_assessment)
            st.download_button(
                label="📥 Download Innovation Assessment",
                data=st.session_state.innovation_assessment,
                file_name="innovation_assessment.md",
                mime="text/markdown"
            )
        
        if st.button("Proceed to executive briefing"):
            next_step()
            st.rerun()

    elif st.session_state.step == 8:
        colored_header(
            label="Executive Briefing",
            description="C-suite level summary and decision recommendation",
            color_name="blue-green-70"
        )
        
        if 'executive_briefing' not in st.session_state:
            st.session_state.executive_briefing = None
        
        if not st.session_state.executive_briefing:
            with st.status("Generating executive briefing...", expanded=True) as status:
                st.write("Creating C-level summary...")
                st.write("Developing decision recommendations...")
                st.session_state.executive_briefing = gemini.generate_executive_briefing(
                    st.session_state.rfp_text, st.session_state.company_profile
                )
                status.update(label="Executive briefing completed!", state="complete", expanded=False)
        
        with st.expander("Executive Briefing", expanded=True):
            st.markdown(st.session_state.executive_briefing)
            st.download_button(
                label="📥 Download Executive Briefing",
                data=st.session_state.executive_briefing,
                file_name="executive_briefing.md",
                mime="text/markdown"
            )
        
        if st.button("Proceed to final proposal generation"):
            next_step()
            st.rerun()

    elif st.session_state.step == 9:
        colored_header(
            label="Project Proposal Generation",
            description="Creating a comprehensive project proposal based on the RFP",
            color_name="blue-green-70"
        )
        
        if not st.session_state.proposal:
            with st.status("Generating proposal...", expanded=True) as status:
                st.write("Analyzing all previous insights...")
                time.sleep(1)
                st.write("Crafting a comprehensive project proposal...")
                st.session_state.proposal = gemini.generate_project_proposal(st.session_state.rfp_text,st.session_state.company_profile)
                time.sleep(1)
                st.write("Proposal generation complete! ✅")
                status.update(label="Proposal generation completed!", state="complete", expanded=False)
        
        with st.expander("Complete Project Proposal", expanded=True):
            st.markdown('<div class="markdown-content">', unsafe_allow_html=True)
            st.markdown(st.session_state.proposal)
            st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(
                    label="📥 Download Complete Proposal",
                    data=st.session_state.proposal,
                    file_name="rfp_proposal.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        
        st.success("🎉 Proposal generation process completed successfully!")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("💾 Download All Files as ZIP", use_container_width=True):
                st.info("This feature would create a ZIP file with all generated files.")
                
        with col2:
            if st.button("🔄 Generate New Proposal", use_container_width=True):
                st.session_state.proposal = None
                st.rerun()
                
        with col3:
            if st.button("📄 Start New RFP Analysis", use_container_width=True):
                reset_process()
                st.rerun()

style_metric_cards()













