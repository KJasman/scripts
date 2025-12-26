import tkinter as tk
from tkinter import ttk, filedialog
import json
from pathlib import Path
from datetime import datetime
import webbrowser
import tempfile
import os

class InstagramPostGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Post Viewer")
        self.root.geometry("600x140")
        self.root.resizable(False, False)
        
        self.data_dir = None
        self.media_dir = None
        self.posts = []
        self.html_file = None
        
        self._create_widgets()
        self._show_welcome_message()
        
        # Cleanup temporary files on exit
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
    def _create_widgets(self):
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Data Directory:").pack(side=tk.LEFT)
        self.dir_label = ttk.Label(top_frame, text="No directory selected", foreground="gray")
        self.dir_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(top_frame, text="Select Directory", command=self._select_directory).pack(side=tk.RIGHT)
        
        search_frame = ttk.Frame(self.root, padding="10")
        search_frame.pack(fill=tk.X)
        
        search_controls = ttk.Frame(search_frame)
        search_controls.pack(fill=tk.X)
        
        ttk.Label(search_controls, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_controls, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.search_entry.bind('<Return>', lambda e: self._search_posts())
        
        ttk.Button(search_controls, text="Search", command=self._search_posts).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_controls, text="Clear", command=self._clear_search).pack(side=tk.LEFT)
        
        self.result_label = ttk.Label(search_frame, text="", foreground="blue")
        self.result_label.pack(fill=tk.X, pady=(5, 0))
        
    def _show_welcome_message(self):
        """Show welcome message when no directory is selected"""
        self.result_label.config(text="Select a directory to begin", foreground="gray")
        
    def _select_directory(self):
        directory = filedialog.askdirectory(title="Select Posts Directory")
        if directory:
            data_dir = Path(directory)
            # Check if it's the data directory or parent directory
            if data_dir.name == "data":
                self.data_dir = data_dir
                self.media_dir = data_dir.parent / "media"
            else:
                self.data_dir = data_dir / "data"
                self.media_dir = data_dir / "media"
            
            if self.data_dir.exists():
                self.dir_label.config(text=str(self.data_dir), foreground="black")
                self._load_all_posts()
            else:
                self.dir_label.config(text="Invalid directory structure", foreground="red")
                self.data_dir = None
                
        
    def _load_all_posts(self):
        """Load all posts from the data directory"""
        if not self.data_dir:
            return
            
        self.posts = []
        for json_file in self.data_dir.glob("*.json"):
            # Skip index.json if it exists
            if json_file.name == "index.json":
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    post = json.load(f)
                    # Ensure post is a dict, not a list
                    if isinstance(post, dict):
                        self.posts.append(post)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        
        self.result_label.config(text=f"Loaded {len(self.posts)} posts", foreground="blue")
        
    def _clear_search(self):
        """Clear search input and results"""
        self.search_entry.delete(0, tk.END)
        self.result_label.config(text=f"Loaded {len(self.posts)} posts" if self.posts else "Select a directory to begin", foreground="blue" if self.posts else "gray")
        
        
    def _fuzzy_match(self, text, keyword):
        """Simple fuzzy matching - checks if keyword appears in text (case insensitive)"""
        return keyword.lower() in text.lower()
        
    def _search_posts(self):
        keyword = self.search_entry.get().strip()
        
        if not keyword:
            self.result_label.config(text="Please enter a search keyword", foreground="orange")
            return
            
        if not self.posts:
            self.result_label.config(text="No posts loaded. Select a directory first.", foreground="red")
            return
        
        matching_posts = []
        for p in self.posts:
            if isinstance(p, dict) and self._fuzzy_match(p.get('caption', ''), keyword):
                matching_posts.append(p)
        
        self.result_label.config(text=f"Found {len(matching_posts)} matching posts", foreground="blue")
        
        if matching_posts:
            self._render_html(matching_posts, keyword)
        else:
            self.result_label.config(text=f'No posts found containing "{keyword}"', foreground="orange")
    
    def _render_html(self, posts, keyword):
        """Generate HTML and open in default browser"""
        html = self._build_html(posts, keyword)
        
        if self.html_file and os.path.exists(self.html_file):
            try:
                os.unlink(self.html_file)
            except OSError:
                pass
        
        fd, self.html_file = tempfile.mkstemp(suffix='.html', text=True)
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(html)
        
        webbrowser.open('file://' + self.html_file)
    
    def _on_closing(self):
        """Clean up temporary files and close the application"""
        if self.html_file and os.path.exists(self.html_file):
            try:
                os.unlink(self.html_file)
            except OSError:
                pass
        self.root.destroy()
    
    def _build_html(self, posts, keyword):
        """Build HTML content matching the instagram_viewer.py format"""
        post_cards = []
        for post in posts:
            media_html = self._generate_media_html(post)
            
            try:
                date_obj = datetime.fromisoformat(post['date'].replace('Z', '+00:00'))
                formatted_date = date_obj.strftime("%B %d, %Y")
            except (ValueError, KeyError):
                formatted_date = post.get('date', 'Unknown date')
            
            caption = post['caption'].replace('\n', '<br>')
            
            card_html = f"""
            <div class="post-card">
                <div class="media-container">
                    {media_html}
                </div>
                <div class="post-date">{formatted_date}</div>
                <div class="caption">
                    {caption}
                </div>
                <div class="post-footer">
                    <a href="{post['url']}" target="_blank" class="ig-link">View on Instagram →</a>
                </div>
            </div>
            """
            post_cards.append(card_html)
        
        posts_html = "\n".join(post_cards)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Posts - {keyword}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 4px;
        }}
        
        .header h1 {{
            font-size: 24px;
            color: #333;
        }}
        
        .posts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        
        .post-card {{
            background: white;
            border-radius: 4px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}
        
        .media-container {{
            background: #000;
            position: relative;
            aspect-ratio: 1;
            overflow: hidden;
        }}
        
        .media-container img,
        .media-container video {{
            width: 100%;
            height: 100%;
            display: block;
            object-fit: cover;
        }}
        
        .media-gallery {{
            display: flex;
            overflow-x: auto;
            scroll-snap-type: x mandatory;
        }}
        
        .media-gallery img,
        .media-gallery video {{
            flex: 0 0 100%;
            scroll-snap-align: start;
        }}
        
        .post-date {{
            padding: 10px 15px;
            font-size: 13px;
            color: #666;
            background: #f9f9f9;
            border-bottom: 1px solid #eee;
        }}
        
        .caption {{
            padding: 15px;
            color: #333;
            white-space: pre-wrap;
            flex: 1;
            font-size: 14px;
            line-height: 1.5;
        }}
        
        .caption mark {{
            background: #ffeb3b;
            padding: 2px 4px;
            border-radius: 2px;
        }}
        
        .post-footer {{
            padding: 15px;
            border-top: 1px solid #eee;
        }}
        
        .ig-link {{
            color: #0095f6;
            text-decoration: none;
            font-size: 14px;
        }}
        
        .ig-link:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 768px) {{
            .posts-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{len(posts)} post(s) containing "{keyword}"</h1>
        </div>
        
        <div class="posts-grid">
            {posts_html}
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_media_html(self, post):
        """Generate HTML for post media"""
        media_files = post.get('media_files', [])
        shortcode = post.get('shortcode', '')
        
        if not media_files:
            return '<div style="padding: 20px; text-align: center; color: #999;">No media</div>'
        
        if len(media_files) == 1:
            media_file = media_files[0]
            media_path = str(self.media_dir / shortcode / media_file).replace('\\', '/')
            
            if media_file.endswith('.mp4'):
                return f'<video controls preload="metadata"><source src="file:///{media_path}" type="video/mp4">Your browser does not support video.</video>'
            else:
                return f'<img src="file:///{media_path}" alt="Instagram post">'
        else:
            items = []
            for media_file in media_files:
                media_path = str(self.media_dir / shortcode / media_file).replace('\\', '/')
                if media_file.endswith('.mp4'):
                    items.append(f'<video controls preload="metadata"><source src="file:///{media_path}" type="video/mp4">Your browser does not support video.</video>')
                else:
                    items.append(f'<img src="file:///{media_path}" alt="Instagram post">')
            
            return f'<div class="media-gallery">{"".join(items)}</div>'


def main():
    root = tk.Tk()
    app = InstagramPostGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
