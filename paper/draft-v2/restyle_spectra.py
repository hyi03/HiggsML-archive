"""Restyle the pinned historical vector PDFs without reconstructing MC data.

Run with Python and PyMuPDF. Only connecting paths, titles and legends change.
The source PDFs, markers, error bars, axes and support shading are preserved.
These presentation derivatives do not recover the missing numerical artifacts.
"""
from decimal import Decimal
import argparse
import hashlib
import json
from pathlib import Path
import re

import pymupdf as fitz


ROOT = Path(__file__).resolve().parent
SOURCES = {
    'mass-yields': 'f43e44c43995193ed3bf2b00b85879a21fa402f6e174913a5e977b72d739a06b',
    'mass-shapes': '2652429bd80559042c1342d3174b809bd560d96b224beeb77a81d7a23c671f6d',
}
NUMBER = r'-?\d+(?:\.\d+)?'
CURVE = re.compile(rf'(?m)^(?:{NUMBER} {NUMBER} m\n)(?:{NUMBER} {NUMBER} l\n){{6}}\nS')
TEXT = re.compile(
    rf'q\n1 0 -0 1 (?P<x>{NUMBER}) (?P<y>{NUMBER}) cm\nBT\n'
    rf'/F1 (?P<size>{NUMBER}) Tf\n0 0 Td\n.*?\nET\nQ', re.S)
FRAME = re.compile(r'/A4 gs[^\n]*\n\n(?P<path>.*?)h\n\nB', re.S)


def replace_ranges(source, changes):
    """Keep every byte outside explicitly identified display changes."""
    position, output = 0, []
    for start, end, replacement in sorted(changes):
        if start < position:
            raise ValueError('Overlapping display changes')
        output.extend((source[position:start], replacement))
        position = end
    return ''.join(output) + source[position:]


def step_path(match):
    points = [line.split()[:2] for line in match.group().splitlines() if line.endswith((' m', ' l'))]
    xs = [Decimal(x) for x, _ in points]
    if len(points) != 7 or any(b <= a for a, b in zip(xs, xs[1:])):
        raise ValueError('Expected seven ordered bin centres')
    widths = [b - a for a, b in zip(xs, xs[1:])]
    if max(widths) - min(widths) > Decimal('0.00001'):
        raise ValueError('Expected equally spaced display bins')
    edges = [xs[0] - widths[0]/2]
    edges += [(a+b)/2 for a, b in zip(xs, xs[1:])]
    edges += [xs[-1] + widths[-1]/2]
    lines = [f'{edges[0]:f} {points[0][1]} m']
    for index, (_, y) in enumerate(points):
        lines.append(f'{edges[index+1]:f} {y} l')
        if index < 6:
            lines.append(f'{edges[index+1]:f} {points[index+1][1]} l')
    # Every bin retains its original PDF ordinate, without numeric resampling.
    return '\n'.join(lines) + '\n\nS'


def text_block(text, x, y, size):
    escaped = text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
    return f'q\n1 0 0 1 {x:.8f} {y:.8f} cm\nBT\n/helv {size} Tf\n0 g\n0 0 Td\n({escaped}) Tj\nET\nQ'


def restyle(stem, expected_hash, output):
    source = ROOT / 'figures/basic-20261108' / f'{stem}.pdf'
    if hashlib.sha256(source.read_bytes()).hexdigest() != expected_hash:
        raise ValueError(f'Historical source hash mismatch: {source}')
    document = fitz.open(source)
    if len(document) != 1:
        raise ValueError('Expected a single-page vector figure')
    page = document[0]
    streams = page.get_contents()
    if len(streams) != 1 or page.rotation:
        raise ValueError('Unexpected PDF stream layout')
    original = page.read_contents().decode('latin1')
    blocks = list(TEXT.finditer(original))
    spans = [span for block in page.get_text('dict')['blocks']
             for line in block.get('lines', []) for span in line['spans']]

    def locate(span):
        x, y = span['origin']
        matches = [block for block in blocks if abs(float(block['x'])-x) < .002
                   and abs(page.rect.height-float(block['y'])-y) < .002]
        if len(matches) != 1:
            raise ValueError(f'Cannot bind text to its PDF block: {span["text"]}')
        return matches[0]

    curves = list(CURVE.finditer(original))
    if len(curves) != 8:
        raise ValueError('Expected two seven-bin curves in each of four panels')
    changes = [(curve.start(), curve.end(), step_path(curve)) for curve in curves]
    titles = [span for span in spans if re.fullmatch(r'(ABCD|BCD):42, (signal|background)', span['text'])]
    if len(titles) != 4:
        raise ValueError('Unexpected panel titles')
    for span in titles:
        model, process = span['text'].split(', ')
        subset, seed = model.split(':')
        title = f'{subset}, seed {seed}: {process}'
        block = locate(span)
        centre = (span['bbox'][0]+span['bbox'][2])/2
        x = centre-fitz.get_text_length(title, fontname='helv', fontsize=12)/2
        changes.append((block.start(), block.end(), text_block(title, x, float(block['y']), 12)))
    for span in spans:
        if span['text'].startswith('Draft-v2 controlled MC'):
            title = ('Normalized four-lepton mass spectra' if stem == 'mass-shapes'
                     else 'Four-lepton mass spectra') + ' before and after selection (MC)'
            x = (page.rect.width-fitz.get_text_length(title, fontname='helv', fontsize=12))/2
            block = locate(span)
            changes.append((block.start(), block.end(), text_block(title, x, page.rect.height-27, 12)))
        elif span['text'].startswith('Fixed-network grouped MC errors;'):
            block = locate(span)
            changes.append((block.start(), block.end(), ''))

    legends = [span for span in spans if span['text'] == 'Baseline']
    if len(legends) != 4:
        raise ValueError('Unexpected legend count')
    for span in legends:
        before = locate(span)
        high_span = next(other for other in spans if other['text'] == 'High score'
                         and abs(other['origin'][0]-span['origin'][0]) < .002
                         and abs(other['origin'][1]-span['origin'][1]-15) < .002)
        after = locate(high_span)
        start = original.rfind('/A4 gs', 0, before.start())
        end = after.end()
        legend = original[start:end]
        frame = FRAME.match(legend)
        if frame is None:
            raise ValueError('Cannot identify the legend frame')
        coordinates = [list(map(float, line.split()[:-1])) for line in frame['path'].splitlines() if line.strip()]
        xs = [x for line in coordinates for x in line[::2]]
        midpoint = (min(xs)+max(xs))/2
        extra = max(0., fitz.get_text_length('Before selection', fontname='helv', fontsize=10)
                    - (high_span['bbox'][2]-high_span['bbox'][0]) + 3)
        def extend(line):
            parts = line.split()
            for index in range(0, len(parts)-1, 2):
                if float(parts[index]) > midpoint:
                    parts[index] = f'{float(parts[index])+extra:.8f}'
            return ' '.join(parts)
        path = '\n'.join(extend(line) for line in frame['path'].splitlines()) + '\n'
        replacement = text_block('Before selection', float(before['x']), float(before['y']), 10)
        legend = replace_ranges(legend, [(frame.start('path'), frame.end('path'), path),
                                        (before.start()-start, before.end()-start, replacement)])
        shift = -extra if max(xs) > page.rect.width-30 else 0
        legend = f'q\n1 0 0 1 {shift:.8f} 0 cm\n' + legend + '\nQ'
        changes.append((start, end, legend))
    if len(changes) != 18:
        raise ValueError('Expected eight curves, six title blocks and four legends')
    modified = replace_ranges(original, changes)
    # Content outside these 18 bounded substitutions is retained verbatim,
    # including scientific marker/error-bar commands and support shading.
    page.insert_font(fontname='helv')
    document.update_stream(streams[0], modified.encode('latin1'))
    metadata = document.metadata
    metadata.update(title=('Normalized mass spectra' if stem == 'mass-shapes' else 'Mass spectra'),
                    subject=f'Presentation-only derivative of SHA-256 {expected_hash}; no MC recomputation.')
    document.set_metadata(metadata)
    target = output / f'{stem}.pdf'
    document.save(target, garbage=4, deflate=True)
    document.close()
    check = fitz.open(target)
    if len(check[0].get_drawings()) != len(fitz.open(source)[0].get_drawings()):
        raise ValueError('Drawing count changed unexpectedly')
    text = check[0].get_text()
    if text.count('Before selection') != 4 or 'Draft-v2' in text or 'seed 42' not in text:
        raise ValueError('Restyled labels failed verification')
    check.close()
    target_name = str(target.relative_to(ROOT)) if target.is_relative_to(ROOT) else str(target)
    return dict(source=str(source.relative_to(ROOT)), source_sha256=expected_hash,
                output=target_name, output_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                changed_curves=8, changed_title_blocks=6, changed_legends=4,
                preserved='Other PDF content commands, including data markers, errors and shading, are unchanged.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('figures/report-en-20261115'),
                        help='Fresh output directory; relative paths start at this script directory.')
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.mkdir(exist_ok=False)
    audit = [restyle(stem, digest, output) for stem, digest in SOURCES.items()]
    (output/'presentation-audit.json').write_text(json.dumps(audit, indent=2)+'\n', encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
