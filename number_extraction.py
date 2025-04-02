import re
from decimal import Decimal

def extract_numbers(text):
    """
    Extract all numbers from text using regular expressions.
  
    """
    # Pattern for various number formats
    number_pattern = r'(-?(?:(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+)(?:[eE][-+]?\d+)?)'
    
    found_numbers = []
    
    # Find all matches
    for match in re.finditer(number_pattern, text):
        original = match.group(0)
        start_pos = match.start()
        
        # Convert to Decimal (remove commas first)
        clean_num = original.replace(',', '')
        
        decimal_value = Decimal(clean_num)

        # store the number, it's original string, and it's position
        found_numbers.append((decimal_value, original, start_pos))
        
    return found_numbers

def detect_table_boundaries(text):
    """
    Identify all tables in a text and their precise boundaries
    
    Args:
        text (str): The text to analyze
        
    Returns:
        list: List of dictionaries with table info including boundaries
    """
    tables = []
    lines = text.split('\n')
    
    # Look for table patterns
    table_start = None
    current_table = None
    
    for i, line in enumerate(lines):
        # Table rows typically have pipe characters or consistent spacing
        if '|' in line or re.search(r'\s{2,}', line):
            # Check if we're starting a new table
            if table_start is None:
                table_start = i
                current_table = {
                    'start_line': i,
                    'title': None,
                    'headers': [],
                    'end_line': None
                }
                
                # Look for title above the table
                for j in range(i-1, max(0, i-5), -1):
                    if lines[j].strip() and not '|' in lines[j]:
                        current_table['title'] = lines[j].strip()
                        break
            
            # If the second line has separator markers, the first line is likely headers
            if i == table_start + 1 and re.search(r'[-=|]+', line) and table_start > 0:
                current_table['headers'] = [h.strip() for h in re.split(r'\|', lines[table_start]) if h.strip()]
        
        # Table ends with an empty line or a line that's clearly not a table
        elif table_start is not None:
            # Empty line or clearly not a table row
            if not line.strip() or (not '|' in line and not re.search(r'\s{2,}', line)):
                current_table['end_line'] = i - 1
                tables.append(current_table)
                table_start = None
                current_table = None
    
    # If we ended in a table, add it
    if current_table is not None:
        current_table['end_line'] = len(lines) - 1
        tables.append(current_table)
    
    return tables


def get_table_for_position(tables, position, text):
    """
    Find which table (if any) contains the given position
    
    Args:
        tables (list): List of table dictionaries
        position (int): Position in text
        text (str): Full text
        
    Returns:
        dict or None: Table containing the position, or None
    """
    lines = text.split('\n')
    
    # Find which line contains our position
    current_pos = 0
    current_line = 0
    
    for i, line in enumerate(lines):
        if current_pos + len(line) >= position:
            current_line = i
            break
        current_pos += len(line) + 1  # +1 for the newline
    
    # Check which table contains this line
    for table in tables:
        if table['start_line'] <= current_line <= table['end_line']:
            return table
    
    return None
    
def detect_multiplier(context_text):
    """
    Detect if there's a multiplier like 'millions' or 'billions' in the context.
    """
    multipliers = {
        'million': 1_000_000,
        'millions': 1_000_000,
        'billion': 1_000_000_000,
        'billions': 1_000_000_000,
        'trillion': 1_000_000_000_000,
        'thousands': 1_000,
        'thousand': 1_000
    }
    
    # Convert to lowercase for case-insensitive matching
    context_lower = context_text.lower()
    
    # First check for shorthand notations in headings or labels
    notation_patterns = [
        (r'\(\$M\)', 1_000_000),       # ($M) - millions
        (r'\(M\$\)', 1_000_000),       # (M$) - millions
        (r'\(\$B\)', 1_000_000_000),   # ($B) - billions
        (r'\(B\$\)', 1_000_000_000),   # (B$) - billions
        (r'\(\$K\)', 1_000),           # ($K) - thousands
        (r'\(K\$\)', 1_000),           # (K$) - thousands
        (r'\$ *M', 1_000_000),         # $M or $ M - millions
        (r'M\$', 1_000_000),           # M$ - millions
        (r'\$ *B', 1_000_000_000),     # $B or $ B - billions
        (r'B\$', 1_000_000_000),       # B$ - billions
        (r'\$ *K', 1_000),             # $K or $ K - thousands
        (r'K\$', 1_000)                # K$ - thousands
    ]
    
    for pattern, value in notation_patterns:
        if re.search(pattern, context_text, re.IGNORECASE):
            return pattern, value
    
    # Check for explicit phrases indicating values are in specific units
    phrases = [
        ('dollars in millions', 1_000_000),
        ('(dollars in millions)', 1_000_000),
        ('$ in millions', 1_000_000),
        ('($ in millions)', 1_000_000),
        ('in millions', 1_000_000),
        ('(in millions)', 1_000_000),
        ('dollars in billions', 1_000_000_000),
        ('(dollars in billions)', 1_000_000_000),
        ('$ in billions', 1_000_000_000),
        ('($ in billions)', 1_000_000_000),
        ('in billions', 1_000_000_000),
        ('(in billions)', 1_000_000_000)
    ]
    
    for phrase, value in phrases:
        if phrase in context_lower:
            return phrase, value
    
    # Then look for standalone multiplier words
    for word, value in multipliers.items():
        if word in context_lower:
            # Make sure it's a whole word by checking for spaces or punctuation around it
            word_pattern = r'\b' + word + r'\b'
            if re.search(word_pattern, context_lower):
                return word, value
    
    # If no multiplier is found, return None and a value of 1 (no modification)
    return None, 1

def get_context(text, position, window=100):
    """Get context around a position in text."""
    start = max(0, position - window)
    end = min(len(text), position + window)
    return text[start:end]

def analyze_numbers(pdf_processor):
    """
    Analyze numbers with more precise table boundary detection
    """
    largest_raw = {'value': Decimal('-Infinity'), 'original': None, 'page': None}
    largest_modified = {'value': Decimal('-Infinity'), 'raw_value': None, 'original': None, 'page': None}
    
    # Process each page
    for page_num, page_text in enumerate(pdf_processor.pages):
        # First identify all tables on the page
        tables = detect_table_boundaries(page_text)
        
        # Extract all numbers from the page
        numbers = extract_numbers(page_text)
        
        for decimal_value, original, position in numbers:
            # Skip negative numbers
            if decimal_value < 0:
                continue
                
            # Get context around this number
            context_text = get_context(page_text, position)
            
            # Check if the number is in a table
            table = get_table_for_position(tables, position, page_text)
            
            # Initialize multiplier info
            multiplier_name = None
            multiplier_value = 1
            
            if table:
                # First check table title for modifiers
                if table['title']:
                    multiplier_name, multiplier_value = detect_multiplier(table['title'])
                
                # If no multiplier in title, check headers
                if not multiplier_name and table['headers']:
                    headers_text = " ".join(table['headers'])
                    multiplier_name, multiplier_value = detect_multiplier(headers_text)
            
            # If still no multiplier, check immediate context
            if not multiplier_name:
                multiplier_name, multiplier_value = detect_multiplier(context_text)
            
            # Calculate modified value
            modified_value = decimal_value * multiplier_value
            
            # Update largest raw number
            if decimal_value > largest_raw['value']:
                largest_raw = {
                    'value': decimal_value,
                    'original': original,
                    'page': page_num + 1,
                    'context': context_text[:150],
                    'in_table': table is not None,
                    'table_title': table['title'] if table else None
                }
            
            # Update largest modified number
            if modified_value > largest_modified['value']:
                largest_modified = {
                    'value': modified_value,
                    'raw_value': decimal_value,
                    'original': original,
                    'page': page_num + 1,
                    'context': context_text[:150],
                    'multiplier': multiplier_name,
                    'multiplier_value': multiplier_value,
                    'in_table': table is not None,
                    'table_title': table['title'] if table else None
                }
    
    return {
        'largest_raw': largest_raw,
        'largest_modified': largest_modified
    }