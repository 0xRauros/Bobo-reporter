from flask import Flask, render_template, jsonify, request, send_file
import os
import platform
import shutil
from datetime import datetime
from contextlib import closing

from bobo_reader import LOCAL_COPY_PATH
import bobo_reader
from bobo_db import get_official_bookmarks, open_connection, bookmarks_query
from clippings_parser import parse_clippings
from kindle_reports import kindle_report
from get_windows_filepath import find_kindle_documents_path
from utils import query_result_to_book_list
from jinja2 import Environment, FileSystemLoader
from datetime import date

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'tmp/uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('tmp', exist_ok=True)

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)


@app.route('/')
def index():
    """Main page"""
    return render_template('web_index.html')


@app.route('/api/scan-device', methods=['GET'])
def scan_device():
    """Scan for connected Kobo or Kindle devices"""
    try:
        # Check for Kobo (Linux)
        if platform.system() == 'Linux':
            try:
                username = os.getlogin()
                kobo_path = bobo_reader.KOBO_PATH.format(OS_USERNAME=username)
                if os.path.exists(kobo_path):
                    return jsonify({
                        'status': 'success',
                        'device': 'Kobo',
                        'path': kobo_path
                    })
            except (OSError, AttributeError):
                pass  # Kobo detection not available on this system
        
        # Check for Kindle (Windows)
        if platform.system() == 'Windows':
            try:
                kindle_path = find_kindle_documents_path()
                if kindle_path:
                    return jsonify({
                        'status': 'success',
                        'device': 'Kindle',
                        'path': kindle_path
                    })
            except ImportError as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e) + ' Please use file upload instead, or install pywin32: pip install pywin32'
                }), 500
        
        return jsonify({
            'status': 'not_found',
            'message': 'No device detected. Please connect your Kobo or Kindle device, or use file upload.'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/process-kobo', methods=['POST'])
def process_kobo():
    """Process Kobo device and generate report"""
    try:
        # Check if we're on Linux
        if platform.system() != 'Linux':
            return jsonify({
                'status': 'error',
                'message': 'Kobo support is currently only available on Linux systems. Please use file upload instead.'
            }), 400
        
        # Copy database file
        try:
            username = os.getlogin()
            kobo_path = bobo_reader.KOBO_PATH.format(OS_USERNAME=username)
        except (OSError, AttributeError):
            return jsonify({
                'status': 'error',
                'message': 'Could not determine username for Kobo path detection. Please use file upload instead.'
            }), 400
            
        if not os.path.exists(kobo_path):
            return jsonify({
                'status': 'error',
                'message': 'Kobo device not found. Please ensure the device is connected and use file upload if needed.'
            }), 404
        
        shutil.copy(kobo_path, LOCAL_COPY_PATH)
        
        # Get bookmarks
        bookmarks = get_official_bookmarks()
        if not bookmarks:
            clear_tmp()
            return jsonify({
                'status': 'error',
                'message': 'No bookmarks found in database'
            }), 404
        
        # Generate HTML report
        books = query_result_to_book_list(bookmarks)
        template = env.get_template("default.html")
        html_content = template.render({"books": books, "date": date.today()})
        
        # Save report
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_filename = f"tmp/kobo_report_{timestamp}.html"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Clean up temp database file
        if os.path.exists(LOCAL_COPY_PATH):
            os.remove(LOCAL_COPY_PATH)
        
        return jsonify({
            'status': 'success',
            'report_url': f'/api/report/{os.path.basename(report_filename)}',
            'message': f'Report generated successfully with {len(books)} books'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/process-kindle', methods=['POST'])
def process_kindle():
    """Process Kindle device and generate report"""
    try:
        data = request.get_json()
        clippings_path = data.get('path')
        
        if not clippings_path:
            # Try to find automatically
            if platform.system() == 'Windows':
                try:
                    clippings_path = find_kindle_documents_path()
                except ImportError as e:
                    return jsonify({
                        'status': 'error',
                        'message': str(e) + ' Please provide the path manually or use file upload.'
                    }), 400
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Kindle path not provided and auto-detection not available on this platform'
                }), 400
        
        if not clippings_path or not os.path.exists(clippings_path):
            return jsonify({
                'status': 'error',
                'message': 'Kindle clippings file not found'
            }), 404
        
        # Parse clippings
        df = parse_clippings(clippings_path)
        
        if df.empty:
            return jsonify({
                'status': 'error',
                'message': 'No clippings found in file'
            }), 404
        
        # Generate report
        kindle_report(df)
        
        # Find the generated report (kindle_report creates a timestamped file)
        # We'll need to get the filename, but kindle_report doesn't return it
        # So we'll generate it with a predictable name
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_filename = f"tmp/kindle_report_{timestamp}.html"
        
        # Re-generate with known filename
        import pandas as pd
        
        env_kindle = Environment(loader=FileSystemLoader("templates"))
        parsed_data = {}
        for book, group in df.groupby("Book Title"):
            author = group["Metadata"].iloc[0].replace("Author: ", "")
            notes = group.apply(
                lambda row: {
                    "category": row["Category"].capitalize(),
                    "text": row["Text"],
                    "page": row["Page"] if pd.notna(row["Page"]) else "N/A",
                    "position": row["Position"],
                    "added_on": row["Added On"]
                },
                axis=1
            ).tolist()
            
            parsed_data[book] = {
                "author": author,
                "notes": notes
            }
        
        template = env_kindle.get_template("kindle_default.html")
        html_content = template.render(
            date=datetime.now().strftime("%Y-%m-%d"),
            books=parsed_data
        )
        
        with open(report_filename, "w", encoding="utf-8") as file:
            file.write(html_content)
        
        return jsonify({
            'status': 'success',
            'report_url': f'/api/report/{os.path.basename(report_filename)}',
            'message': f'Report generated successfully with {len(parsed_data)} books'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    """Handle file uploads (for manual file selection)"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        device_type = request.form.get('device_type', 'kindle')
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        # Save uploaded file
        if device_type == 'kindle':
            filename = 'My Clippings.txt'
        else:  # kobo
            filename = 'KoboReader.sqlite'
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        if device_type == 'kindle':
            # Process Kindle file
            df = parse_clippings(filepath)
            if df.empty:
                return jsonify({
                    'status': 'error',
                    'message': 'No clippings found in file'
                }), 404
            
            # Generate report (same logic as process_kindle)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            report_filename = f"tmp/kindle_report_{timestamp}.html"
            
            import pandas as pd
            
            env_kindle = Environment(loader=FileSystemLoader("templates"))
            parsed_data = {}
            for book, group in df.groupby("Book Title"):
                author = group["Metadata"].iloc[0].replace("Author: ", "")
                notes = group.apply(
                    lambda row: {
                        "category": row["Category"].capitalize(),
                        "text": row["Text"],
                        "page": row["Page"] if pd.notna(row["Page"]) else "N/A",
                        "position": row["Position"],
                        "added_on": row["Added On"]
                    },
                    axis=1
                ).tolist()
                
                parsed_data[book] = {
                    "author": author,
                    "notes": notes
                }
            
            template = env_kindle.get_template("kindle_default.html")
            html_content = template.render(
                date=datetime.now().strftime("%Y-%m-%d"),
                books=parsed_data
            )
            
            with open(report_filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'status': 'success',
                'report_url': f'/api/report/{os.path.basename(report_filename)}',
                'message': f'Report generated successfully with {len(parsed_data)} books'
            })
        
        else:  # kobo
            # Process Kobo file
            bookmarks = get_official_bookmarks_from_path(filepath)
            if not bookmarks:
                return jsonify({
                    'status': 'error',
                    'message': 'No bookmarks found in database'
                }), 404
            
            books = query_result_to_book_list(bookmarks)
            template = env.get_template("default.html")
            html_content = template.render({"books": books, "date": date.today()})
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            report_filename = f"tmp/kobo_report_{timestamp}.html"
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'status': 'success',
                'report_url': f'/api/report/{os.path.basename(report_filename)}',
                'message': f'Report generated successfully with {len(books)} books'
            })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


def get_official_bookmarks_from_path(db_path):
    """Get bookmarks from a specific database path"""
    from contextlib import closing
    
    with closing(open_connection(db_path)) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(bookmarks_query)
            bookmarks = cursor.fetchall()
            return bookmarks
        except Exception as e:
            print(f"Error querying database: {e}")
            return None


@app.route('/api/report/<filename>')
def get_report(filename):
    """Serve generated report HTML files"""
    try:
        report_path = os.path.join('tmp', filename)
        if os.path.exists(report_path):
            return send_file(report_path)
        else:
            return jsonify({
                'status': 'error',
                'message': 'Report not found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

