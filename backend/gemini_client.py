

import os
import tempfile
import google.generativeai as genai
from dotenv import load_dotenv
from docx2pdf import convert
from pathlib import Path
import streamlit as st
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class GeminiClient:
    def __init__(self, model_name="gemini-2.0-flash"):
        """Initialize the Gemini client with the specified model"""
        self.model = genai.GenerativeModel(model_name)
        self.vision_model = genai.GenerativeModel('gemini-2.0-flash')
    
    # def extract_text_from_docx(self, docx_file):
    #     """
    #     Convert DOCX to PDF and then extract text using Gemini
    #     """
    #     try:
    #         # Create temporary directory for file processing
    #         with tempfile.TemporaryDirectory() as temp_dir:
    #             # Save uploaded DOCX file temporarily
    #             docx_path = os.path.join(temp_dir, "document.docx")
    #             with open(docx_path, "wb") as f:
    #                 f.write(docx_file.getvalue())
                
    #             # Convert DOCX to PDF
    #             pdf_path = os.path.join(temp_dir, "document.pdf")
    #             convert(docx_path, pdf_path)
                
    #             # Extract text from PDF using Gemini
    #             return self.extract_text_from_pdf_file(pdf_path)
                
    #     except Exception as e:
    #         raise Exception(f"Error processing DOCX file: {str(e)}")
    #         return None
    
    # def extract_text_from_pdf_file(self, pdf_path):
    #     """
    #     Extract text from PDF file using Gemini's multimodal capabilities
    #     """
    #     try:
    #         # Upload file to Gemini
    #         with open(pdf_path, 'rb') as f:
    #            pdf_bytes = f.read()
            
    #         # Extract text using Gemini
    #         prompt = """
    #         Please extract all text content from this PDF document. 
    #         Return only the extracted text without any additional formatting or commentary.
    #         Preserve the structure and organization of the content as much as possible.
    #         """
            
    #         # Create the image part from PDF bytes (first page)
    #         # Note: For multi-page PDFs, you may need to split it first
    #         response = self.model.generate_content([
    #            prompt,
    #            {'mime_type': 'application/pdf', 'data': pdf_bytes}
    #         ])
            
    #         # Process and return the extraction result
    #         return response.text
            
    #     except Exception as e:
    #         raise Exception(f"Error extracting text from PDF: {str(e)}")
    #         return None
    
    # def extract_text_from_uploaded_pdf(self, pdf_file):
    #     """
    #     Extract text from uploaded PDF file using Gemini
    #     """
    #     try:
    #         # Create temporary file for PDF processing
    #         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
    #             temp_file.write(pdf_file.getvalue())
    #             temp_file_path = temp_file.name
            
    #         try:
    #             # Extract text using Gemini
    #             text = self.extract_text_from_pdf_file(temp_file_path)
    #             return text
    #         finally:
    #             # Clean up temporary file
    #             os.unlink(temp_file_path)
                
    #     except Exception as e:
    #         raise Exception(f"Error processing uploaded PDF: {str(e)}")
    #         return None
    
    # async def extract_text_from_docx(self, docx_file):
    #     """
    #     Convert DOCX to PDF and then extract text using Gemini
    #     """
    #     try:
    #         # Create temporary directory for file processing
    #         with tempfile.TemporaryDirectory() as temp_dir:
    #             # Save uploaded DOCX file temporarily
    #             docx_path = os.path.join(temp_dir, "document.docx")
    #             docx_content = await docx_file.read()
    #             with open(docx_path, "wb") as f:
    #                 f.write(docx_content)
    #             await docx_file.seek(0)  # Reset file pointer
                
    #             # Convert DOCX to PDF
    #             pdf_path = os.path.join(temp_dir, "document.pdf")
    #             convert(docx_path, pdf_path)
                
    #             # Extract text from PDF using Gemini
    #             return await self.extract_text_from_pdf_file(pdf_path)
                
    #     except Exception as e:
    #         raise Exception(f"Error processing DOCX file: {str(e)}")

    # async def extract_text_from_pdf_file(self, pdf_path):
    #     """
    #     Extract text from PDF file using Gemini's multimodal capabilities
    #     """
    #     try:
    #         # Upload file to Gemini
    #         with open(pdf_path, 'rb') as f:
    #             pdf_bytes = f.read()
            
    #         # Extract text using Gemini
    #         prompt = """
    #         Please extract all text content from this PDF document. 
    #         Return only the extracted text without any additional formatting or commentary.
    #         Preserve the structure and organization of the content as much as possible.
    #         """
            
    #         response = await self.model.generate_content([
    #             prompt,
    #             {'mime_type': 'application/pdf', 'data': pdf_bytes}
    #         ])
            
    #         return response.text
            
    #     except Exception as e:
    #         raise Exception(f"Error extracting text from PDF: {str(e)}")

    # async def extract_text_from_uploaded_pdf(self, pdf_file):
    #     """
    #     Extract text from uploaded PDF file using Gemini
    #     """
    #     try:
    #         # Create temporary file for PDF processing
    #         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
    #             pdf_content = await pdf_file.read()
    #             temp_file.write(pdf_content)
    #             temp_file_path = temp_file.name
    #             await pdf_file.seek(0)  # Reset file pointer
            
    #         try:
    #             # Extract text using Gemini
    #             text = await self.extract_text_from_pdf_file(temp_file_path)
    #             return text
    #         finally:
    #             # Clean up temporary file
    #             os.unlink(temp_file_path)
                
    #     except Exception as e:
    #         raise Exception(f"Error processing uploaded PDF: {str(e)}")
    
    async def extract_text_from_docx(self, docx_file):
        """
        Convert DOCX to PDF and then extract text using Gemini
        """
        try:
            # Create temporary directory for file processing
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save uploaded DOCX file temporarily
                docx_path = os.path.join(temp_dir, "document.docx")
                docx_content = await docx_file.read()
                with open(docx_path, "wb") as f:
                    f.write(docx_content)
                await docx_file.seek(0)  # Reset file pointer
                
                # Convert DOCX to PDF
                pdf_path = os.path.join(temp_dir, "document.pdf")
                convert(docx_path, pdf_path)
                
                # Extract text from PDF using Gemini
                return await self.extract_text_from_pdf_file(pdf_path)
                
        except Exception as e:
            raise Exception(f"Error processing DOCX file: {str(e)}")

    async def extract_text_from_pdf_file(self, pdf_path):
        """
        Extract text from PDF file using Gemini's multimodal capabilities
        """
        try:
            # Upload file to Gemini
            with open(pdf_path, 'rb') as f:
                pdf_bytes = f.read()
            
            # Extract text using Gemini
            prompt = """
            Please extract all text content from this PDF document.
            Return only the extracted text without any additional formatting or commentary.
            Preserve the structure and organization of the content as much as possible.
            """
            
            # Remove await here - generate_content is synchronous
            response = self.model.generate_content([
                prompt,
                {'mime_type': 'application/pdf', 'data': pdf_bytes}
            ])
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    async def extract_text_from_uploaded_pdf(self, pdf_file):
        """
        Extract text from uploaded PDF file using Gemini
        """
        try:
            # Create temporary file for PDF processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                pdf_content = await pdf_file.read()
                temp_file.write(pdf_content)
                temp_file_path = temp_file.name
                await pdf_file.seek(0)  # Reset file pointer
            
            try:
                # Extract text using Gemini
                text = await self.extract_text_from_pdf_file(temp_file_path)
                return text
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            raise Exception(f"Error processing uploaded PDF: {str(e)}")
      
    async def analyze_eligibility(self, rfp_text, company_profile):
        """
        Analyze if the company meets the eligibility requirements in the RFP
        """
        prompt = f"""
        You are an experienced bid manager specializing in evaluating RFP eligibility. 
        Based on the following RFP document and company profile, analyze whether the company meets the basic eligibility requirements to respond to this RFP.
        
        RFP Text:
        {rfp_text}
        
        Company Profile:
        {company_profile}
        
        Provide a comprehensive eligibility analysis with the following sections:
        
        1. **Summary of Eligibility**:
           - Overall assessment of eligibility (Fully Eligible, Partially Eligible, Not Eligible)
           - Executive summary of key findings
        
        2. **Mandatory Requirements Analysis**:
           - Table listing all mandatory requirements from the RFP
           - For each requirement, indicate whether the company meets it (Met, Partially Met, Not Met)
           - Provide justification for each assessment based on the company profile
        
        3. **Gap Analysis**:
           - Identify any significant gaps between RFP requirements and company capabilities
           - Suggest possible ways to address these gaps (partnerships, new hires, etc.)
        
        4. **Competitive Position**:
           - Assess how well the company is positioned compared to likely competitors
           - Identify any unique advantages or disadvantages
        
        5. **Recommendation**:
           - Clear recommendation on whether to proceed with a proposal
           - If proceeding, note any special considerations that should be addressed in the proposal
        
        Format your response in markdown, with clear headings, tables, and bullet points.
        Use factual, objective language based strictly on the information provided.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
        
    async def generate_project_proposal(self, rfp_text, company_profile):
        """
        Generate a comprehensive project proposal addressing semantic gaps in typical proposals
        """
        prompt = f"""
        You are an expert proposal writer specializing in strategic business transformation proposals. 
        Create a comprehensive, executive-ready project proposal that goes beyond basic technical delivery 
        to demonstrate strategic business value and competitive differentiation.

        RFP Text:
        {rfp_text}

        Company Profile:
        {company_profile}

        Create a proposal with the following enhanced sections:

        1. **EXECUTIVE SUMMARY & STRATEGIC ALIGNMENT**:
        - Quantifiable business impact and ROI projections with timelines
        - Strategic alignment with client's long-term business objectives
        - Competitive advantage creation and market positioning benefits
        - Executive-level value propositions that resonate with C-suite decision makers

        2. **COMPANY PROFILE & COMPETITIVE DIFFERENTIATION**:
        - Unique market position and proprietary methodologies
        - Industry-specific expertise and relevant case studies with measurable outcomes
        - Innovation track record and emerging technology adoption
        - Partnership ecosystem and vendor relationships

        3. **BUSINESS TRANSFORMATION VISION**:
        - Comprehensive understanding of client's industry challenges and market forces
        - Digital transformation roadmap beyond immediate project scope
        - Change management strategy addressing cultural and organizational transformation
        - Future-state business capabilities and competitive positioning

        4. **SOLUTION ARCHITECTURE & INNOVATION**:
        - Modern, scalable architecture with cloud-native approaches
        - AI/ML integration opportunities and data-driven insights
        - API-first design and microservices architecture where applicable
        - Security-by-design and compliance framework
        - Emerging technology integration roadmap (IoT, blockchain, etc.)

        5. **IMPLEMENTATION METHODOLOGY & RISK MITIGATION**:
        - Agile/DevOps delivery methodology with continuous value delivery
        - Comprehensive risk assessment with quantified impact analysis
        - Scenario planning and contingency strategies
        - Quality assurance framework and success metrics
        - Stakeholder engagement and communication strategy

        6. **TEAM STRUCTURE & CAPABILITY BUILDING**:
        - Senior leadership involvement and escalation procedures
        - Knowledge transfer and capability building programs
        - Center of Excellence establishment
        - Long-term skill development and certification roadmaps

        7. **FINANCIAL MODEL & VALUE REALIZATION**:
        - Detailed cost-benefit analysis with NPV calculations
        - Phased investment approach with quick wins identification
        - Total Economic Impact (TEI) analysis
        - Cost optimization strategies and efficiency gains
        - Flexible pricing models and payment structures

        8. **RISK MANAGEMENT & BUSINESS CONTINUITY**:
        - Enterprise risk assessment matrix with probability and impact scores
        - Business continuity planning and disaster recovery strategies
        - Vendor risk management and third-party dependencies
        - Compliance and regulatory risk mitigation
        - Change management risk assessment

        9. **INNOVATION & FUTURE ROADMAP**:
        - Technology evolution strategy and platform extensibility
        - Industry 4.0 readiness and digital maturity advancement
        - Sustainability and ESG considerations
        - Competitive intelligence and market trend analysis
        - Long-term partnership and growth opportunities

        10. **SUCCESS METRICS & GOVERNANCE**:
            - KPI framework with baseline establishment methodology
            - Business value measurement and tracking systems
            - Governance structure with executive oversight
            - Continuous improvement processes and feedback loops
            - Performance dashboards and reporting mechanisms

        11. **CLIENT SUCCESS ENABLEMENT**:
            - User adoption acceleration programs
            - Training and certification pathways
            - Support model and service level agreements
            - Community building and best practice sharing
            - Continuous optimization and enhancement services

        12. **NEXT STEPS & PARTNERSHIP VISION**:
            - Decision timeline and onboarding acceleration
            - Strategic partnership framework
            - Proof of concept or pilot program proposals
            - Long-term relationship and growth planning

        FORMATTING REQUIREMENTS:
        - Use professional markdown formatting with clear headings and subheadings
        - Include tables for complex information (timelines, costs, risks)
        - Add executive summary boxes for key value propositions
        - Use bullet points for clarity and scanability
        - Include quantified benefits wherever possible
        - Ensure content is tailored to the specific industry and client context
        - Write at an executive level that would impress C-suite decision makers
        - Focus on business outcomes rather than just technical deliverables

        TONE AND APPROACH:
        - Strategic and consultative rather than purely technical
        - Forward-thinking and innovation-focused
        - Risk-aware but opportunity-driven
        - Partnership-oriented rather than vendor-focused
        - Quantified and metrics-driven where possible
        """
        max_generation_config = genai.types.GenerationConfig(
        temperature=0.3,           # Slightly creative but focused
        top_p=0.8,                # Nucleus sampling
        top_k=40,                 # Top-k sampling
        max_output_tokens=8192,   # Maximum tokens for Gemini Pro
        candidate_count=1,        # Number of response candidates
        stop_sequences=None,      # No stop sequences for max output
    )
        response = self.model.generate_content(prompt, generation_config=max_generation_config)
        return response.text
    
    async def analyze_competitive_landscape(self, rfp_text, company_profile):
        """
        Analyze competitive landscape and positioning
        """
        prompt = f"""
        Analyze the competitive landscape for this RFP and provide strategic positioning recommendations:
        
        RFP Text: {rfp_text}
        Company Profile: {company_profile}
        
        Provide:
        1. **Likely Competitors**: Who else will bid on this RFP?
        2. **Competitive Advantages**: What are our unique differentiators?
        3. **Competitive Threats**: Where might we be at a disadvantage?
        4. **Positioning Strategy**: How should we position our proposal?
        5. **Win Themes**: Key messages that will differentiate us
        6. **Price Strategy**: Competitive pricing considerations
        
        Format in markdown with actionable recommendations.
        """
        response = self.model.generate_content(prompt)
        return response.text

    async def generate_executive_briefing(self, rfp_text, company_profile):
        """
        Generate C-suite level executive briefing
        """
        prompt = f"""
        Create an executive briefing document for C-level decision makers:
        
        RFP Text: {rfp_text}
        Company Profile: {company_profile}
        
        Include:
        1. **Strategic Opportunity Assessment** (2-3 sentences)
        2. **Business Impact Summary** (quantified benefits)
        3. **Investment Summary** (high-level costs and ROI)
        4. **Risk Assessment** (top 3 risks and mitigations)
        5. **Decision Recommendation** (Go/No-Go with rationale)
        6. **Key Success Factors** (what needs to happen to win)
        
        Keep it concise - maximum 1 page when printed.
        Use executive language focused on business value, not technical details.
        """
        response = self.model.generate_content(prompt)
        return response.text

    async def assess_innovation_opportunities(self, rfp_text):
        """
        Identify opportunities for innovation and emerging technology integration
        """
        prompt = f"""
        Analyze this RFP for innovation and emerging technology opportunities:
        
        RFP Text: {rfp_text}
        
        Identify:
        1. **AI/ML Integration Opportunities**: Where can AI add value?
        2. **Automation Potential**: What processes can be automated?
        3. **Data Analytics Opportunities**: What insights can be generated?
        4. **Cloud-Native Advantages**: How can cloud architecture benefit the client?
        5. **Industry 4.0 Applications**: IoT, edge computing, digital twin opportunities
        6. **Future Technology Roadmap**: 2-3 year technology evolution plan
        
        Focus on business value and competitive advantage, not just technical possibilities.
        """
        response = self.model.generate_content(prompt)
        return response.text
    
    async def analyze_rfp(self, rfp_text):
        """
        Analyze the RFP document and provide a comprehensive breakdown
        """
        prompt = f"""
        You are an expert RFP analyst. Analyze the following RFP document and provide a detailed breakdown:
        
        RFP Text:
        {rfp_text}
        
        Provide a comprehensive breakdown that includes:
        1. Executive Summary - Brief overview of the RFP
        2. Key Requirements - Critical requirements listed in the RFP
        3. Evaluation Criteria - How proposals will be evaluated
        4. Timeline - Important dates and deadlines
        5. Budget Considerations - Any budget information provided
        
        Format your response in markdown.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    async def extract_requirements(self, rfp_text):
        """
        Extract specific requirements from the RFP text
        """
        prompt = f"""
        You are an expert in requirement analysis. Extract and categorize all requirements from the following RFP text:
        
        RFP Text:
        {rfp_text}
        
        For each requirement:
        1. Assign a unique ID (REQ-001, REQ-002, etc.)
        2. Classify as Functional, Non-Functional, Technical, or Business
        3. Assign a priority (Critical, High, Medium, Low)
        4. Provide a clear, concise description
        
        Format your response as a markdown table with these columns:
        | ID | Type | Priority | Requirement Description |
        
        Ensure all requirements are specific, measurable, and actionable.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    async def generate_tasks(self, requirements):
        """
        Generate actionable Jira-style tasks based on the requirements
        """
        prompt = f"""
        You are a project manager experienced in breaking down requirements into actionable tasks. 
        Based on the following requirements, create Jira-style tasks:
        
        Requirements:
        {requirements}
        
        For each task:
        1. Assign a unique ID (TASK-001, TASK-002, etc.)
        2. Provide a short, descriptive title
        3. Write a detailed description
        4. Estimate effort (Story Points: 1, 2, 3, 5, 8, 13)
        5. Assign a task type (Development, Testing, Documentation, Design)
        6. Map to the requirement ID it fulfills
        
        Format your response as a markdown table with these columns:
        | Task ID | Title | Description | Story Points | Type | Requirement ID |
        
        Ensure tasks are specific, actionable, and can be completed in 1-3 days of work.
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    


    


    # def extract_text_from_docx_proposal(self, docx_file):
    #     """
    #     Convert DOCX to PDF and then extract text using Gemini
    #     """
    #     try:
    #         # Create temporary directory for file processing
    #         with tempfile.TemporaryDirectory() as temp_dir:
    #             # Save uploaded DOCX file temporarily
    #             docx_path = os.path.join(temp_dir, "document.docx")
    #             with open(docx_path, "wb") as f:
    #               f.write(docx_file.file.read())
                
    #             # Convert DOCX to PDF
    #             pdf_path = os.path.join(temp_dir, "document.pdf")
    #             convert(docx_path, pdf_path)
                
    #             # Extract text from PDF using Gemini
    #             return self.extract_text_from_pdf_file_proposal(pdf_path)
                
    #     except Exception as e:
    #         raise Exception(f"Error processing DOCX file: {str(e)}")
    #         return None

    # def extract_text_from_pdf_file_proposal(self, pdf_path):
    #     """
    #     Extract text from PDF file using Gemini's multimodal capabilities
    #     """
    #     try:
    #         # Upload file to Gemini
    #         with open(pdf_path, 'rb') as f:
    #             pdf_bytes = f.read()
            
    #         # Extract text using Gemini
    #         prompt = """
    #         Please extract all text content from this PDF document. 
    #         Return only the extracted text without any additional formatting or commentary.
    #         Preserve the structure and organization of the content as much as possible.
    #         Also include the PDF page number for each section of text.
    #         """
        
    #         response = self.model.generate_content([
    #             prompt,
    #             {'mime_type': 'application/pdf', 'data': pdf_bytes}
    #         ])
            
    #         # Check if response was successful and has text
    #         if response and hasattr(response, 'text') and response.text:
    #             return response.text
    #         else:
    #             st.error("No text content returned from Gemini")
    #             return None
                
    #     except Exception as e:
    #         st.error(f"Error extracting text from PDF: {str(e)}")
    #         return None
    
    # def extract_text_from_uploaded_pdf_proposal(self, pdf_file):
    #     """
    #     Extract text from uploaded PDF file using Gemini
    #     """
   
    #     try:
    #         # Create temporary file for PDF processing
    #         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
    #             temp_file.write(pdf_file.read())
    #             temp_file_path = temp_file.name
            
    #         try:
    #             # Extract text using Gemini
    #             text = self.extract_text_from_pdf_file(temp_file_path)
    #             return text
    #         finally:
    #             # Clean up temporary file
    #             os.unlink(temp_file_path)
                
    #     except Exception as e:
    #         st.error(f"Error processing uploaded PDF: {str(e)}")
    #         return None
    

    async def extract_text_from_pdf_file_proposal(self, pdf_path: str):
        """Extract text from a PDF file using Gemini"""
        try:
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

           
            prompt = """
            Please extract all text content from this PDF document. 
            Return only the extracted text without any additional formatting or commentary.
            Preserve the structure and organization of the content as much as possible.
            Also include the PDF page number for each section of text.
            """

            response = await self.model.generate_content_async(
                [prompt, {"mime_type": "application/pdf", "data": pdf_bytes}]
            )

            if response and hasattr(response, "text") and response.text:
                return response.text
            else:
                raise Exception("No text content returned from Gemini")

        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    async def extract_text_from_uploaded_pdf_proposal(self, pdf_file):
        """Extract text from an uploaded PDF file"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                content = await pdf_file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name

            try:
                text = await self.extract_text_from_pdf_file_proposal(temp_file_path)
                return text
            finally:
                os.unlink(temp_file_path)

        except Exception as e:
            raise Exception(f"Error processing uploaded PDF: {str(e)}")

    async def extract_text_from_docx_proposal(self, docx_file):
        """Extract text from DOCX using Gemini"""
        try:
            content = await docx_file.read()
            prompt = "Extract all text content from this DOCX file."

            response = await self.model.generate_content_async(
                [
                    prompt,
                    {
                        "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "data": content,
                    },
                ]
            )

            return response.text if response and hasattr(response, "text") else None

        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
        
    async def analysis_proposal(self, proposal_text, extra_components=None):
        """
        Check the key components that are present in the RFP proposal
        
        Args:
            proposal_text (str): The RFP proposal text to analyze
            extra_components (str or list, optional): Additional components to check for
        
        Returns:
            str: Analysis results in markdown table format
        """
        standard_components = [
            "1. Executive Summary / Project Overview",
            "2. Scope of Work (In Scope)",
            "3. Out of Scope",
            "4. Prerequisites / Requirements",
            "5. Deliverables",
            "6. Timeline / Schedule",
            "7. Technology Stack / Technical Requirements",
            "8. Budget / Cost Estimation",
            "9. Team Structure / Resources",
            "10. Risk Assessment / Mitigation",
            "11. Success Criteria / Acceptance Criteria",
            "12. Testing Strategy",
            "13. Maintenance & Support",
            "14. Additional Comments / Notes"
        ]
        
        # Create copy of standard components
        components_to_check = standard_components.copy()
        
        # Handle extra components
        if extra_components:
            next_number = len(standard_components) + 1
            
            if isinstance(extra_components, str):
                components_to_check.append(f"{next_number}. {extra_components}")
            elif isinstance(extra_components, list):
                for component in extra_components:
                    components_to_check.append(f"{next_number}. {component}")
                    next_number += 1
        
        components_list = "\n  ".join(components_to_check)
        
        prompt = f"""
        You are a project manager experienced in analyzing RFP (Request for Proposal) documents. 
        Based on the following proposal text, analyze which key RFP components are present:
        
        Proposal Text:
        {proposal_text}
        
        The RFP components to check for are:
        {components_list}
        
        Format your response as a markdown table with these columns:
        | Component | Present (True/False) if true ✅ else ❌  | Details/Notes | PageNumber
        
        For each component, indicate whether it's present in the proposal and provide brief details if found.
        """       
        response = self.model.generate_content(prompt)
        return response.text
    
    async def analyze_pricing(self, proposal_text, ai_analysis_details, historical_data=None):

        """
        Analyze pricing on a component-wise basis for detailed breakdown and evaluation
        """
        prompt = f"""
        Perform a comprehensive component-wise price analysis on the following proposal.
        Use the component scope identified in the AI analysis to structure the pricing breakdown.
 
        PROPOSAL TEXT:
        {proposal_text}
 
        AI ANALYSIS DETAILS (Component Scope Reference):
        {ai_analysis_details}
 
        ---
        COMPONENT-WISE PRICING ANALYSIS
 
        Based on the components identified in the AI analysis details above, please analyze and present the pricing information in the following structured format:
 
        1. **COMPONENT SCOPE MAPPING**:
        First, extract and list all components/deliverables identified in the AI analysis details:
        - Map each component from the scope to its corresponding pricing
        - Identify any pricing items not covered in the scope
        - Flag any scope items without clear pricing
 
        2. **PRICING BREAKDOWN BY COMPONENT**:
        Create a detailed table for each component found in the AI analysis:
        | Component Name | Scope Description | Quantity | Unit Price | Total Price | Price Category | Pricing Notes |
 
        For each component from the AI analysis, identify:
        - Component name as defined in the analysis
        - Scope description from the AI analysis
        - Quantity or units for pricing
        - Individual unit pricing
        - Total cost for that component
        - Category (Labor, Materials, Software, Hardware, Services, etc.)
        - Any special pricing conditions or notes
 
        3. **LABOR COMPONENT ANALYSIS** (based on scope):
        For labor components identified in the AI analysis:
        - Break down by role/skill level mentioned in scope
        - Hourly rates for each position
        - Total hours allocated per role
        - Compare rates with market standards for similar scope
        - Identify any premium or discounted positions
 
        4. **DELIVERABLE COMPONENT ANALYSIS**:
        For each deliverable identified in the AI analysis scope:
        - Deliverable name and description
        - Associated costs and pricing structure
        - Timeline impact on pricing
        - Quality/complexity factors affecting price
 
        5. **SERVICE COMPONENT ANALYSIS**:
        Based on services defined in the component scope:
        - Professional services breakdown
        - Implementation and deployment costs
        - Training costs per component
        - Support and maintenance per component
        - Service level agreements and warranty costs
 
        6. **TECHNOLOGY COMPONENT ANALYSIS**:
        For technology components from the scope analysis:
        - Software licenses and costs per component
        - Hardware requirements and pricing
        - Integration costs between components
        - Maintenance and support costs per technology component
 
        7. **COMPONENT COST RANKING**:
        - Rank all components from AI analysis by total cost (highest to lowest)
        - Calculate percentage of total cost for each component
        - Identify the top 5 most expensive components from the scope
        - Show cost distribution across all identified components
 
        8. **SCOPE-TO-PRICING ALIGNMENT**:
        - Verify that all scope components have corresponding pricing
        - Identify any pricing without clear scope definition
        - Flag potential scope creep or missing elements
        - Assess if pricing aligns with component complexity/effort
 
        9. **COMPONENT-SPECIFIC RECOMMENDATIONS**:
        For each major component identified in the AI analysis:
        - Pricing reasonableness assessment
        - Value proposition evaluation
        - Risk factors specific to that component
        - Negotiation points or alternatives
        - Cost optimization opportunities
 
        10. **COMPONENT INTERDEPENDENCIES**:
        - Identify pricing dependencies between components
        - Assess bundled vs. individual component pricing
        - Evaluate impact of component changes on overall pricing
        - Recommend optimal component packaging
 
        Format the response in clear markdown with tables where appropriate.
        Ensure all analysis is tied back to the specific components identified in the AI analysis details.
        Focus on providing actionable insights for each component rather than general assessments.
        """
 
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error in component-wise price analysis: {str(e)}"

    async def analyze_cost_realism(self, proposal_text, ai_analysis_details):
        """
        Implement FAR 15.404-1(d) Cost Realism Analysis
        """
        prompt = f"""
        Perform a comprehensive cost realism analysis on the following government contract proposal 
        per FAR 15.404-1(d). Evaluate whether the proposed costs are realistic for the work to be performed.

        PROPOSAL TEXT:
        {proposal_text}

        AI ANALYSIS DETAILS:
        {ai_analysis_details}

        ---
        COST REALISM ANALYSIS REQUIREMENTS:

        1. LABOR COST REALISM:
        - Analyze proposed labor categories and skill levels
        - Evaluate if labor hours are realistic for proposed tasks
        - Compare labor rates with market standards and locality pay
        - Assess if proposed labor mix matches technical requirements
        - Flag any unusually high or low labor estimates

        2. MATERIAL COST REALISM:
        - Evaluate material quantities vs. work scope
        - Assess material specifications and quality requirements
        - Compare material costs with market prices
        - Check for appropriate material waste/shrinkage factors
        - Identify any missing or under-estimated materials

        3. SUBCONTRACTOR COST REALISM:
        - Analyze subcontractor selection and pricing
        - Evaluate if subcontractor capabilities match requirements
        - Assess prime contractor oversight and management costs
        - Check for appropriate subcontractor profit margins

        4. OVERHEAD AND INDIRECT COST ANALYSIS:
        - Evaluate overhead rates for reasonableness
        - Assess G&A expenses and allocation methods
        - Review facilities costs and utilization rates
        - Analyze other direct costs (ODCs) for appropriateness

        5. SCHEDULE REALISM vs. COST:
        - Evaluate if proposed timeline is achievable with proposed resources
        - Assess potential for schedule compression costs
        - Identify resource conflicts or unrealistic assumptions
        - Check for adequate contingency in schedule and cost

        6. TECHNICAL APPROACH vs. COST ALIGNMENT:
        - Verify costs support proposed technical solution
        - Identify any disconnects between approach and resources
        - Assess if proposed team size matches work complexity
        - Evaluate innovation/risk vs. cost trade-offs

        ---
        RISK ASSESSMENT:
        
        1. PERFORMANCE RISK:
        - Identify areas where low costs may impact performance
        - Assess contractor's ability to deliver with proposed resources
        - Evaluate potential for cost growth during performance

        2. SCHEDULE RISK:
        - Analyze if costs support schedule commitments
        - Identify resource-constrained critical path items
        - Assess potential for schedule slippage due to underestimating

        3. COST GROWTH RISK:
        - Identify line items most likely to experience overruns
        - Evaluate adequacy of management reserve/contingency
        - Assess historical contractor performance on similar efforts

        ---
        FINAL COST REALISM DETERMINATION:
        Provide:
        - Overall cost realism assessment (Realistic/Unrealistic/Questionable)
        - Specific areas of concern requiring clarification
        - Recommended adjustments to most probable cost
        - Risk mitigation strategies for identified concerns
        - Suggested areas for negotiation or contractor clarification
        
        Format your response with clear sections and specific findings.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error in cost realism analysis: {str(e)}"

    async def technical_analysis_review(self, proposal_text):
        """
        Perform comprehensive technical analysis and evaluation
        """
        prompt = f"""
        Conduct a thorough technical analysis of the following proposal to evaluate the contractor's 
        technical approach, capability, and likelihood of successful performance.

        PROPOSAL TEXT:
        {proposal_text}

        ---
        TECHNICAL ANALYSIS FRAMEWORK:

        1. TECHNICAL APPROACH EVALUATION:
        - Assess comprehensiveness of proposed solution
        - Evaluate innovation and state-of-the-art considerations
        - Analyze methodology and work breakdown structure
        - Review integration of all technical requirements
        - Identify any gaps or weaknesses in approach

        2. TECHNICAL FEASIBILITY ASSESSMENT:
        - Evaluate realistic achievability of proposed solution
        - Assess technical risks and mitigation strategies
        - Review compliance with technical specifications
        - Analyze performance requirements vs. proposed capabilities
        - Identify potential technical challenges

        3. PAST PERFORMANCE CORRELATION:
        - Assess relevance of cited past performance
        - Evaluate scale and complexity comparisons
        - Review lessons learned integration
        - Analyze team continuity from past efforts
        - Assess risk based on performance history

        4. PERSONNEL AND QUALIFICATIONS:
        - Evaluate key personnel qualifications vs. requirements
        - Assess team composition and skill mix
        - Review organizational structure and reporting
        - Analyze staffing plan adequacy
        - Identify potential resource constraints

        5. FACILITIES AND EQUIPMENT:
        - Assess facility adequacy for proposed work
        - Evaluate equipment capabilities and availability
        - Review security clearance and facility requirements
        - Analyze geographic distribution if applicable
        - Assess infrastructure support capabilities

        6. SUBCONTRACTOR INTEGRATION:
        - Evaluate subcontractor technical capabilities
        - Assess prime contractor management approach
        - Review work allocation and integration plans
        - Analyze communication and coordination methods
        - Assess overall team cohesion

        ---
        RISK ANALYSIS:

        1. TECHNICAL PERFORMANCE RISKS:
        - Identify high-risk technical areas
        - Assess probability and impact of technical failures
        - Evaluate backup plans and alternatives
        - Review testing and validation approaches

        2. SCHEDULE RISKS:
        - Analyze critical path technical dependencies
        - Assess resource loading and availability
        - Evaluate parallel vs. sequential work planning
        - Identify potential schedule compression impacts

        3. INTEGRATION RISKS:
        - Assess system integration complexity
        - Evaluate interface management approach
        - Review compatibility with existing systems
        - Analyze interoperability requirements

        ---
        COMPLIANCE VERIFICATION:
        - Verify compliance with all technical requirements
        - Identify any deviations or exceptions
        - Assess impact of proposed alternatives
        - Review regulatory and standard compliance

        ---
        FINAL TECHNICAL ASSESSMENT:
        Provide:
        - Overall technical rating (Excellent/Good/Satisfactory/Marginal/Unsatisfactory)
        - Key technical strengths and innovations
        - Critical technical weaknesses or gaps
        - Recommended areas for clarification
        - Risk mitigation recommendations
        - Technical evaluation summary for source selection
        
        Structure your response with clear headings and specific technical findings.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error in technical analysis: {str(e)}"

    async def compliance_assessment(self, proposal_text):
        """
        Comprehensive compliance assessment against RFP requirements
        """
        prompt = f"""
        Perform a detailed compliance assessment of the following proposal to determine adherence 
        to RFP requirements and identify any non-compliant areas.

        PROPOSAL TEXT:
        {proposal_text}

        ---
        COMPLIANCE ASSESSMENT AREAS:

        1. PROPOSAL FORMAT AND SUBMISSION REQUIREMENTS:
        - Verify adherence to page limits and formatting
        - Check required sections and content organization
        - Assess completeness of required submissions
        - Review compliance with submission instructions
        - Identify any missing required documents

        2. TECHNICAL REQUIREMENTS COMPLIANCE:
        - Verify compliance with all technical specifications
        - Check adherence to performance requirements
        - Assess compliance with quality standards
        - Review regulatory and code compliance
        - Identify any technical requirement gaps

        3. CONTRACTUAL TERMS AND CONDITIONS:
        - Assess acceptance of standard contract terms
        - Review any proposed exceptions or deviations
        - Evaluate compliance with special contract requirements
        - Check adherence to delivery and performance terms
        - Assess warranty and support commitments

        4. CERTIFICATION AND REGISTRATION REQUIREMENTS:
        - Verify required business registrations (SAM, CAGE)
        - Check industry-specific certifications
        - Assess personnel certification requirements
        - Review facility accreditation needs
        - Verify small business representations

        5. SECURITY AND CLEARANCE REQUIREMENTS:
        - Assess facility security clearance (FSC) compliance
        - Verify personnel security clearance requirements
        - Review information security protocols
        - Check ITAR/EAR compliance if applicable
        - Assess cybersecurity requirements adherence

        6. ADMINISTRATIVE REQUIREMENTS:
        - Verify cost/price proposal format compliance
        - Check required cost breakdowns and supporting data
        - Assess audit trail and cost traceability
        - Review required representations and certifications
        - Verify proper signature authorities

        ---
        SOCIOECONOMIC COMPLIANCE:

        1. Small Business Requirements:
        - Verify small business size standard compliance
        - Check subcontracting plan requirements
        - Assess HUBZone, SDVOSB, WOSB compliance
        - Review mentor-protégé arrangements
        - Evaluate small business participation goals

        2. Equal Opportunity Compliance:
        - Assess EEO compliance statements
        - Review affirmative action commitments
        - Check VEVRAA compliance
        - Evaluate Section 503 compliance
        - Assess diversity and inclusion commitments

        ---
        ENVIRONMENTAL AND SAFETY COMPLIANCE:
        - Verify environmental regulation compliance
        - Assess workplace safety requirements
        - Check hazardous material handling protocols
        - Review waste disposal and recycling plans
        - Evaluate sustainability requirements

        ---
        DATA MANAGEMENT AND INTELLECTUAL PROPERTY:
        - Assess data delivery requirements compliance
        - Review intellectual property rights handling
        - Check data rights and licensing terms
        - Evaluate information handling protocols
        - Assess government access requirements

        ---
        COMPLIANCE RISK ASSESSMENT:
        - Identify critical compliance gaps
        - Assess risk of non-compliance impacts
        - Evaluate potential for cure/correction
        - Assess past compliance performance
        - Review compliance management systems

        ---
        FINAL COMPLIANCE DETERMINATION:
        Provide:
        - Overall compliance rating (Compliant/Conditionally Compliant/Non-Compliant)
        - List of all compliance gaps or concerns
        - Critical vs. minor compliance issues
        - Recommended actions for compliance resolution
        - Areas requiring clarification or correction
        - Compliance risk assessment for contract award
        
        Format response with clear compliance status for each major area.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error in compliance assessment: {str(e)}"

    async def analysis_proposal_summary(self, proposal_text, ai_analysis_details, price_analysis=None, 
                                cost_realism=None, technical_analysis=None, compliance_assessment=None):
        """
        Generate a comprehensive executive summary of the RFP proposal analysis combining all evaluation components
        
        Args:
            proposal_text: The main proposal content for overall assessment
            ai_analysis_details: Detailed component analysis from AI assessment
            price_analysis: Results of price competitiveness analysis (optional)
            cost_realism: Results of cost realism analysis (optional)
            technical_analysis: Results of technical evaluation (optional)
            compliance_assessment: Compliance verification results (optional)
            
        Returns:
            str: A comprehensive executive summary in markdown format suitable for decision-makers
        """
        prompt = f"""
        As a senior government contracts specialist, generate a comprehensive 2-3 page executive summary 
        that synthesizes all analyses of this proposal. The summary should provide clear, actionable 
        insights for procurement decision-makers.
        
        # INPUT DATA
        
        ## PROPOSAL CONTENT:
        {proposal_text}
        
        ## DETAILED ANALYSES:
        
        **AI Component Analysis:**
        {ai_analysis_details}
        
        **Price Analysis:**
        {price_analysis if price_analysis else "Not performed"}
        
        **Cost Realism Assessment:**
        {cost_realism if cost_realism else "Not performed"}
        
        **Technical Evaluation:**
        {technical_analysis if technical_analysis else "Not performed"}
        
        **Compliance Verification:**
        {compliance_assessment if compliance_assessment else "Not performed"}
        
        # REQUIRED OUTPUT STRUCTURE
        
        ## 1. EXECUTIVE OVERVIEW
        - High-level proposal assessment (completeness, quality, competitiveness)
        - Key statistics (page count, sections completed, compliance rate)
        - Overall recommendation (Approve/Conditional Approval/Reject)
        - Summary of most significant findings
        
        ## 2. COMPONENT ANALYSIS SUMMARY
        - Table of critical components with status indicators:
        | Component | Status (✅/❌) | Notes | Page Number |
        |-----------|--------------|-------|----------------|
        [Include all major components from analysis]
        - Missing or incomplete elements
        - Quality assessment of provided components
        
        ## 3. EVALUATION MATRIX
        Create a quick-reference table summarizing all evaluation factors:
        | Factor | Rating (1-5) | Strengths | Concerns |
        |--------|-------------|-----------|----------|
        | Technical Approach | | | |
        | Price/Cost | | | |
        | Compliance | | | |
        | Risk | | | |
        | Past Performance | | | |
        
        ## 4. DETAILED ASSESSMENT SECTIONS
        
        **A. Technical Evaluation**
        - Approach adequacy and innovation
        - Team qualifications
        - Technical risks and mitigation
        
        **B. Price/Cost Analysis**
        - Price competitiveness
        - Cost realism findings
        - Value proposition
        - Budget alignment
        
        **C. Compliance Status**
        - Mandatory requirements met/missing
        - Conditional compliance items
        - Documentation completeness
        
        ## 5. RISK ASSESSMENT
        - Performance risk (High/Medium/Low)
        - Cost growth potential
        - Schedule risks
        - Technical implementation risks
        - Overall risk rating with justification
        
        ## 6. STRENGTHS & WEAKNESSES
        - Top 3 proposal strengths
        - Top 3 critical weaknesses
        - Competitive advantages
        - Areas requiring clarification
        
        ## 7. RECOMMENDATIONS & NEXT STEPS
        - Award recommendation
        - Required negotiations or clarifications
        - Suggested contract type
        - Special conditions if applicable
        - Timeline for resolution if conditional
        
        # FORMATTING REQUIREMENTS
        - Use professional government contracting terminology
        - Include specific examples and page references
        - Highlight critical decision points
        - Balance conciseness with comprehensive coverage
        - Use markdown formatting with clear headings
        - Include quantitative metrics where available
        
        Generate approximately 1500-2000 words of detailed analysis suitable for senior leadership review.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating proposal summary: {str(e)}"



























