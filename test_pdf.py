#!/usr/bin/env python3
"""
Test PDF generation functionality
"""

import os
import sys
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

def generate_pdf_report(analysis_data, output_path):
    """Generate a professional PDF report for malware analysis"""
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    # Title
    story.append(Paragraph("🔍 AI MALWARE DETECTION REPORT", title_style))
    story.append(Spacer(1, 20))
    
    # File Information Section
    story.append(Paragraph("📁 FILE INFORMATION", heading_style))
    file_info = [
        ['Property', 'Value'],
        ['Filename', analysis_data.get('filename', 'N/A')],
        ['Analysis Time', analysis_data.get('timestamp', 'N/A')],
        ['Analysis ID', analysis_data.get('id', 'N/A')]
    ]
    
    file_table = Table(file_info, colWidths=[2*inch, 4*inch])
    file_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(file_table)
    story.append(Spacer(1, 20))
    
    # Analysis Results Section
    story.append(Paragraph("🤖 AI PREDICTION RESULTS", heading_style))
    
    prediction = analysis_data.get('prediction', 'Unknown')
    risk_score = analysis_data.get('risk_score', 0)
    confidence = analysis_data.get('confidence', {})
    
    # Determine threat level and color
    if prediction == 'MALWARE':
        threat_color = colors.red
        threat_level = "🚨 HIGH RISK"
    else:
        threat_color = colors.green
        threat_level = "✅ LOW RISK"
    
    results_info = [
        ['Metric', 'Value'],
        ['Verdict', f"{prediction}"],
        ['Risk Score', f"{risk_score:.1f}%"],
        ['Threat Level', threat_level],
        ['Malware Confidence', f"{confidence.get('malware', 0):.3f}"],
        ['Benign Confidence', f"{confidence.get('benign', 0):.3f}"]
    ]
    
    results_table = Table(results_info, colWidths=[2*inch, 4*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 2), (-1, 2), threat_color),  # Risk score row
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(results_table)
    story.append(Spacer(1, 20))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,
        textColor=colors.grey
    )
    
    story.append(Spacer(1, 40))
    story.append(Paragraph("AI Malware Detection System © 2025 | Powered by Machine Learning & Virtual Machine Analysis", footer_style))
    
    # Build PDF
    doc.build(story)
    return output_path

if __name__ == "__main__":
    # Test data
    test_data = {
        'id': 'test_123',
        'filename': 'test_file.exe',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'prediction': 'BENIGN',
        'risk_score': 15.5,
        'confidence': {'malware': 0.155, 'benign': 0.845},
        'behavioral_summary': {
            'new_processes': 5,
            'network_connections': 0,
            'files_created': 3,
            'suspicious_activities': 2
        },
        'features': {
            'malware_risk_score': 15.5,
            'process_count': 5,
            'file_operations': 3
        }
    }
    
    # Create reports directory
    os.makedirs('reports/pdf', exist_ok=True)
    
    # Generate PDF
    output_file = 'reports/pdf/test_report.pdf'
    try:
        generate_pdf_report(test_data, output_file)
        print(f"✅ PDF generated successfully: {output_file}")
        print(f"✅ File exists: {os.path.exists(output_file)}")
        print(f"✅ File size: {os.path.getsize(output_file)} bytes")
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        import traceback
        traceback.print_exc()
