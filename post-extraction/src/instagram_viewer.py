import json
from pathlib import Path
from datetime import datetime

class PostViewer:
    def __init__(self, data_dir="instagram_posts/data", media_dir="instagram_posts/media"):
        self.data_dir = Path(data_dir)
        self.media_dir = Path(media_dir)
        
    def search_posts(self, keyword):
        """Search posts by keyword in caption"""
        index_path = self.data_dir / "index.json"
        
        if not index_path.exists():
            print(f"Error: Index file not found at {index_path}")
            print("Please run instagram_extractor.py first!")
            return []
        
        with open(index_path, 'r', encoding='utf-8') as f:
            all_posts = json.load(f)
        
        keyword_lower = keyword.lower()
        matching_posts = []
        
        for post in all_posts:
            caption = post['caption']
            # Remove hashtags from caption for search
            caption_without_hashtags = self._remove_hashtags(caption)
            
            # Search in caption without hashtags
            if keyword_lower in caption_without_hashtags.lower():
                matching_posts.append(post)
        
        return matching_posts
    
    def _remove_hashtags(self, text):
        """Remove all hashtags from text"""
        import re
        return re.sub(r'#\w+', '', text)
    
    def generate_html(self, keyword, output_file=None):
        """Generate HTML page for posts matching keyword"""
        posts = self.search_posts(keyword)
        
        if not posts:
            print(f"No posts found containing '{keyword}'")
            return None
        
        print(f"Found {len(posts)} post(s) containing '{keyword}'")
        
        if output_file is None:
            safe_keyword = "".join(c if c.isalnum() else "_" for c in keyword)
            output_file = f"instagram_{safe_keyword}.html"
        
        html = self._build_html(posts, keyword)
        
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"HTML file created: {output_path.absolute()}")
        return output_path
    
    def _build_html(self, posts, keyword):
        """Build HTML content"""
        
        # Generate post cards
        post_cards = []
        for post in posts:
            media_html = self._generate_media_html(post)
            
            # Format date
            date_obj = datetime.fromisoformat(post['date'])
            formatted_date = date_obj.strftime("%B %d, %Y")
            
            # Highlight keyword in caption
            caption = post['caption'].replace('\n', '<br>')
            import re
            caption_highlighted = re.sub(
                f'({re.escape(keyword)})',
                r'<mark>\1</mark>',
                caption,
                flags=re.IGNORECASE
            )
            
            card_html = f"""
            <div class="post-card">
                <div class="media-container">
                    {media_html}
                </div>
                <div class="post-date">{formatted_date}</div>
                <div class="caption">
                    {caption_highlighted}
                </div>
                <div class="post-footer">
                    <a href="{post['url']}" target="_blank" class="ig-link">View on Instagram →</a>
                </div>
            </div>
            """
            post_cards.append(card_html)
        
        posts_html = "\n".join(post_cards)
        
        # Build complete HTML
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
        media_files = post['media_files']
        shortcode = post['shortcode']
        
        if len(media_files) == 1:
            # Single media
            media_file = media_files[0]
            # Ensure forward slashes for HTML/URLs
            media_path = f"instagram_posts/media/{shortcode}/{media_file}".replace('\\', '/')
            
            # Debug: Print the path being used
            print(f"  Media path: {media_path}")
            
            if media_file.endswith('.mp4'):
                return f'<video controls preload="metadata"><source src="{media_path}" type="video/mp4">Your browser does not support video.</video>'
            else:
                return f'<img src="{media_path}" alt="Instagram post" onerror="this.style.border=\'2px solid red\'">'
        else:
            # Multiple media (carousel)
            items = []
            for media_file in media_files:
                # Ensure forward slashes for HTML/URLs
                media_path = f"instagram_posts/media/{shortcode}/{media_file}".replace('\\', '/')
                print(f"  Media path: {media_path}")
                if media_file.endswith('.mp4'):
                    items.append(f'<video controls preload="metadata"><source src="{media_path}" type="video/mp4">Your browser does not support video.</video>')
                else:
                    items.append(f'<img src="{media_path}" alt="Instagram post" onerror="this.style.border=\'2px solid red\'">')
            
            return f'<div class="media-gallery">{"".join(items)}</div>'


def main():
    import sys
    
    print("Instagram Post Viewer")
    print("=" * 50)
    
    # Get keyword
    if len(sys.argv) > 1:
        keyword = " ".join(sys.argv[1:])
    else:
        keyword = input("Enter keyword to search for: ").strip()
    
    if not keyword:
        print("Error: Please provide a keyword")
        return
    
    # Create viewer and generate HTML
    viewer = PostViewer()
    html_path = viewer.generate_html(keyword)
    
    if html_path:
        print(f"\nOpen the HTML file in your browser to view the posts!")
        print(f"File: {html_path.absolute()}")


if __name__ == "__main__":
    main()
