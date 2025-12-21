import instaloader
import json
from pathlib import Path

class InstagramExtractor:
    def __init__(self, username, output_dir="instagram_posts"):
        self.username = username
        self.output_dir = Path(output_dir)
        self.media_dir = self.output_dir / "media"
        self.data_dir = self.output_dir / "data"
        
        # Create directories
        self.media_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.loader = instaloader.Instaloader(
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=True,
            compress_json=False,
            post_metadata_txt_pattern=""
        )
    
    def login(self, username, password):
        """Login to Instagram"""
        try:
            self.loader.load_session_from_file(username)
            print(f"Loaded session for {username}")
            return
        except FileNotFoundError:
            pass
        
        print(f"Logging in as {username}...")
        try:
            self.loader.login(username, password)
            self.loader.save_session_to_file()
            print("Login successful!")
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            print("\n2-Factor Authentication required!")
            code = input("Enter 2FA code: ").strip()
            self.loader.two_factor_login(code)
            self.loader.save_session_to_file()
            print("Login successful with 2FA!")
    
    def extract_available_posts(self):
        """Extract all posts with 'AVAILABLE' in the caption"""
        print(f"\nFetching posts from @{self.username}...")
        profile = instaloader.Profile.from_username(self.loader.context, self.username)
        
        posts_data = []
        post_count = 0
        available_count = 0
        skipped_count = 0
        
        for post in profile.get_posts():
            post_count += 1
            caption = post.caption if post.caption else ""
            
            if "AVAILABLE" in caption.upper():
                available_count += 1
                
                # Check if post already exists
                post_dir = self.media_dir / post.shortcode
                json_path = self.data_dir / f"{post.shortcode}.json"
                
                if post_dir.exists() and json_path.exists():
                    print(f"\n[{available_count}] Skipping (already downloaded): {post.shortcode}")
                    print("Stopping - assuming all older posts are already downloaded.")
                    skipped_count += 1
                    
                    # Load existing post data for index
                    with open(json_path, 'r', encoding='utf-8') as f:
                        post_info = json.load(f)
                    posts_data.append(post_info)
                    break  # Stop checking older posts
                
                print(f"\n[{available_count}] Found AVAILABLE post: {post.shortcode}")
                
                # Create unique folder for this post
                post_dir.mkdir(exist_ok=True)
                
                # Download media
                media_files = self._download_post_media(post, post_dir)
                
                # Save post data
                post_info = {
                    "shortcode": post.shortcode,
                    "date": post.date_utc.isoformat(),
                    "caption": caption,
                    "likes": post.likes,
                    "media_files": media_files,
                    "url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "is_video": post.is_video
                }
                
                posts_data.append(post_info)
                
                # Save individual JSON
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(post_info, f, indent=2, ensure_ascii=False)
                
                print(f"  Saved {len(media_files)} media file(s)")
        
        # Save master index
        index_path = self.data_dir / "index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(posts_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*50}")
        print(f"Extraction complete!")
        print(f"Total posts scanned: {post_count}")
        print(f"Posts with 'AVAILABLE': {available_count}")
        print(f"Already downloaded (skipped): {skipped_count}")
        print(f"Newly downloaded: {available_count - skipped_count}")
        print(f"Data saved to: {self.output_dir}")
        print(f"{'='*50}")
        
        return posts_data
    
    def _download_post_media(self, post, post_dir):
        """Download all media from a post"""
        media_files = []
        
        if post.typename == 'GraphSidecar':  # Multiple images/videos
            for idx, node in enumerate(post.get_sidecar_nodes(), 1):
                if node.is_video:
                    filename = f"{post.shortcode}_{idx}.mp4"
                    filepath = post_dir / f"{post.shortcode}_{idx}"  # No extension - download_pic adds it
                    self.loader.download_pic(filename=str(filepath), 
                                            url=node.video_url, 
                                            mtime=post.date_utc)
                else:
                    filename = f"{post.shortcode}_{idx}.jpg"
                    filepath = post_dir / f"{post.shortcode}_{idx}"  # No extension - download_pic adds it
                    self.loader.download_pic(filename=str(filepath), 
                                            url=node.display_url, 
                                            mtime=post.date_utc)
                media_files.append(filename)
        else:  # Single image or video
            if post.is_video:
                filename = f"{post.shortcode}.mp4"
                filepath = post_dir / post.shortcode  # No extension - download_pic adds it
                self.loader.download_pic(filename=str(filepath), 
                                        url=post.video_url, 
                                        mtime=post.date_utc)
            else:
                filename = f"{post.shortcode}.jpg"
                filepath = post_dir / post.shortcode  # No extension - download_pic adds it
                self.loader.download_pic(filename=str(filepath), 
                                        url=post.url, 
                                        mtime=post.date_utc)
            media_files.append(filename)
        
        return media_files


def main():
    import getpass
    
    print("Instagram Post Extractor")
    print("=" * 50)
    
    # Get credentials\
    extract_target = input("Enter Instagram profile to extract from: ").strip()
    login_username = input("Enter Instagram username: ").strip()
    password = getpass.getpass("Enter Instagram password: ")
    
    # Create extractor
    extractor = InstagramExtractor(extract_target)
    
    # Login and extract
    extractor.login(login_username, password)
    extractor.extract_available_posts()


if __name__ == "__main__":
    main()
