import markdown
import sys

def test_markdown_api():
    md_text = '# Hello Yocto\nThis is **bold** text.'
    expected_html_parts = [
        '<h1>Hello Yocto</h1>',
        '<p>This is <strong>bold</strong> text.</p>'
    ]
    
    html_output = markdown.markdown(md_text)
    
    for part in expected_html_parts:
        if part not in html_output:
            print(f'Logic failed: "{part}" not found in output')
            sys.exit(1)
            
    print('Markdown API test: PASSED')

if __name__ == '__main__':
    test_markdown_api()