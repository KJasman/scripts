# Instagram Post Extractor & Viewer

The purpose of this tool is to assist with small business owners who are looking 
to transition from Instagram-driven stores to either a proprietary online 
e-commerce platform (e.g. Shopify, Hostinger, Wix). 

This tool allows users to bulk extract and filter Instagram posts and find exactly
the listing they want. 

This tool is somewhat unrefined at the moment, but it is designed to meet the very
niche needs of some "makers" that sell via Instagram. Functionality may be expanded
by request or PR. 

## Extract Posts

1. Run `extract_posts.bat`
2. Enter Instagram profile to extract from
3. Enter your Instagram credentials
4. Enter keyword to search for
5. Posts saved to `instagram_posts/posts_{keyword}/`

## View Posts

1. Run `run_gui.bat`
2. Click "Select Directory"
3. Choose the posts folder (e.g., `instagram_posts/posts_available/`)
4. Type search keywords and click "Search"
5. Results open in browser

## Requirements

- Python 3.x
- Internet connection
- Instagram account


## Errata:

You can also just run the python files directly... The batch files exist to simplify the experience for some Windows users. 