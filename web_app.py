"""
AI Malware Detection System - Advanced Web GUI
God-tier Flask application with real-time analysis, interactive dashboards, and modern UI
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_socketio import SocketIO, emit
import os
import json
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
import plotly.graph_objs as go
import plotly.utils
from werkzeug.utils import secure_filename
import zipfile
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

# Import our AI detection system
import sys
sys.path.append(str(Path(__file__).parent))
from src.detection.ai_malware_tester import MalwareDetector
from src.analysis.vm_behavior_analyzer import VMBehaviorAnalyzer

def serialize_for_json(obj):
    """Convert datetime objects to JSON-serializable format"""
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, dict):
        return {key: serialize_for_json(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    else:
        return obj

def generate_pdf_report(analysis_data, output_path):
    """Generate a comprehensive PDF report for malware analysis"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=0.5*inch, rightMargin=0.5*inch)
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
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.darkgreen
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
    prediction_details = analysis_data.get('prediction_details', {})
    
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
    
    # Behavioral Analysis Section
    behavioral_summary = analysis_data.get('behavioral_summary', {})
    if behavioral_summary:
        story.append(Paragraph("🔬 BEHAVIORAL ANALYSIS SUMMARY", heading_style))
        
        behavioral_info = [
            ['Behavior Category', 'Count/Status'],
            ['Execution Success', '✅' if behavioral_summary.get('execution_success') else '❌'],
            ['New Processes', str(behavioral_summary.get('new_processes', 0))],
            ['Network Connections', str(behavioral_summary.get('network_connections', 0))],
            ['Files Created', str(behavioral_summary.get('files_created', 0))],
            ['Registry Changes', str(behavioral_summary.get('registry_changes', 0))],
            ['Suspicious Activities', str(behavioral_summary.get('suspicious_activities', 0))]
        ]
        
        behavioral_table = Table(behavioral_info, colWidths=[3*inch, 3*inch])
        behavioral_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(behavioral_table)
        story.append(Spacer(1, 20))
    
    # ML Features Section
    features = analysis_data.get('features', {})
    if features:
        story.append(Paragraph("📊 MACHINE LEARNING FEATURES", heading_style))
        
        # Key ML features
        key_features = [
            ['Feature', 'Value'],
            ['Malware Risk Score', f"{features.get('malware_risk_score', 0):.2f}"],
            ['Suspicious Process Count', str(features.get('suspicious_process_count', 0))],
            ['Network Activity Detected', 'Yes' if features.get('has_network_activity', 0) else 'No'],
            ['Files Created Count', str(features.get('files_created_count', 0))],
            ['Execution Errors', 'Yes' if features.get('has_execution_error', 0) else 'No'],
            ['Registry Modifications', str(features.get('registry_changes_count', 0))],
            ['Process Spawning Activity', str(features.get('process_spawn_count', 0))],
            ['System Resource Usage', f"{features.get('system_resource_usage', 0):.2f}"]
        ]
        
        features_table = Table(key_features, colWidths=[3*inch, 3*inch])
        features_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(features_table)
        story.append(Spacer(1, 15))
    
    # Detailed Process Analysis
    detailed_analysis = analysis_data.get('detailed_analysis', {})
    behavioral_changes = detailed_analysis.get('behavioral_changes', {})
    
    if behavioral_changes:
        story.append(Paragraph("🔍 DETAILED PROCESS ANALYSIS", heading_style))
        
        # New Processes
        new_processes = behavioral_changes.get('new_processes', [])
        if new_processes:
            story.append(Paragraph("New Processes Created:", subheading_style))
            for i, process in enumerate(new_processes[:10], 1):  # Show top 10
                process_text = process[:100] + "..." if len(process) > 100 else process
                story.append(Paragraph(f"{i}. {process_text}", styles['Normal']))
            if len(new_processes) > 10:
                story.append(Paragraph(f"... and {len(new_processes) - 10} more processes", styles['Normal']))
            story.append(Spacer(1, 10))
        
        # Suspicious Activities
        suspicious_activities = behavioral_changes.get('suspicious_activities', [])
        if suspicious_activities:
            story.append(Paragraph("🚨 SUSPICIOUS ACTIVITIES DETECTED:", subheading_style))
            for i, activity in enumerate(suspicious_activities[:15], 1):  # Show top 15
                activity_text = activity[:120] + "..." if len(activity) > 120 else activity
                story.append(Paragraph(f"{i}. {activity_text}", styles['Normal']))
            if len(suspicious_activities) > 15:
                story.append(Paragraph(f"... and {len(suspicious_activities) - 15} more activities", styles['Normal']))
            story.append(Spacer(1, 10))
        
        # Network Connections
        network_connections = behavioral_changes.get('new_network_connections', [])
        if network_connections:
            story.append(Paragraph("🌐 NETWORK CONNECTIONS:", subheading_style))
            for i, connection in enumerate(network_connections[:10], 1):  # Show top 10
                story.append(Paragraph(f"{i}. {connection}", styles['Normal']))
            if len(network_connections) > 10:
                story.append(Paragraph(f"... and {len(network_connections) - 10} more connections", styles['Normal']))
            story.append(Spacer(1, 10))
    
    # Threat Assessment Section
    story.append(Paragraph("⚠️ THREAT ASSESSMENT & RECOMMENDATIONS", heading_style))
    
    # Assessment text based on prediction
    if prediction == 'MALWARE':
        assessment_text = """
        <b>🚨 HIGH RISK - MALWARE DETECTED</b><br/>
        • Immediate isolation recommended<br/>
        • Do not execute this file<br/>
        • Scan system for potential compromise<br/>
        • Review file source and distribution method<br/>
        • Consider forensic analysis for attribution<br/>
        • Update security policies and detection rules
        """
        assessment_color = colors.red
    else:
        assessment_text = f"""
        <b>✅ VERY LOW RISK - Appears to be legitimate software</b><br/>
        • File passed AI malware detection<br/>
        • Behavioral analysis shows normal activity<br/>
        • Safe to use with standard precautions<br/>
        • Continue monitoring for unusual behavior<br/>
        • Keep security software updated<br/>
        • Recommendation: Safe to use
        """
        assessment_color = colors.green
    
    story.append(Paragraph(assessment_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Analysis Details
    story.append(Paragraph("📋 ANALYSIS TECHNICAL DETAILS", heading_style))
    
    tech_details = [
        ['Technical Parameter', 'Value'],
        ['AI Model Used', 'Gradient Boosting Classifier'],
        ['Features Analyzed', str(prediction_details.get('features_used', 'N/A'))],
        ['VM Analysis Duration', f"{detailed_analysis.get('analysis_duration', 'N/A')} seconds"],
        ['Analysis Engine Version', '2025.09'],
        ['Detection Database', 'Updated'],
        ['Confidence Threshold', '0.5']
    ]
    
    tech_table = Table(tech_details, colWidths=[3*inch, 3*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 30))
    
    # Footer
    footer_text = """
    <i>AI Malware Detection System © 2025 | Powered by Machine Learning & Virtual Machine Analysis<br/>
    This report was generated using advanced behavioral analysis and gradient boosting classification.<br/>
    For technical support or questions about this analysis, please contact your security team.</i>
    """
    story.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Comprehensive PDF report generated: {output_path}")


# Flask configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'malware-detection-system-2025'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Initialize SocketIO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Global variables for system state
analysis_queue = []
analysis_results = []
results_file = Path('analysis_results.json')

# Load existing analysis results on startup
def load_analysis_results():
    """Load analysis results from persistent storage"""
    global analysis_results
    if results_file.exists():
        try:
            with open(results_file, 'r', encoding='utf-8') as f:
                analysis_results = json.load(f)
            print(f"📊 Loaded {len(analysis_results)} previous analysis results")
        except Exception as e:
            print(f"⚠️ Error loading analysis results: {e}")
            analysis_results = []
    else:
        analysis_results = []

def save_analysis_results():
    """Save analysis results to persistent storage"""
    try:
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(serialize_for_json(analysis_results), f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Error saving analysis results: {e}")

# Load results on startup
load_analysis_results()
system_stats = {
    'total_analyses': 0,
    'malware_detected': 0,
    'benign_detected': 0,
    'analysis_errors': 0,
    'last_analysis': None,
    'system_status': 'Ready',
    'queue_size': 0
}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class AnalysisManager:
    """Manages malware analysis queue and real-time updates"""
    
    def __init__(self):
        self.detector = MalwareDetector()
        self.analyzer = VMBehaviorAnalyzer()
        self.is_processing = False
        self.current_analysis = None
    
    def add_to_queue(self, file_path, original_filename):
        """Add a file to the analysis queue"""
        analysis_id = f"analysis_{int(time.time())}"
        analysis_item = {
            'id': analysis_id,
            'file_path': file_path,
            'filename': original_filename,
            'status': 'Queued',
            'timestamp': datetime.now(),
            'progress': 0,
            'result': None,
            'error': None
        }
        analysis_queue.append(analysis_item)
        system_stats['queue_size'] = len(analysis_queue)
        
        # Emit queue update
        socketio.emit('queue_update', {
            'queue_size': len(analysis_queue),
            'analysis_item': serialize_for_json({
                'id': analysis_id,
                'filename': original_filename,
                'status': 'Queued',
                'timestamp': analysis_item['timestamp']
            })
        })
        
        return analysis_id
    
    def process_queue(self):
        """Process analysis queue in background thread"""
        while True:
            if analysis_queue and not self.is_processing:
                self.is_processing = True
                analysis_item = analysis_queue.pop(0)
                self.current_analysis = analysis_item
                system_stats['queue_size'] = len(analysis_queue)
                
                try:
                    self.analyze_file(analysis_item)
                except Exception as e:
                    analysis_item['error'] = str(e)
                    analysis_item['status'] = 'Error'
                    system_stats['analysis_errors'] += 1
                
                analysis_results.append(analysis_item)
                if len(analysis_results) > 100:  # Keep only last 100 results
                    analysis_results.pop(0)
                
                # Save results to persistent storage
                save_analysis_results()
                
                self.is_processing = False
                self.current_analysis = None
            
            time.sleep(1)
    
    def analyze_file(self, analysis_item):
        """Analyze a single file with real-time progress updates"""
        analysis_item['status'] = 'Analyzing'
        analysis_item['progress'] = 10
        
        # Emit progress update
        socketio.emit('analysis_progress', {
            'id': analysis_item['id'],
            'status': 'Starting VM Analysis',
            'progress': 10
        })
        
        try:
            # Step 1: VM Analysis
            analysis_item['progress'] = 30
            socketio.emit('analysis_progress', {
                'id': analysis_item['id'],
                'status': 'Running in Virtual Machine',
                'progress': 30
            })
            
            result = self.detector.test_file(analysis_item['file_path'], save_report=True)
            
            # Step 2: AI Classification
            analysis_item['progress'] = 70
            socketio.emit('analysis_progress', {
                'id': analysis_item['id'],
                'status': 'AI Classification',
                'progress': 70
            })
            
            # Step 3: Report Generation
            analysis_item['progress'] = 90
            socketio.emit('analysis_progress', {
                'id': analysis_item['id'],
                'status': 'Generating Report',
                'progress': 90
            })
            
            if result['success']:
                analysis_item['result'] = result
                analysis_item['status'] = 'Complete'
                analysis_item['progress'] = 100
                
                # Generate PDF report
                try:
                    pdf_filename = f"malware_report_{analysis_item['id']}.pdf"
                    pdf_dir = os.path.join(os.getcwd(), 'reports', 'pdf')
                    pdf_path = os.path.join(pdf_dir, pdf_filename)
                    os.makedirs(pdf_dir, exist_ok=True)
                    
                    print(f"🔍 Debug: Generating PDF at: {pdf_path}")
                    
                    # Prepare data for PDF generation
                    pdf_data = {
                        'id': analysis_item['id'],
                        'filename': analysis_item['filename'],
                        'timestamp': analysis_item['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                        'prediction': result['prediction'],
                        'risk_score': result['risk_score'],
                        'confidence': {
                            'malware': result.get('prediction_result', {}).get('malware_confidence', 0),
                            'benign': result.get('prediction_result', {}).get('benign_confidence', 0)
                        },
                        'behavioral_summary': {
                            'execution_success': result.get('analysis_result', {}).get('behavioral_data', {}).get('execution_success', False),
                            'new_processes': len(result.get('analysis_result', {}).get('behavioral_data', {}).get('behavioral_changes', {}).get('new_processes', [])),
                            'network_connections': len(result.get('analysis_result', {}).get('behavioral_data', {}).get('behavioral_changes', {}).get('new_network_connections', [])),
                            'files_created': result.get('analysis_result', {}).get('behavioral_data', {}).get('behavioral_changes', {}).get('files_created', 0),
                            'registry_changes': result.get('analysis_result', {}).get('behavioral_data', {}).get('behavioral_changes', {}).get('registry_changes', 0),
                            'suspicious_activities': len(result.get('analysis_result', {}).get('behavioral_data', {}).get('behavioral_changes', {}).get('suspicious_activities', []))
                        },
                        'features': result.get('analysis_result', {}).get('ml_features', {}),
                        'detailed_analysis': result.get('analysis_result', {}).get('behavioral_data', {}),
                        'prediction_details': result.get('prediction_result', {})
                    }
                    
                    generate_pdf_report(pdf_data, pdf_path)
                    analysis_item['pdf_report'] = pdf_path
                    
                    print(f"✅ Debug: PDF generated successfully at: {pdf_path}")
                    print(f"✅ Debug: PDF exists: {os.path.exists(pdf_path)}")
                    print(f"✅ Debug: PDF size: {os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0} bytes")
                    
                except Exception as pdf_error:
                    print(f"❌ PDF generation error: {pdf_error}")
                    import traceback
                    traceback.print_exc()
                    analysis_item['pdf_report'] = None
                
                # Update system stats
                system_stats['total_analyses'] += 1
                if result['prediction'] == 'MALWARE':
                    system_stats['malware_detected'] += 1
                else:
                    system_stats['benign_detected'] += 1
                system_stats['last_analysis'] = datetime.now()
                
                # Emit completion
                completion_data = {
                    'id': analysis_item['id'],
                    'filename': analysis_item['filename'],
                    'prediction': result['prediction'],
                    'risk_score': result['risk_score'],
                    'confidence': result.get('confidence', {}),
                    'behavioral_summary': result.get('behavioral_summary', {}),
                    'features': result.get('features', {}),
                    'report_path': result.get('report_path', ''),
                    'pdf_report': analysis_item.get('pdf_report', ''),
                    'timestamp': analysis_item['timestamp'],
                    'stats': system_stats
                }
                
                print(f"🔍 Debug: Emitting completion data with PDF: {analysis_item.get('pdf_report', 'None')}")
                
                socketio.emit('analysis_complete', serialize_for_json(completion_data))
            else:
                analysis_item['status'] = 'Error'
                analysis_item['error'] = result.get('error', 'Unknown error')
                system_stats['analysis_errors'] += 1
        
        except Exception as e:
            analysis_item['status'] = 'Error'
            analysis_item['error'] = str(e)
            system_stats['analysis_errors'] += 1
        
        # Clean up uploaded file
        try:
            os.remove(analysis_item['file_path'])
        except:
            pass

# Initialize analysis manager
analysis_manager = AnalysisManager()

# Start background processing thread
processing_thread = threading.Thread(target=analysis_manager.process_queue, daemon=True)
processing_thread.start()

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html', stats=system_stats)

@app.route('/upload')
def upload_page():
    """File upload page"""
    return render_template('upload.html')

@app.route('/analyze', methods=['POST'])
def analyze_file():
    """Handle file upload and start analysis"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    timestamp = int(time.time())
    safe_filename = f"{timestamp}_{filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    file.save(file_path)
    
    # Add to analysis queue
    analysis_id = analysis_manager.add_to_queue(file_path, filename)
    
    return jsonify({
        'success': True,
        'analysis_id': analysis_id,
        'message': f'File {filename} added to analysis queue'
    })

@app.route('/download/report/<analysis_id>')
def download_report(analysis_id):
    """Download PDF report for a specific analysis"""
    try:
        print(f"🔍 Debug: Download request for analysis_id: {analysis_id}")
        print(f"🔍 Debug: Available analysis results: {len(analysis_results)}")
        
        # Find the analysis result - try both the given ID and alternative formats
        analysis_result = None
        for result in analysis_results:
            print(f"🔍 Debug: Checking result ID: {result['id']}")
            if (result['id'] == analysis_id or 
                result['id'] == f"analysis_{analysis_id.replace('analysis_', '').replace('behavior_', '')}" or
                result['id'] == f"behavior_{analysis_id.replace('analysis_', '').replace('behavior_', '')}"):
                analysis_result = result
                break
        
        if not analysis_result:
            print(f"❌ Debug: Analysis not found for ID: {analysis_id}")
            return jsonify({'error': 'Analysis not found'}), 404
        
        print(f"✅ Debug: Found analysis result: {analysis_result.get('filename', 'N/A')}")
        
        # Check if PDF report exists
        pdf_path = analysis_result.get('pdf_report')
        print(f"🔍 Debug: PDF path from result: {pdf_path}")
        
        if not pdf_path:
            print(f"❌ Debug: No PDF path in analysis result")
            return jsonify({'error': 'PDF report path not found'}), 404
            
        if not os.path.exists(pdf_path):
            print(f"❌ Debug: PDF file does not exist at: {pdf_path}")
            return jsonify({'error': f'PDF report file not found at: {pdf_path}'}), 404
        
        print(f"✅ Debug: PDF file exists, sending: {pdf_path}")
        
        # Send file
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"malware_analysis_{analysis_result['filename']}_{analysis_id}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"❌ Debug: Download error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/results')
def results_page():
    """Analysis results page"""
    return render_template('results.html')

@app.route('/api/results')
def get_results():
    """API endpoint for analysis results"""
    results_data = []
    for result in reversed(analysis_results[-50:]):  # Last 50 results
        results_data.append({
            'id': result['id'],
            'filename': result['filename'],
            'status': result['status'],
            'timestamp': result['timestamp'],
            'prediction': result['result']['prediction'] if result.get('result') else None,
            'risk_score': result['result']['risk_score'] if result.get('result') else None,
            'pdf_report': result.get('pdf_report', ''),
            'has_pdf': bool(result.get('pdf_report') and os.path.exists(result.get('pdf_report', ''))),
            'error': result.get('error')
        })
    
    return jsonify(serialize_for_json(results_data))

@app.route('/api/stats')
def get_stats():
    """API endpoint for system statistics"""
    return jsonify(serialize_for_json(system_stats))

@app.route('/api/queue')
def get_queue():
    """API endpoint for analysis queue status"""
    queue_data = []
    for item in analysis_queue:
        queue_data.append({
            'id': item['id'],
            'filename': item['filename'],
            'status': item['status'],
            'progress': item['progress'],
            'timestamp': item['timestamp']
        })
    
    return jsonify(serialize_for_json(queue_data))

@app.route('/analytics')
def analytics_page():
    """Advanced analytics dashboard"""
    return render_template('analytics.html')

@app.route('/api/analytics')
def get_analytics():
    """Generate analytics data for dashboard"""
    # Threat distribution
    threat_data = {
        'malware_count': system_stats['malware_detected'],
        'benign_count': system_stats['benign_detected'],
        'error_count': system_stats['analysis_errors']
    }
    
    # Recent activity (last 24 hours)
    recent_activity = []
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    for result in analysis_results:
        if result['timestamp'] > cutoff_time and result.get('result'):
            recent_activity.append({
                'hour': result['timestamp'].hour,
                'is_malware': 1 if result['result']['prediction'] == 'MALWARE' else 0,
                'risk_score': result['result']['risk_score']
            })
    
    # Risk score distribution
    risk_scores = [item['risk_score'] for item in recent_activity]
    
    return jsonify({
        'threat_distribution': threat_data,
        'recent_activity': recent_activity,
        'risk_scores': risk_scores,
        'total_analyses': system_stats['total_analyses']
    })

@app.route('/live')
def live_monitoring():
    """Live monitoring page"""
    return render_template('live.html')

@socketio.on('connect')
def handle_connect(auth):
    """Handle client connection"""
    emit('system_status', serialize_for_json({
        'status': 'Connected',
        'stats': system_stats,
        'queue_size': len(analysis_queue),
        'current_analysis': analysis_manager.current_analysis['filename'] if analysis_manager.current_analysis else None
    }))

@socketio.on('request_update')
def handle_update_request(data=None):
    """Handle manual update request"""
    emit('stats_update', serialize_for_json(system_stats))

if __name__ == '__main__':
    print("🚀 Starting AI Malware Detection Web Interface...")
    print("📊 Dashboard: http://localhost:5000")
    print("🔬 Upload & Analyze: http://localhost:5000/upload")
    print("📈 Analytics: http://localhost:5000/analytics")
    print("📡 Live Monitor: http://localhost:5000/live")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
