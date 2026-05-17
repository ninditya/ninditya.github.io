import re

with open('/Users/ninditya/ninditya.github.io/index.html', 'r') as f:
    content = f.read()

def extract_grid(name):
    # Find start
    match = re.search(f'<div class="roadmap-grid" data-i18n="{name}">', content)
    if not match:
        return ""
    start_idx = match.end()
    
    # Simple nested div counter to find the end
    depth = 1
    idx = start_idx
    while depth > 0 and idx < len(content):
        next_open = content.find('<div', idx)
        next_close = content.find('</div', idx)
        
        if next_open == -1 and next_close == -1:
            break
            
        if next_open != -1 and next_open < next_close:
            depth += 1
            idx = next_open + 4
        else:
            depth -= 1
            idx = next_close + 5
            
    grid_html = content[start_idx:idx-6] # exclude the last </div>
    
    # minify
    grid_html = re.sub(r'\n\s*', '', grid_html)
    return grid_html

print("--- stage1Grid ---")
print(extract_grid('stage1Grid'))
print("\n--- stage2Grid ---")
print(extract_grid('stage2Grid'))
print("\n--- stage3Grid ---")
print(extract_grid('stage3Grid'))
